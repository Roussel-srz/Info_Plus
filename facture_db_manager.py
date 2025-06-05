import sqlite3

class FactureDatabaseManager:
    def __init__(self, data_base):
        self.conn = sqlite3.connect(data_base)
        self.cursor = self.conn.cursor()
        self.create_table()
    
    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS facture (
            num_facture TEXT,
            date_facture TEXT,
            nom_client TEXT,
            designation TEXT,
            quantite INTEGER,
            prix_unitaire INTEGER,
            montant INTEGER
        )
        """
        self.cursor.execute(query)
        self.conn.commit()
    
    def insert_facture(self, num_facture, date_facture, nom_client, designation, quantite, prix_unitaire, montant):
        query = """
        INSERT INTO facture (num_facture, date_facture, nom_client, designation, quantite, prix_unitaire, montant)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        self.cursor.execute(query, (num_facture, date_facture, nom_client, designation, quantite, prix_unitaire, montant))
        self.conn.commit()
    
    def fetch_factures_grouped(self):
        """Récupère les factures groupées par num_facture avec le total"""
        query = """
        SELECT num_facture, nom_client, SUM(montant) as total 
        FROM facture 
        GROUP BY num_facture
        ORDER BY date_facture DESC
        """
        return self.cursor.execute(query).fetchall()

    def fetch_facture_details(self, num_facture):
        """Récupère toutes les lignes d'une facture spécifique"""
        query = """
        SELECT designation, quantite, prix_unitaire, montant 
        FROM facture 
        WHERE num_facture = ?
        ORDER BY designation
        """
        return self.cursor.execute(query, (num_facture,)).fetchall()
    # --------------------------client-------------------------------
    def create_client_table(self):
        """Crée la table liste_client si elle n'existe pas"""
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS liste_client (
            id_client INTEGER PRIMARY KEY AUTOINCREMENT,
            nom_client TEXT UNIQUE,
            adresse_client TEXT
        )
        ''')
        self.conn.commit()

    def get_all_clients(self):
        """Récupère tous les clients de la table liste_client"""
        self.cursor.execute('SELECT nom_client FROM liste_client ORDER BY nom_client')
        return [row[0] for row in self.cursor.fetchall()]

    def add_client(self, nom_client, adresse_client=None):
        """Ajoute un nouveau client à la table"""
        try:
            self.cursor.execute('''
            INSERT INTO liste_client (nom_client, adresse_client)
            VALUES (?, ?)
            ''', (nom_client, adresse_client))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            # Le client existe déjà (nom_client est UNIQUE)
            return False
        
    def fetch_facture_info(self, num_facture):
        """Récupère les informations de base d'une facture"""
        query = """
        SELECT num_facture, nom_client, date_facture, SUM(montant) as total
        FROM facture 
        WHERE num_facture = ?
        GROUP BY num_facture
        """
        return self.cursor.execute(query, (num_facture,)).fetchone()

    def close(self):
        """Ferme la connexion à la base de données"""
        self.conn.close()
    
    def __del__(self):
        """Destructeur - ferme la connexion si elle est encore ouverte"""
        if hasattr(self, 'conn'):
            self.conn.close()