from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMessageBox, QDialog, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import QDate
from ui_utils import create_button , create_label, titre,create_spinbox
from config import APP_NAME, LOGO_PATH
import sys

class NotesDialog(QDialog):
    def __init__(self, notes_manager, parent=None):
        super().__init__(parent)
        self.notes_manager = notes_manager
        self.setWindowTitle(f"{APP_NAME} - Gestion des Notes")
        self.setWindowIcon(QtGui.QIcon(LOGO_PATH))
        self.resize(800, 500)  # Taille initiale légèrement plus grande
        self.setMinimumSize(600, 400)  # Taille minimale
        self.setup_ui()
        

    def setup_ui(self):
        layout = QVBoxLayout()

        # Barre d'outils
        toolbar = QtWidgets.QToolBar()
        add_action = toolbar.addAction("Ajouter")
        add_action.triggered.connect(self.add_note)
        delete_action = toolbar.addAction("Supprimer")
        delete_action.triggered.connect(self.delete_selected_note)
        layout.addWidget(toolbar)

        # Tableau des notes
        self.notes_table = QtWidgets.QTableWidget()
        self.notes_table.setColumnCount(4)
        self.notes_table.setHorizontalHeaderLabels(["Date", "Titre", "Description", "Importance"])
        self.notes_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.notes_table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.notes_table.horizontalHeader().setStretchLastSection(False) 
        self.notes_table.doubleClicked.connect(self.edit_note)
        layout.addWidget(self.notes_table)

        # Boutons
        btn_layout = QHBoxLayout()
        close_btn = QtWidgets.QPushButton("Fermer")
        close_btn.clicked.connect(self.close)
        close_btn.setFixedHeight(30) 
        btn_layout.addWidget(close_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)
        self.load_notes()

    def load_notes(self):
        # Récupère toutes les notes triées par date (du plus récent au plus ancien)
        notes = self.notes_manager.get_all_notes()
        
        # Trie les notes par date (format dd/MM/yyyy)
        notes.sort(key=lambda x: QtCore.QDate.fromString(x[1], "dd/MM/yyyy"), reverse=True)
        
        self.notes_table.setRowCount(len(notes))
        
        for row, note in enumerate(notes):
            for col, data in enumerate(note[1:]):  # On saute l'ID
                item = QtWidgets.QTableWidgetItem(str(data))
                self.notes_table.setItem(row, col, item)
                
                # Colorer les notes importantes
                if note[4] >= 4:  # Si importance >= 4
                    item.setBackground(QtGui.QColor(255, 0, 0))
                    item.setForeground(QtGui.QColor("white"))
                elif note[4] >= 2:  # Si importance >= 2
                    item.setBackground(QtGui.QColor(0, 100, 150))
                    item.setForeground(QtGui.QColor("white"))

        # Ajuster la largeur des colonnes
        header = self.notes_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)  # Date
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)  # Titre
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.Stretch)  # Description prend le reste
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeMode.Fixed)
        header.resizeSection(3, 80)

    def add_note(self):
        dialog = NoteEditDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            date, titre, description, importance = dialog.get_data()
            self.notes_manager.add_note(date, titre, description, importance)
            self.load_notes()

    def edit_note(self, index):
        row = index.row()
        # Récupère toutes les notes triées comme elles sont affichées
        notes = self.notes_manager.get_all_notes()
        notes.sort(key=lambda x: QtCore.QDate.fromString(x[1], "dd/MM/yyyy"), reverse=True)
        
        note_id = notes[row][0]  # Utilise le même tri que l'affichage
        note_data = notes[row][1:]  # Récupère les données sans l'ID
        
        dialog = NoteEditDialog(self)
        dialog.set_data(*note_data)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            date, titre, description, importance = dialog.get_data()
            self.notes_manager.update_note(note_id, titre, description, importance)
            self.load_notes()
            
    def delete_selected_note(self):
        selected = self.notes_table.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner une note à supprimer")
            return
            
        row = selected[0].row()
        notes = self.notes_manager.get_all_notes()  # Déjà triées par date
        note_id = notes[row][0]
        
        reply = QMessageBox.question(
            self, 
            "Confirmation", 
            "Voulez-vous vraiment supprimer cette note?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.notes_manager.delete_note(note_id)
            self.load_notes()


class NoteEditDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Éditer une note")
        self.setup_ui()
        

    def setup_ui(self):
        layout = QVBoxLayout()

        # Date
        self.date_edit = QtWidgets.QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        layout.addWidget(QtWidgets.QLabel("Date:"))
        layout.addWidget(self.date_edit)

        # Titre
        self.titre_edit = QtWidgets.QLineEdit()
        layout.addWidget(QtWidgets.QLabel("Titre:"))
        layout.addWidget(self.titre_edit)

        # Description
        self.desc_edit = QtWidgets.QTextEdit()
        layout.addWidget(QtWidgets.QLabel("Description:"))
        layout.addWidget(self.desc_edit)

        # Importance
        self.importance_slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.importance_slider.setRange(1, 5)
        self.importance_slider.setTickPosition(QtWidgets.QSlider.TickPosition.TicksBelow)
        self.importance_slider.setTickInterval(1)
        layout.addWidget(QtWidgets.QLabel("Importance (1-5):"))
        layout.addWidget(self.importance_slider)

        # Boutons
        btn_layout = QHBoxLayout()
        ok_btn = QtWidgets.QPushButton("OK")
        ok_btn.clicked.connect(self.accept)
        cancel_btn = QtWidgets.QPushButton("Annuler")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(ok_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)
        
        

    def set_data(self, date, titre, description, importance):
        qdate = QDate.fromString(date, "dd/MM/yyyy")
        self.date_edit.setDate(qdate)
        self.titre_edit.setText(titre)
        self.desc_edit.setPlainText(description)
        self.importance_slider.setValue(importance)

    def get_data(self):
        date = self.date_edit.date().toString("dd/MM/yyyy")
        titre = self.titre_edit.text()
        description = self.desc_edit.toPlainText()
        importance = self.importance_slider.value()
        return date, titre, description, importance

if __name__ == "__main__":
    from note_manager import NotesManager
    
    app = QtWidgets.QApplication(sys.argv)
    try:
        with open("style.qss", "r") as file:
            app.setStyleSheet(file.read())
    except FileNotFoundError:
        print("Le fichier style.qss n'a pas été trouvé.")
    # Exemple d'utilisation
    notes_manager = NotesManager("data_base.db")
    dialog = NotesDialog(notes_manager)
    dialog.exec()
    
    notes_manager.close()
    sys.exit(app.exec())