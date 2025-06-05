import sqlite3

class DatabaseManager:
    def __init__(self, data_base):
        """Initialise la connexion à la base de données."""
        self.conn = sqlite3.connect(data_base)
        self.cursor = self.conn.cursor()

    def insert_data(self, designation, quantite, prix_unitaire, entree, sortie, date, remarque, client):
        """Insère une nouvelle entrée dans la table 'gestion'."""
        self.cursor.execute('''
        INSERT INTO gestion (designation, quantite, prix_unitaire, entree, sortie, date, remarque, client)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (designation, quantite, prix_unitaire, entree, sortie, date, remarque, client))
        self.conn.commit()
        print(f"Données insérées : Désignation='{designation}', Quantité={quantite}, Prix Unitaire={prix_unitaire}, client = {client}")

    def fetch_all_data(self):
        """Récupère toutes les entrées sans filtre."""
        try:
            self.cursor.execute('SELECT * FROM gestion ORDER BY id DESC')
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Erreur SQLite: {e}")
            return []

    def fetch_entree(self):
        """Récupère la somme des entrées par désignation pour une date donnée."""
        try:
            self.cursor.execute('''
                SELECT designation, SUM(entree) as total_entree 
                FROM gestion 
                WHERE date = "07/01/2025" 
                GROUP BY designation 
                ORDER BY designation
            ''')
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Erreur SQLite: {e}")
            return []
    
    def fetch_sortie(self):
        """Récupère la somme des sorties par désignation pour une date donnée."""
        try:
            self.cursor.execute('''
                SELECT designation, SUM(sortie) as total_sortie 
                FROM gestion 
                WHERE date = "07/01/2025" 
                GROUP BY designation 
                ORDER BY designation
            ''')
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Erreur SQLite: {e}")
            return []
    
    def fetch_data_by_jour(self, jour, month, year):
        """Récupère les entrées pour un jour, mois et année spécifiques."""
        try:
            query = '''
            SELECT * FROM gestion
            WHERE substr(date, 1, 2) = ? 
              AND substr(date, 4, 2) = ? 
              AND substr(date, 7, 4) = ?
            ORDER BY id DESC
            '''
            self.cursor.execute(query, (jour, month, year))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Erreur SQLite: {e}")
            return []

    def fetch_data_by_month(self, month, year):
        """Récupère les entrées pour un mois et année spécifiques."""
        try:
            query = '''
            SELECT * FROM gestion
            WHERE substr(date, 4, 2) = ? 
              AND substr(date, 7, 4) = ? 
            ORDER BY id DESC
            '''
            self.cursor.execute(query, (month, year))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Erreur SQLite: {e}")
            return []
    
    def fetch_data_by_year(self, year):
        """Récupère les entrées pour une année spécifique."""
        try:
            query = '''
            SELECT * FROM gestion
            WHERE substr(date, 7, 4) = ? 
            ORDER BY id DESC
            '''
            self.cursor.execute(query, (year,))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Erreur SQLite: {e}")
            return []

    def update_data(self, id, designation, quantite, prix_unitaire):
        """Met à jour une entrée existante."""
        try:
            self.cursor.execute('''
            UPDATE gestion
            SET designation = ?, quantite = ?, prix_unitaire = ?
            WHERE id = ?
            ''', (designation, quantite, prix_unitaire, id))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Erreur SQLite lors de la mise à jour: {e}")

    def delete_data(self, id):
        """Supprime une entrée de la table."""
        try:
            self.cursor.execute('DELETE FROM gestion WHERE id = ?', (id,))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Erreur SQLite lors de la suppression: {e}")

    def get_designations(self):
        """Récupère toutes les désignations distinctes."""
        try:
            self.cursor.execute('SELECT DISTINCT designation FROM gestion ORDER BY designation')
            return [row[0] for row in self.cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Erreur SQLite: {e}")
            return []

    def close(self):
        """Ferme la connexion à la base de données."""
        try:
            self.conn.close()
        except sqlite3.Error as e:
            print(f"Erreur SQLite lors de la fermeture: {e}")