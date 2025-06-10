import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMessageBox, QDialog, QVBoxLayout, QLineEdit, QPushButton
import sqlite3
import os
class ClientDialog(QDialog):
    def __init__(self, parent=None, client=None):
        super().__init__(parent)
        self.setWindowTitle("Ajouter/Modifier Client")
        self.setFixedSize(400, 300)
        
        layout = QVBoxLayout()
        
        self.nom_input = QLineEdit()
        self.nom_input.setPlaceholderText("Nom du client")
        layout.addWidget(self.nom_input)
        
        self.adresse_input = QLineEdit()
        self.adresse_input.setPlaceholderText("Adresse")
        layout.addWidget(self.adresse_input)
        
        self.telephone_input = QLineEdit()
        self.telephone_input.setPlaceholderText("Numéro de téléphone")
        layout.addWidget(self.telephone_input)
        
        btn_save = QPushButton("Enregistrer")
        btn_save.clicked.connect(self.accept)
        btn_save.setFixedHeight(30)  # Définit la hauteur du bouton à 50 pixels
        layout.addWidget(btn_save)  
        
        if client:
            self.nom_input.setText(client[1])
            self.adresse_input.setText(client[2])
            self.telephone_input.setText(client[3])
        
        self.setLayout(layout)
    
    def get_data(self):
        return {
            "nom": self.nom_input.text().strip(),
            "adresse": self.adresse_input.text().strip(),
            "telephone": self.telephone_input.text().strip()
        }
