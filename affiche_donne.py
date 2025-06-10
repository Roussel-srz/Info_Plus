import sys
from datetime import datetime
from PyQt6 import QtCore, QtGui, QtWidgets
from database_manager import DatabaseManager
from ui_utils import create_button , create_label, titre, create_table


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1100, 600)

        # Logo
        self.logo = QtWidgets.QPushButton(parent=Form)
        self.logo.setGeometry(QtCore.QRect(400, 200, 300, 300))
        self.logo.setObjectName("logo")
        
        sary = QtGui.QIcon()
        sary.addFile("logo.png", QtCore.QSize())
        self.logo.setIcon(sary)
        Form.setWindowIcon(sary)
        self.logo.setIconSize(QtCore.QSize(300, 300))

        # Initialisation de la base de données
        self.db_manager = DatabaseManager("data_base.db")

        # Titre
        font = QtGui.QFont()
        self.titre = QtWidgets.QLabel("Base de donnée", parent=Form)
        self.titre.setGeometry(QtCore.QRect(20, 20, 500, 51))
        
        font.setFamily("Microsoft New Tai Lue")
        font.setPointSize(36)
        font.setBold(True)
        self.titre.setFont(font)

        # Table Widget
        self.tableWidget = create_table(20, 80, 1050, 450, parent=Form, 
                     column_count=9,
                    headers=["ID", "Désignation", "Quantité", "Prix Unitaire", "Date", "Entrée", "Sortie", "Client", "Remarque"])
        
        self.tableWidget.setColumnWidth(0, 50)
        self.tableWidget.setColumnWidth(1, 200)
        self.tableWidget.setColumnWidth(2, 70)

        # Labels pour les totaux
        self.entree_label = QtWidgets.QLabel("Montant Total Entrant: 0 Ar", parent=Form)
        self.entree_label.setGeometry(QtCore.QRect(20, 540, 400, 30))
        
        self.sortie_label = QtWidgets.QLabel("Montant Total Sortant: 0 Ar", parent=Form)
        self.sortie_label.setGeometry(QtCore.QRect(400, 540, 400, 30))
        
        self.reste_label = QtWidgets.QLabel("Montant Total : 0 Ar", parent=Form)
        self.reste_label.setGeometry(QtCore.QRect(20, 570, 300, 30))

        font.setPointSize(14)
        self.entree_label.setFont(font)
        self.sortie_label.setFont(font)

        # ComboBox pour le jour
        self.jour = QtWidgets.QComboBox(parent=Form)
        self.jour.setGeometry(QtCore.QRect(620, 35, 51, 31))
        jour_list = ["Tout"] + [str(i + 1).zfill(2) for i in range(31)]
        self.jour.addItems(jour_list)
        self.jour.setCurrentIndex(datetime.now().day)

        # ComboBox pour le mois
        self.mois = QtWidgets.QComboBox(parent=Form)
        self.mois.setGeometry(QtCore.QRect(690, 35, 141, 31))
        mois_list = ["Tout", "Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
                     "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
        self.mois.addItems(mois_list)
        self.mois.setCurrentIndex(datetime.now().month)

        # ComboBox pour l'année
        self.annee = QtWidgets.QComboBox(parent=Form)
        self.annee.setGeometry(QtCore.QRect(850, 35, 80, 31))
        self.annee.addItems(["Toutes", "2025", "2026", "2027", "2028", "2029"])
        self.annee.setCurrentText(str(datetime.now().year))

        # Connexion des signaux
        self.jour.currentIndexChanged.connect(self.filtre)
        self.mois.currentIndexChanged.connect(self.filtre)
        self.annee.currentIndexChanged.connect(self.filtre)

        # Chargement initial des données
        self.filtre()


    def filtre(self):
        """Filtre les données selon les critères sélectionnés."""
        try:
            year_str = self.annee.currentText()
            month_index = self.mois.currentIndex()
            jour = self.jour.currentText()

            # Si "Toutes" est sélectionné pour l'année
            if year_str == "Toutes":
                self.load_data()
                return

            # Si "Tout" est sélectionné pour le mois
            if month_index == 0:
                self.load_data(year=year_str)
                return

            # Si "Tout" est sélectionné pour le jour
            if jour == "Tout":
                month_str = str(month_index).zfill(2)
                self.load_data(month=month_str, year=year_str)
                return

            # Filtre complet (jour, mois, année)
            month_str = str(month_index).zfill(2)
            self.load_data(jour=jour, month=month_str, year=year_str)

        except Exception as e:
            print(f"Erreur lors du filtrage: {e}")

    def load_data(self, jour=None, month=None, year=None):
        """Charge les données selon les filtres spécifiés."""
        try:
            # Déterminer quel filtre appliquer
            if jour and month and year:
                data = self.db_manager.fetch_data_by_jour(jour, month, year)
            elif month and year:
                data = self.db_manager.fetch_data_by_month(month, year)
            elif year:
                data = self.db_manager.fetch_data_by_year(year)
            else:
                data = self.db_manager.fetch_all_data()

            self.tableWidget.setRowCount(len(data) if data else 0)
            
            total_entree = total_sortie = reste = 0

            if data:
                for row_index, row_data in enumerate(data):
                    for column_index, item in enumerate(row_data):
                        item_text = str(item) if item is not None else ""
                        self.tableWidget.setItem(row_index, column_index,
                                              QtWidgets.QTableWidgetItem(item_text))
                    
                    # Calcul des totaux
                    total_entree += row_data[5] if row_data[5] is not None else 0
                    total_sortie += row_data[6] if row_data[6] is not None else 0

            reste = total_entree - total_sortie
            
            # Formatage des nombres avec séparateurs de milliers
            formatted_entree = "{:,}".format(total_entree).replace(",", " ")
            formatted_sortie = "{:,}".format(total_sortie).replace(",", " ")
            formatted_reste = "{:,}".format(reste).replace(",", " ")
            
            # Mise à jour des labels
            self.entree_label.setText(f"Montant Total Entrant: <font color='green'>{formatted_entree} Ar</font>")
            self.sortie_label.setText(f"Montant Total Sortant: <font color='red'>{formatted_sortie} Ar</font>")
            
            color = 'yellow' if reste >= 0 else 'red'
            self.reste_label.setText(f"Montant Total : <font color='{color}'>{formatted_reste} Ar</font>")

        except Exception as e:
            print(f"Erreur lors du chargement des données: {e}")
            self.tableWidget.setRowCount(0)
            self.entree_label.setText("Montant Total Entrant: 0 Ar")
            self.sortie_label.setText("Montant Total Sortant: 0 Ar")
            self.reste_label.setText("Montant Total : 0 Ar")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    try:
        with open("style_dark.qss", "r") as file:
            app.setStyleSheet(file.read())
    except FileNotFoundError:
        print("Le fichier style.qss n'a pas été trouvé.")

    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())