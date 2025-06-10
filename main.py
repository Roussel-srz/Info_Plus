from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMessageBox, QDialog, QVBoxLayout, QTextEdit, QDialogButtonBox
from PyQt6.QtCore import QDate
from ui_utils import create_button, create_label, titre, create_spinbox
from config import LOGO_PATH, APP_NAME, BASE_DE_DONNEE
import sys
import darkdetect  # Pour détecter le thème système (à installer avec `pip install darkdetect`)
import subprocess
import os

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
        self.Gestion_vente_label = titre("GESTION DE VENTE",x=120,y=35, parent=Form,font_size=28)

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
        self.btn_add_client.setObjectName("add_client_main")

        # Bouton de validation
        self.valider_btn = self.btn_add_client = create_button("VALIDER",420, 320, 181, 41, parent=Form,font_size=18)
        self.valider_btn.setShortcut("Ctrl+Return")
        self.valider_btn.clicked.connect(self.validate_input) # Connecter le bouton à la méthode de validation
        self.valider_btn.setObjectName("valider_btn")

        # Autres composants de l'interface utilisateur
        self.designation_lbl = create_label("Désignation",90, 150, 131, 21, parent=Form)
        self.quantite_label = create_label("Quantité",250, 150, 131, 21, parent=Form)
        self.prix_unitaire_label = create_label("Prix Unitaire",410, 150, 131, 21, parent=Form)
        self.client_label = create_label("Client :", 190, 280, 131, 21, parent=Form)

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        font.setUnderline(True)

        spin_font = QtGui.QFont()
        spin_font.setFamily("Segoe UI")
        spin_font.setPointSize(12)
        self.prix_unitaire = create_spinbox(430, 180, 81,min_val=100,parent=Form,suffix=" Ar")
        self.prix_unitaire.setFont(spin_font)
        
        # Enlever les boutons d'augmentation et de diminution
        self.prix_unitaire.setButtonSymbols(QtWidgets.QAbstractSpinBox.ButtonSymbols.NoButtons)
        # self.prix_unitaire.setButtonSymbols()
        
        # SpinBox pour quantité
        self.quantite = create_spinbox(290, 181, 61, parent=Form, min_val=0)
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
        self.notes_btn.setGeometry(QtCore.QRect(537, 60, 131, 30))
        self.notes_btn.setShortcut("Ctrl+N")
        self.notes_btn.clicked.connect(self.open_notes_interface)
        # Ajoutez ce bouton après les autres boutons
        # Bouton Sauvegarde Locale
        self.backup_btn = QtWidgets.QPushButton("Sauvegarde Locale", parent=Form)
        self.backup_btn.setGeometry(QtCore.QRect(400, 365, 121, 30))
        self.backup_btn.clicked.connect(self.create_local_backup)
        self.backup_btn.setObjectName("sync_btn")

        # Bouton Sync GitHub
        self.sync_btn = QtWidgets.QPushButton("Sync GitHub", parent=Form)
        self.sync_btn.setGeometry(QtCore.QRect(530, 365, 121, 30))
        self.sync_btn.clicked.connect(self.manual_sync_with_github)
        self.sync_btn.setObjectName("sync_btn")

        # Bouton Partage
        self.partage_btn = QtWidgets.QPushButton("PARTAGE", parent=Form)
        self.partage_btn.setObjectName("partage_btn")
        self.partage_btn.setGeometry(QtCore.QRect(537, 140, 131, 30))
        self.partage_btn.clicked.connect(self.open_partage_interface)
        

        # Bouton pour basculer entre les styles
        self.toggle_style_btn = QtWidgets.QPushButton("", parent=Form)
        self.toggle_style_btn.setGeometry(QtCore.QRect(537, 180, 131, 30))
        self.toggle_style_btn.setObjectName("toggle_style_btn")
        self.toggle_style_btn.clicked.connect(self.toggle_style)
        self.update_style_button_text()  # Mettre à jour le texte du bouton

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
    def toggle_style(self):
        """Bascule entre le style par défaut, le mode sombre et le thème système."""
        current_style = app.styleSheet()
        
        if "style_dark.qss" in current_style:
            # Revenir au style système (par défaut)
            with open("style.qss", "r") as file:
                app.setStyleSheet(file.read())
        else:
            # Passer au mode sombre
            with open("style_dark.qss", "r") as file:
                app.setStyleSheet(file.read())
        
        self.update_style_button_text()

    def update_style_button_text(self):
        """Met à jour le texte du bouton en fonction du style actuel."""
        current_style = app.styleSheet()
        if "style_dark.qss" in current_style:
            self.toggle_style_btn.setText("Mode Clair")
        else:
            self.toggle_style_btn.setText("Mode Sombre")

    def use_system_theme(self):
        """Applique le thème système (Windows)."""
        try:
            if darkdetect.theme() == "Dark":
                with open("style_dark.qss", "r") as file:
                    app.setStyleSheet(file.read())
            else:
                with open("style.qss", "r") as file:
                    app.setStyleSheet(file.read())
        except:
            app.setStyleSheet("")  # Fallback si darkdetect échoue
    def open_partage_interface(self):
        """Ouvre l'interface de partage de fichiers."""
        from partage_interface import PartageDialog
        dialog = PartageDialog(Form)  # Form comme parent
        dialog.exec()
    def setup_designation(self, parent):
        self.designation = QtWidgets.QComboBox(parent=parent)
        self.designation.setGeometry(QtCore.QRect(80, 181, 161, 31))
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
         self.afficher_btn.setGeometry(QtCore.QRect(537, 100, 131, 30))
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
    
    def sync_db(self):
        reply = QMessageBox.question(
            self, 
            'Confirmation', 
            'La synchronisation écrasera les données locales. Voulez-vous continuer?', 
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                success = self.db_manager.sync()
                if success:
                    QMessageBox.information(self, "Succès", "Base de données synchronisée !")
                else:
                    QMessageBox.warning(self, "Avertissement", "La synchronisation a échoué")
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Échec de la synchronisation : {str(e)}")
# --------------------------------------------------------------------------------------

    def backup_to_github(self):
        """Gère la sauvegarde vers GitHub"""
        # Vérifier d'abord la configuration
        if not self._check_github_config():
            self._show_github_config_dialog()
            return
            
        reply = QMessageBox.question(
            None, 
            'Confirmation', 
            'Voulez-vous sauvegarder vos données vers GitHub?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                success = self.db_manager.backup_to_github()
                if success:
                    QMessageBox.information(None, "Succès", "Sauvegarde vers GitHub réussie!")
                else:
                    QMessageBox.warning(None, "Avertissement", "Échec de la sauvegarde")
            except Exception as e:
                QMessageBox.critical(None, "Erreur", f"Erreur lors de la sauvegarde: {str(e)}")

    def _check_github_config(self):
        """Vérifie si la configuration GitHub est complète"""
        from config import GITHUB_TOKEN, REPO_OWNER, REPO_NAME
        return all([GITHUB_TOKEN, REPO_OWNER, REPO_NAME])

    def _show_github_config_dialog(self):
        """Affiche un dialogue pour configurer GitHub"""
        dialog = QtWidgets.QDialog()
        dialog.setWindowTitle("Configuration GitHub")
        layout = QtWidgets.QVBoxLayout()
        
        # Champ pour le token
        token_label = QtWidgets.QLabel("Token GitHub:")
        token_input = QtWidgets.QLineEdit()
        token_input.setPlaceholderText("Collez votre token d'accès GitHub ici")
        
        # Boutons
        btn_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.StandardButton.Ok | QtWidgets.QDialogButtonBox.StandardButton.Cancel)
        btn_box.accepted.connect(dialog.accept)
        btn_box.rejected.connect(dialog.reject)
        
        layout.addWidget(token_label)
        layout.addWidget(token_input)
        layout.addWidget(btn_box)
        dialog.setLayout(layout)
        
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            # Sauvegarder la configuration
            with open("config.py", "a") as f:
                f.write(f"\nGITHUB_TOKEN = '{token_input.text()}'\n")
            QMessageBox.information(None, "Succès", "Configuration sauvegardée! Redémarrez l'application.")
    

    def create_local_backup(self):
        """Gère la création d'une sauvegarde locale."""
        try:
            backup_path = self.db_manager.create_local_backup()
            if backup_path:
                QMessageBox.information(
                    None, 
                    "Succès", 
                    f"Sauvegarde locale créée:\n{os.path.basename(backup_path)}"
                )
            else:
                QMessageBox.warning(None, "Erreur", "Échec de la sauvegarde locale")
        except Exception as e:
            QMessageBox.critical(None, "Erreur", f"Erreur lors de la sauvegarde: {str(e)}")

    def manual_sync_with_github(self):
        """Gère la synchronisation manuelle avec GitHub."""
        if not self._check_github_config():
            self._show_github_config_dialog()
            return

        # Vérifier les mises à jour distantes
        remote_updated = False
        try:
            remote_updated = self.db_manager._check_remote_updates()
        except Exception as e:
            print(f"Erreur vérification distante: {e}")

        # Afficher le dialogue de choix
        choice = self._ask_sync_direction(remote_updated)
        
        if choice == "upload":
            self._upload_to_github()
        elif choice == "download":
            self._download_from_github()

    def _ask_sync_direction(self, remote_updated):
        """Affiche le dialogue pour choisir la direction de synchronisation."""
        msg = QMessageBox()
        msg.setWindowTitle("Direction de synchronisation")
        msg.setText("Choisissez l'opération de synchronisation:")
        
        if remote_updated:
            msg.setInformativeText("⚠ Une version plus récente existe sur GitHub!")
        
        btn_upload = msg.addButton("Envoyer vers GitHub", QMessageBox.ButtonRole.ActionRole)
        btn_download = msg.addButton("Télécharger depuis GitHub", QMessageBox.ButtonRole.ActionRole)
        msg.addButton(QMessageBox.StandardButton.Cancel)
        
        msg.exec()
        
        if msg.clickedButton() == btn_upload:
            return "upload"
        elif msg.clickedButton() == btn_download:
            return "download"
        return None

    def _upload_to_github(self):
        """Gère l'envoi vers GitHub."""
        reply = QMessageBox.question(
            None, 
            'Confirmation', 
            'Envoyer les données locales vers GitHub?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                success = self.db_manager.backup_to_github()
                if success:
                    QMessageBox.information(None, "Succès", "Données envoyées vers GitHub!")
                else:
                    QMessageBox.warning(None, "Avertissement", "Échec de l'envoi")
            except Exception as e:
                QMessageBox.critical(None, "Erreur", f"Erreur lors de l'envoi: {str(e)}")

    def _download_from_github(self):
        """Gère le téléchargement depuis GitHub."""
        reply = QMessageBox.question(
            None, 
            'Confirmation', 
            'Remplacer les données locales par la version GitHub?\nCette action écrasera toutes vos données locales!',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                # Forcer le téléchargement même s'il y a des données locales
                success = self.db_manager.sync(force=True)
                if success:
                    QMessageBox.information(None, "Succès", "Données synchronisées depuis GitHub!")
                else:
                    QMessageBox.warning(None, "Avertissement", "Échec de la synchronisation")
            except Exception as e:
                QMessageBox.critical(None, "Erreur", f"Erreur lors du téléchargement: {str(e)}")
                
# Code principal de l'application
if __name__ == "__main__":
    import subprocess
    from database_manager import DatabaseManager  # Assurez-vous que ce fichier est dans le même répertoire
    from facture_db_manager import FactureDatabaseManager
    from  client_dialog import ClientDialog
    from client_manager import ClientManager
    from note_manager import NotesManager


    app = QtWidgets.QApplication(sys.argv)

    # Appliquer le thème système au démarrage
    def use_system_theme():
        try:
            if darkdetect.theme() == "Dark":
                with open("style_dark.qss", "r") as file:
                    app.setStyleSheet(file.read())
            else:
                with open("style.qss", "r") as file:
                    app.setStyleSheet(file.read())
        except:
            app.setStyleSheet("")  # Fallback si darkdetect échoue

    use_system_theme()

    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())
