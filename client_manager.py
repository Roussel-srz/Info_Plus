# client_manager.py
import sqlite3
from PyQt6.QtWidgets import QMessageBox, QDialog
from client_dialog import ClientDialog
class ClientManager:
    def __init__(self, db_file="data_base.db"):
        self.conn = sqlite3.connect(db_file)
        self.create_table()

    def create_table(self):
        """Crée la table si elle n'existe pas"""
        query = """
        CREATE TABLE IF NOT EXISTS liste_client (
            id_client INTEGER PRIMARY KEY AUTOINCREMENT,
            nom_client TEXT NOT NULL UNIQUE,  
            adresse_client TEXT,
            numero_client TEXT
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def get_all_clients(self):
        """Récupère tous les clients"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM liste_client ORDER BY nom_client")
        return cursor.fetchall()

    def get_client_names(self):
        """Récupère seulement les noms des clients"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT nom_client FROM liste_client ORDER BY nom_client")
        return [row[0] for row in cursor.fetchall()]

    def add_client(self, nom, adresse="", numero=""):
        """Ajoute un nouveau client"""
        try:
            self.conn.execute(
                "INSERT INTO liste_client (nom_client, adresse_client, numero_client) VALUES (?, ?, ?)",
                (nom, adresse, numero)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def add_client_with_dialog(self, parent=None):
        """Ouvre un dialogue pour ajouter un client et retourne le nom si réussi"""
        dialog = ClientDialog(parent)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            if data["nom"]:
                if self.add_client(data["nom"], data["adresse"], data["telephone"]):
                    return data["nom"]
                else:
                    QMessageBox.warning(parent, "Erreur", "Ce client existe déjà!")
            else:
                QMessageBox.warning(parent, "Erreur", "Le nom du client est obligatoire!")
        return None


    def update_client(self, id_client, nom, adresse, numero):
        """Met à jour un client existant"""
        self.conn.execute(
            "UPDATE liste_client SET nom_client=?, adresse_client=?, numero_client=? WHERE id_client=?",
            (nom, adresse, numero, id_client)
        )
        self.conn.commit()

    def delete_client(self, id_client):
        """Supprime un client"""
        self.conn.execute("DELETE FROM liste_client WHERE id_client=?", (id_client,))
        self.conn.commit()