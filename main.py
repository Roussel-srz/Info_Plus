from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QDate, QTime
from ui_utils import create_button , create_label, titre,create_spinbox
from config import LOGO_PATH, APP_NAME, BASE_DE_DONNEE
import sys

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(688, 398)

        self.logo = QtWidgets.QPushButton(parent=Form)
        self.logo.setGeometry(QtCore.QRect(10,10,100,100))
        self.logo.setObjectName("logo")
        sary = QtGui.QIcon()
        sary.addFile(LOGO_PATH, QtCore.QSize())
        self.logo.setIcon(sary)
        Form.setWindowIcon(sary)
        Form.setWindowTitle(APP_NAME)
        self.logo.setIconSize(QtCore.QSize(100,100))

        # Initialiser DatabaseManager
        self.db_manager = DatabaseManager(BASE_DE_DONNEE)
        self.facture_db_manager = FactureDatabaseManager(BASE_DE_DONNEE)
        self.client_db_manager = ClientManager(BASE_DE_DONNEE)
        self.Gestion_vente_label = titre("GESTION DE VENTE",parent=Form)

        # Champ de texte pour remarques
        self.remarque = QtWidgets.QLineEdit(parent=Form)
        self.remarque.setGeometry(QtCore.QRect(180, 235, 451, 31))
        self.remarque.setObjectName("remarque")
        
        # ComboBox pour désignation
        
        self.font10 = QtGui.QFont()
        self.font10.setPointSize(10)
        self.setup_designation(Form)

        # -------------------------------
        self.client = QtWidgets.QComboBox(parent=Form)
        self.client.setGeometry(QtCore.QRect(180, 300, 161, 31))
        self.client.setFont(self.font10)
        self.client.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.client.setEditable(True)
        
        # Charger les clients depuis la base de données
        self.load_clients()
        
        # Bouton pour ajouter un nouveau client
        self.btn_add_client = create_button("+",350, 300, 31, 31, parent=Form)
        self.btn_add_client.setShortcut("Ctrl++")
        self.btn_add_client.clicked.connect(self.add_new_client)

        # Bouton de validation
        self.valider_btn = self.btn_add_client = create_button("VALIDER",420, 320, 181, 41, parent=Form,font_size=18)
        self.valider_btn.setShortcut("Ctrl+Return")
        self.valider_btn.clicked.connect(self.validate_input) # Connecter le bouton à la méthode de validation

        # Autres composants de l'interface utilisateur
        self.designation_lbl = create_label("Désignation",190, 150, 131, 21, parent=Form)
        self.quantite_label = create_label("Quantité",380, 150, 131, 21, parent=Form)
        self.prix_unitaire_label = create_label("Prix Unitaire",510, 150, 131, 21, parent=Form)
        self.client_label = create_label("Client :", 190, 280, 131, 21, parent=Form)

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        font.setUnderline(True)

        spin_font = QtGui.QFont()
        spin_font.setFamily("Segoe UI")
        spin_font.setPointSize(12)
        self.prix_unitaire = create_spinbox(530, 180, 81,min_val=100,parent=Form,suffix=" Ar")
        self.prix_unitaire.setFont(spin_font)
        
        # Enlever les boutons d'augmentation et de diminution
        self.prix_unitaire.setButtonSymbols(QtWidgets.QAbstractSpinBox.ButtonSymbols.NoButtons)
        # self.prix_unitaire.setButtonSymbols()
        
        # SpinBox pour quantité
        self.quantite = create_spinbox(390, 181, 61, parent=Form, min_val=0)
        # self.quantite.setGeometry(QtCore.QRect(390, 181, 61, 31))
        self.quantite.setFont(spin_font)
         # RadioButtons pour entrée/sortie
        self.entree = QtWidgets.QRadioButton("Entrée", parent=Form)
        self.entree.setGeometry(QtCore.QRect(350, 280, 89, 20))
        self.sortie = QtWidgets.QRadioButton("Sortie", parent=Form)
        self.sortie.setGeometry(QtCore.QRect(440 ,280 ,89 ,20))
        self.sortie.setObjectName("sortie")
         # checkbox facturée
        self.facture = QtWidgets.QCheckBox("Facturée",parent=Form)
        self.facture.setGeometry(QtCore.QRect(520 ,280 ,89 ,20))
        self.facture.setObjectName("facture")

         # Champ de texte numero facture
        self.num_facture = QtWidgets.QLineEdit(parent=Form)
        self.num_facture.setGeometry(QtCore.QRect(590, 280, 80, 20))

        # Définir la valeur par défaut avec la date du jour au format DDMMYYYY_
        current_date = QDate.currentDate()
        default_num_facture = current_date.toString("ddMMyyyy") + "_"
        self.num_facture.setText(default_num_facture)

         # DateEdit pour sélectionner une date
        self.date = QtWidgets.QDateEdit(parent=Form)
        self.date.setGeometry(QtCore.QRect(40, 360, 110, 22))

        # Définir la date actuelle
        self.date.setDate(QDate.currentDate())  # Pour définir uniquement la date actuelle
        # Ou pour définir la date et l'heure actuelles :
        # self.date.setDateTime(QDateTime.currentDateTime())
        self.date.setCalendarPopup(True)

         # Label pour remarques
        self.label_5 = QtWidgets.QLabel("Remarque :", parent=Form)
        self.label_5.setGeometry(QtCore.QRect(50 ,240 ,131 ,21))
        font = QtGui.QFont()
        font.setFamily("Rage Italic")
        font.setPointSize(18)
        font.setUnderline(True)
        self.label_5.setFont(font)
        
        self.powered = QtWidgets.QLabel("Powerd By ROUSSEL", parent=Form)
        self.powered.setGeometry(QtCore.QRect(260, 366, 110, 22))

        # Bouton pour les notes
        self.notes_btn = QtWidgets.QPushButton("NOTES", parent=Form)
        self.notes_btn.setObjectName("notes_btn")
        self.notes_btn.setGeometry(QtCore.QRect(400, 20, 131, 30))
        self.notes_btn.setShortcut("Ctrl+N")
        self.notes_btn.clicked.connect(self.open_notes_interface)

         # Appel à la méthode pour traduire l'interface
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def setup_designation(self, parent):
        self.designation = QtWidgets.QComboBox(parent=parent)
        self.designation.setGeometry(QtCore.QRect(180, 181, 161, 31))
        self.designation.setFont(self.font10)
        self.designation.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.designation.setEditable(True)
        # Charger depuis la base de données
        designations = self.db_manager.get_designations()
        if designations:
            self.designation.addItems(designations)
        else:
            # Valeurs par défaut si la base est vide
            self.designation.addItems([
                "PHOTOCOPIE", "PHOTOCOPIE COULEUR", "IMPRESSION", "SAISIE"
            ])                              


    def retranslateUi(self ,Form):
         _translate = QtCore.QCoreApplication.translate
        #  Form.setWindowTitle(_translate("Form" ,"Info Plus"))

         #BOUTTON D'AFFICHAGE DE BASE DE DONNEE
         self.afficher_btn = QtWidgets.QPushButton("Afficher Données", parent=Form)
         self.afficher_btn.setShortcut("Ctrl+D")
         self.afficher_btn.setObjectName("affiche_btn")
         self.afficher_btn.setGeometry(QtCore.QRect(500, 100, 131, 30))
         self.afficher_btn.clicked.connect(self.open_affiche_donne)  # Connecter le bouton à la méthode
         #BOUTTON DE FACTURE
         self.facture_btn = QtWidgets.QPushButton("FACTURE", parent=Form)
         self.facture_btn.setObjectName("facture_btn")
         self.facture_btn.setGeometry(QtCore.QRect(540, 20, 131, 30))
         self.facture_btn.setShortcut("Ctrl+F")
         self.facture_btn.clicked.connect(self.open_facture)  # Connecter le bouton à la méthode
    def open_notes_interface(self):
        """Ouvre l'interface de gestion des notes."""
        from notes_interface import NotesDialog
        from note_manager import NotesManager
        
        notes_manager = NotesManager(BASE_DE_DONNEE)
        dialog = NotesDialog(notes_manager, Form)  # Form comme parent
        dialog.exec()
        notes_manager.close()
    def load_clients(self):
        """Charge la liste des clients depuis la base de données"""
        clients = self.facture_db_manager.get_all_clients()
        self.client.clear()
        self.client.addItems(clients if clients else ["AUTRES"])

    # Dans main.py, modifiez la méthode add_new_client:
    # Dans main.py, changez la méthode add_new_client:
    def add_new_client(self):
        """Ajoute un nouveau client à la base de données"""
        # Passez Form comme parent au lieu de self (Ui_Form)
        client_name = self.client_db_manager.add_client_with_dialog(Form) 
        if client_name:
            self.load_clients()  # Recharger la liste
            self.client.setCurrentText(client_name)  # Sélectionner le nouveau client
    
    def open_affiche_donne(self):
        """Ouvre l'application pour afficher les données."""
        subprocess.Popen([sys.executable, "affiche_donne.py"])  # Ouvre le script affiche_donne.py
    def open_facture(self):
        """Ouvre l'application pour facture."""
        subprocess.Popen([sys.executable, "facture.py"])  # Ouvre le script affiche_donne.py
    def validate_input(self):
        designation = self.designation.currentText()
        quantity = self.quantite.value()
        prix_unitaire = self.prix_unitaire.value()
        remarks = self.remarque.text()
        client = self.client.currentText()
        selected_date = self.date.date()
        selected_date_str = selected_date.toString('dd/MM/yyyy')
        entree = quantity * prix_unitaire
        sortie = quantity * prix_unitaire
        num_facture = self.num_facture.text()

        if not designation:
            QMessageBox.warning(None, "Erreur d'entrée", "Veuillez sélectionner une désignation.")
            return

        if quantity <= 0:
            QMessageBox.warning(None, "Erreur d'entrée", "La quantité doit être supérieure à zéro.")
            return

        try:
            # Insertion dans la base principale
            if self.entree.isChecked():
                self.db_manager.insert_data(designation, quantity, prix_unitaire, entree, 0, selected_date_str, remarks, client)
            elif self.sortie.isChecked():
                self.db_manager.insert_data(designation, quantity, prix_unitaire, 0, sortie, selected_date_str, remarks, client)
            else:
                QMessageBox.warning(None, "Erreur d'entrée", "Entrée ou Sortie ?.")
                return

            # Si la facture est cochée, insertion dans la table facture
            if self.facture.isChecked():
                montant = quantity * prix_unitaire
                facture_db_manager = FactureDatabaseManager("data_base.db")
                facture_db_manager.insert_facture(
                    num_facture=num_facture,
                    date_facture=selected_date_str,
                    nom_client=client,
                    designation=designation,
                    quantite=quantity,
                    prix_unitaire=prix_unitaire,
                    montant=montant
                )
                del facture_db_manager  # Ferme la connexion

            QMessageBox.information(None, "Succès", 
                                f"Désignation : {designation}\n"
                                f"Quantité : {quantity}\n"
                                f"Prix Unitaire : {prix_unitaire} Ar\n"
                                f"Remarques : {remarks}\n"
                                f"Date : {selected_date_str}")

        except Exception as e:
            QMessageBox.critical(None, "Erreur", f"Une erreur est survenue : {str(e)}")
    

# Code principal de l'application
if __name__ == "__main__":
    import subprocess
    from database_manager import DatabaseManager  # Assurez-vous que ce fichier est dans le même répertoire
    from facture_db_manager import FactureDatabaseManager
    from  client_dialog import ClientDialog
    from client_manager import ClientManager

    app = QtWidgets.QApplication(sys.argv)

    # Charger le fichier QSS
    with open("style.qss", "r") as file:
        app.setStyleSheet(file.read())

    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())
