# fenetre_login.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from ui_utils import create_button, create_label

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Connexion")
        layout = QVBoxLayout()

        label = create_label("Bienvenue")
        button = create_button("Se connecter")

        layout.addWidget(label)
        layout.addWidget(button)
        self.setLayout(layout)
