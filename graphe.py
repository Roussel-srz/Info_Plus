import sys
from PyQt6 import QtWidgets
import pyqtgraph as pg
from database_manager import DatabaseManager
import numpy as np

class TransactionApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager('data_base.db')  # Remplacez par le nom de votre base de données
        self.initUI()

    def initUI(self):
        layout = QtWidgets.QVBoxLayout()
        self.graphWidget = pg.PlotWidget()
        layout.addWidget(self.graphWidget)

        # Récupérer les données pour le mois souhaité (par exemple janvier 2025)
        month = "01"  # Mois (format MM)
        year = "2025"  # Année (format AAAA)
        data = self.db_manager.fetch_data_by_month(month, year)

        # Initialiser les totaux des entrées et sorties pour chaque jour
        self.jours = np.arange(1, 32)  # Jours du mois (1 à 31)
        self.entrees = np.zeros(31)  # Entrées par jour
        self.sorties = np.zeros(31)   # Sorties par jour

        for row in data:
            jour = int(row[4][:2])  # Supposons que la date est au format "JJ/MM/AAAA"
            
            # Convertir entree et sortie en int, gérer les erreurs potentielles
            try:
                entree = int(row[5]) if row[5] else 0  # Colonne 'entree'
                sortie = int(row[6]) if row[6] else 0   # Colonne 'sortie'
            except ValueError:
                print(f"Erreur de conversion pour la ligne: {row}")
                entree = 0
                sortie = 0
            
            if 1 <= jour <= 31:  # Vérifier que le jour est valide
                self.entrees[jour - 1] += entree
                self.sorties[jour - 1] += sortie

        # Tracer les données
        self.plotData()

        # Connecter le clic sur le graphique à la méthode d'affichage des transactions
        self.graphWidget.scene().sigMouseClicked.connect(self.on_click)

        self.setLayout(layout)
        self.setWindowTitle('Visualisation des Transactions')
        self.show()

    def plotData(self):
        self.graphWidget.clear()
        
        # Tracer les entrées et sorties
        self.graphWidget.plot(self.jours, self.entrees, pen='g', name='Entrées', symbol='o', label='Entrées')
        self.graphWidget.plot(self.jours, self.sorties, pen='r', name='Sorties', symbol='x', label='Sorties')
        
        # Ajouter une légende
        self.graphWidget.addLegend()
        
        # Configurer les axes
        self.graphWidget.setLabel('left', 'Montant')
        self.graphWidget.setLabel('bottom', 'Jours du mois')

    def on_click(self, event):
        mouse_point = event.scenePos()
        index = int(mouse_point.x())

        if 0 <= index < len(self.jours):
            jour_clique = str(self.jours[index]).zfill(2)  # Format JJ pour la date
            transactions = self.db_manager.fetch_data_by_jour(jour_clique, "01", "2025")  # Exemple pour janvier

            if transactions:
                self.show_transactions_table(transactions)
            else:
                QtWidgets.QMessageBox.information(self, "Transactions du Jour", "Aucune transaction pour ce jour.")

    def show_transactions_table(self, transactions):
        """Affiche un tableau avec les transactions."""
        
        table_window = QtWidgets.QDialog(self)
        table_window.setWindowTitle("Transactions du Jour")
        
        layout = QtWidgets.QVBoxLayout()
        
        table_widget = QtWidgets.QTableWidget()
        
        table_widget.setRowCount(len(transactions))
        table_widget.setColumnCount(8)  # Nombre de colonnes selon votre structure
        
        table_widget.setHorizontalHeaderLabels(["ID", "Désignation", "Quantité", "Prix Unitaire", "Date", "Entrée", "Sortie", "Client"])
        
        for row_index, row in enumerate(transactions):
            for col_index in range(len(row)):
                table_widget.setItem(row_index, col_index, QtWidgets.QTableWidgetItem(str(row[col_index])))
        
        layout.addWidget(table_widget)
        
        table_window.setLayout(layout)
        
        table_window.exec()  # Afficher la fenêtre modale

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = TransactionApp()
    sys.exit(app.exec())
