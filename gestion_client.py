import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import  QDialog
import os
from ui_utils import create_button , create_label, titre, create_table


class Ui_ClientForm(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1000, 600)

        # Titre
        self.titre = titre("GESTION DES CLIENTS",x = 10,y=15, parent=Form)

        # Logo
        self.logo = QtWidgets.QPushButton(parent=Form)
        self.logo.setGeometry(QtCore.QRect(400, 200, 300, 300))
        self.logo.setObjectName("logo")
        if os.path.exists("logo.png"):
            sary = QtGui.QIcon()
            sary.addFile("logo.png", QtCore.QSize())
            self.logo.setIcon(sary)
            Form.setWindowIcon(sary)
            self.logo.setIconSize(QtCore.QSize(300, 300))
        
        # Tableau des clients
        self.table_clients = create_table(20, 90, 900, 440, parent=Form, 
                     column_count=4,
                    headers=["ID", "Nom", "Adresse", "Téléphone"],
                    )
        
        # Définir la largeur des colonnes
        self.table_clients.setColumnWidth(0, 50)  # ID
        self.table_clients.setColumnWidth(1, 300)  # Nom
        self.table_clients.setColumnWidth(2, 300)  # Adresse
        self.table_clients.setColumnWidth(3, 200)  # Téléphone
        
        # Boutons
        self.btn_ajouter = create_button("Ajouter", 20, 540, 150, 30, parent=Form, object_name="btn_ajouter")
        self.btn_modifier = create_button("Modifier", 190, 540, 150, 30, parent=Form, object_name="btn_modifier")
        self.btn_supprimer = create_button("Supprimer", 360, 540, 150, 30, parent=Form, object_name="btn_supprimer")

class GestionClientsUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_ClientForm()
        self.ui.setupUi(self)
        
        self.db = ClientManager()
        
        # Connexion des signaux
        self.ui.btn_ajouter.clicked.connect(self.ajouter_client)
        self.ui.btn_modifier.clicked.connect(self.modifier_client)
        self.ui.btn_supprimer.clicked.connect(self.supprimer_client)
        
        # Chargement initial
        self.charger_clients()
    
    def charger_clients(self):
        """Charge la liste des clients dans le tableau"""
        clients = self.db.get_all_clients()
        self.ui.table_clients.setRowCount(len(clients))
        
        for row, client in enumerate(clients):
            for col, data in enumerate(client):
                item = QtWidgets.QTableWidgetItem(str(data))
                item.setFlags(item.flags() ^ QtCore.Qt.ItemFlag.ItemIsEditable)
                self.ui.table_clients.setItem(row, col, item)
    
    # Dans gestion_client.py, modifiez ajouter_client:
    def ajouter_client(self):
        """Ouvre la boîte de dialogue pour ajouter un client"""
        client_name = self.db.add_client_with_dialog(self)
        if client_name:
            self.charger_clients()

    def modifier_client(self):
        """Modifie le client sélectionné"""
        selected = self.ui.table_clients.currentRow()
        if selected >= 0:
            # Vérifier que tous les items existent avant d'accéder à leurs textes
            items = [
                self.ui.table_clients.item(selected, 0),
                self.ui.table_clients.item(selected, 1),
                self.ui.table_clients.item(selected, 2),
                self.ui.table_clients.item(selected, 3)
            ]
            
            # Si un des items est None, afficher un message d'erreur
            if any(item is None for item in items):
                QtWidgets.QMessageBox.warning(self, "Erreur", "Données du client incomplètes!")
                return
                
            client_id = int(items[0].text())
            client_data = (
                client_id,
                items[1].text(),
                items[2].text(),
                items[3].text()
            )
            
            dialog = ClientDialog(self, client_data)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                data = dialog.get_data()
                if data["nom"]:
                    self.db.update_client(client_id, data["nom"], data["adresse"], data["telephone"])
                    self.charger_clients()
                else:
                    QtWidgets.QMessageBox.warning(self, "Erreur", "Le nom du client est obligatoire!")
        else:
            QtWidgets.QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un client!")

    def supprimer_client(self):
        """Supprime le client sélectionné"""
        selected = self.ui.table_clients.currentRow()
        if selected >= 0:
            reply = QtWidgets.QMessageBox.question(
                self, 
                "Confirmation", 
                "Êtes-vous sûr de vouloir supprimer ce client?",
                QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
            )
            
            if reply == QtWidgets.QMessageBox.StandardButton.Yes:
                client_id = int(self.ui.table_clients.item(selected, 0).text())
                self.db.delete_client(client_id)
                self.charger_clients()
        else:
            QtWidgets.QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un client!")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    from  client_dialog import ClientDialog
    from client_manager import ClientManager
    
    try:
        with open("style.qss", "r") as file:
            app.setStyleSheet(file.read())
    except FileNotFoundError:
        print("Le fichier style.qss n'a pas été trouvé.")
    
    window = GestionClientsUI()
    window.show()
    sys.exit(app.exec())