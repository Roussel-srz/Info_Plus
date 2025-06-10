import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMessageBox, QDialog, QVBoxLayout, QLineEdit, QPushButton
from client_manager import ClientManager
# 

class GestionClientsUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GESTION DES CLIENTS")
        self.resize(1100, 600)
        
        # Style de police
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        
        # Titre
        self.titre = QtWidgets.QLabel("GESTION DES CLIENTS", parent=self)
        self.titre.setGeometry(QtCore.QRect(10, 10, 1060, 51))
        self.titre.setFont(font)
        self.titre.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        
        # Logo (optionnel)
        self.logo = QtWidgets.QPushButton(parent=self)
        self.logo.setGeometry(QtCore.QRect(400, 200, 300, 300))
        self.logo.setObjectName("logo")
        sary = QtGui.QIcon()
        sary.addFile("logo.png", QtCore.QSize())
        self.logo.setIcon(sary)
        self.logo.setIconSize(QtCore.QSize(300, 300))
        
        # Initialisation de la base de données
        self.db = ClientManager()
        
        # Tableau des clients
        self.table = QtWidgets.QTableWidget(parent=self)
        self.table.setGeometry(QtCore.QRect(20, 70, 1060, 400))
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Nom", "Adresse", "Téléphone"])
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setColumnWidth(0, 50)
        self.table.setColumnWidth(1, 250)
        self.table.setColumnWidth(2, 400)
        self.table.setColumnWidth(3, 150)
        
        # Boutons
        self.btn_add = QtWidgets.QPushButton("Ajouter", parent=self)
        self.btn_add.setGeometry(QtCore.QRect(20, 500, 150, 30))
        
        self.btn_edit = QtWidgets.QPushButton("Modifier", parent=self)
        self.btn_edit.setGeometry(QtCore.QRect(200, 500, 150, 30))
        
        self.btn_delete = QtWidgets.QPushButton("Supprimer", parent=self)
        self.btn_delete.setGeometry(QtCore.QRect(380, 500, 150, 30))
        
        self.btn_actualiser = QtWidgets.QPushButton("Actualiser", parent=self)
        self.btn_actualiser.setGeometry(QtCore.QRect(900, 500, 150, 30))
        
        # Connexions
        self.btn_add.clicked.connect(self.add_client)
        self.btn_edit.clicked.connect(self.edit_client)
        self.btn_delete.clicked.connect(self.delete_client)
        self.btn_actualiser.clicked.connect(self.load_clients)
        
        # Charger les données initiales
        self.load_clients()
    
    def load_clients(self):
        """Charge la liste des clients dans le tableau"""
        clients = self.db.get_all_clients()
        self.table.setRowCount(len(clients))
        
        for row, client in enumerate(clients):
            for col, data in enumerate(client):
                item = QtWidgets.QTableWidgetItem(str(data))
                item.setFlags(item.flags() ^ QtCore.Qt.ItemFlag.ItemIsEditable)
                self.table.setItem(row, col, item)
    
    def add_client(self):
        """Ouvre la boîte de dialogue pour ajouter un client"""
        dialog = ClientDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            if data["nom"]:
                if self.db.add_client(data["nom"], data["adresse"], data["telephone"]):
                    self.load_clients()
                else:
                    QMessageBox.warning(self, "Erreur", "Ce client existe déjà!")
            else:
                QMessageBox.warning(self, "Erreur", "Le nom du client est obligatoire!")
    
    def edit_client(self):
        """Modifie le client sélectionné"""
        selected = self.table.currentRow()
        if selected >= 0:
            client_id = int(self.table.item(selected, 0).text())
            client_data = (
                client_id,
                self.table.item(selected, 1).text(),
                self.table.item(selected, 2).text(),
                self.table.item(selected, 3).text()
            )
            
            dialog = ClientDialog(self, client_data)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                data = dialog.get_data()
                if data["nom"]:
                    self.db.update_client(client_id, data["nom"], data["adresse"], data["telephone"])
                    self.load_clients()
                else:
                    QMessageBox.warning(self, "Erreur", "Le nom du client est obligatoire!")
        else:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un client!")
    
    def delete_client(self):
        """Supprime le client sélectionné"""
        selected = self.table.currentRow()
        if selected >= 0:
            reply = QMessageBox.question(
                self, 
                "Confirmation", 
                "Êtes-vous sûr de vouloir supprimer ce client?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                client_id = int(self.table.item(selected, 0).text())
                self.db.delete_client(client_id)
                self.load_clients()
        else:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un client!")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    from gestion_client import ClientDialog
    # Charger le style CSS si disponible
    try:
        with open("style.qss", "r") as file:
            app.setStyleSheet(file.read())
    except FileNotFoundError:
        print("Fichier style.qss non trouvé - utilisation du style par défaut")
    
    window = GestionClientsUI()
    window.show()
    sys.exit(app.exec())