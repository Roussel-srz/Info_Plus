import datetime
import sqlite3
import urllib.request
import os
import shutil
from pathlib import Path
import requests
import base64
import json
from config import GITHUB_TOKEN, REPO_OWNER, REPO_NAME

class DatabaseManager:
    def __init__(self, data_base="data_base.db", db_url="https://github.com/Roussel-srz/Info_Plus/raw/main/data_base.db"):
        """Initialise la connexion à la base de données."""
        self.local_db = data_base
        self.db_url = db_url
        self._ensure_backup_dir_exists()
        # self._download_db()  # Télécharge la base au démarrage
        self.conn = sqlite3.connect(self.local_db)
        self.GITHUB_TOKEN = GITHUB_TOKEN
        self.REPO_OWNER = REPO_OWNER
        self.REPO_NAME = REPO_NAME
        self._check_github_config()
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
    def _create_table(self):
        """Crée la table notes si elle n'existe pas."""
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            titre TEXT NOT NULL,
            description TEXT NOT NULL,
            importance INTEGER DEFAULT 1
        )
        ''')
        self.conn.commit()
        
    def _download_db(self):
        """Télécharge la base via une requête manuelle."""
        import requests
        try:
            headers = {"Authorization": f"token {self.GITHUB_TOKEN}"}
            url = f"https://api.github.com/repos/{self.REPO_OWNER}/{self.REPO_NAME}/contents/data_base.db"
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            # Décodage du contenu base64
            import base64
            db_content = base64.b64decode(response.json()["content"])
            
            # Sauvegarde locale
            with open(self.local_db, "wb") as f:
                f.write(db_content)
            return True
        except Exception as e:
            print(f"Erreur API GitHub : {e}")
            return False
        
    def _has_local_changes(self):
        """Vérifie si la base locale contient des données non synchronisées."""
        if not os.path.exists(self.local_db):
            return False
            
        conn = sqlite3.connect(self.local_db)
        try:
            cursor = conn.cursor()
            
            # Vérifier s'il y a des données dans les tables principales
            for table in ['gestion', 'factures', 'notes']:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                if cursor.fetchone()[0] > 0:
                    return True
                    
            return False
        finally:
            conn.close()

    def _create_empty_db(self):
        """Crée une nouvelle base de données vide avec toutes les tables nécessaires."""
        self.conn = sqlite3.connect(self.local_db)
        self.cursor = self.conn.cursor()
        self._create_table()
        
        # Créer la table gestion qui est nécessaire pour l'application
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS gestion (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            designation TEXT NOT NULL,
            quantite INTEGER NOT NULL,
            prix_unitaire INTEGER NOT NULL,
            entree INTEGER DEFAULT 0,
            sortie INTEGER DEFAULT 0,
            date TEXT NOT NULL,
            remarque TEXT,
            client TEXT
        )
        ''')
        
        # Ajoutez ici d'autres tables nécessaires pour votre application
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS factures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            num_facture TEXT NOT NULL,
            date_facture TEXT NOT NULL,
            nom_client TEXT NOT NULL,
            designation TEXT NOT NULL,
            quantite INTEGER NOT NULL,
            prix_unitaire INTEGER NOT NULL,
            montant INTEGER NOT NULL
        )
        ''')
        
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL UNIQUE
        )
        ''')
        
        # Ajouter quelques valeurs par défaut si nécessaire
        self.cursor.execute('''
        INSERT OR IGNORE INTO clients (nom) VALUES ('AUTRES')
        ''')
        
        self.conn.commit()
    

    def _ensure_backup_dir_exists(self):
        """Crée le dossier Backup_db s'il n'existe pas."""
        os.makedirs("Backup_db", exist_ok=True)

    def create_local_backup(self):
        """Crée une copie de sauvegarde locale sans interaction avec GitHub."""
        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = os.path.join("Backup_db", f"backup_{timestamp}.db")
            
            shutil.copyfile(self.local_db, backup_path)
            print(f"Sauvegarde locale créée: {backup_path}")
            return backup_path
        except Exception as e:
            print(f"Erreur lors de la sauvegarde locale: {e}")
            return None

    def sync(self, force=False):
        """Synchronise la base locale avec la version GitHub (téléchargement seulement)."""
        try:
            # Créer une sauvegarde locale avant sync
            self.create_local_backup()
            
            # Télécharger la nouvelle version
            self._download_db()
            return True
        except Exception as e:
            print(f"Erreur de synchronisation: {e}")
            return False
    def backup_to_github(self):
        """Envoie la base locale vers GitHub (upload seulement)."""
        if not self.github_configured:
            print("Configuration GitHub incomplète")
            return False

        try:
            with open(self.local_db, 'rb') as f:
                db_content = f.read()
            
            success = self._push_to_github(db_content, "Backup manuel de la base de données")
            
            if success:
                print("Sauvegarde vers GitHub réussie!")
                return True
            return False
        except Exception as e:
            print(f"Erreur lors de la sauvegarde GitHub: {e}")
            return False

    def manual_sync_with_github(self):
        """
        Synchronisation bidirectionnelle complète avec GitHub.
        Demande à l'utilisateur la direction de synchronisation.
        """
        try:
            # Vérifier l'état distant
            remote_updated = self._check_remote_updates()
            
            # Demander la direction
            choice = self._ask_sync_direction(remote_updated)
            
            if choice == "upload":
                return self.backup_to_github()
            elif choice == "download":
                return self.sync(force=True)
            return False
        except Exception as e:
            print(f"Erreur lors de la synchronisation: {e}")
            return False

    def _check_remote_updates(self):
        """Vérifie si GitHub a une version plus récente."""
        if not self.github_configured:
            return False

        try:
            url = f"https://api.github.com/repos/{self.REPO_OWNER}/{self.REPO_NAME}/commits?path=data_base.db"
            headers = {"Authorization": f"token {self.GITHUB_TOKEN}"}
            
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                last_commit = response.json()[0]['commit']['author']['date']
                remote_date = datetime.datetime.strptime(last_commit, "%Y-%m-%dT%H:%M:%SZ")
                local_date = datetime.datetime.fromtimestamp(os.path.getmtime(self.local_db))
                return remote_date > local_date
        except Exception:
            pass
        return False

    def _ask_sync_direction(self, remote_updated):
        """
        Affiche un dialogue pour choisir la direction de sync.
        Retourne "upload", "download" ou None.
        """
        # Cette méthode sera implémentée dans l'interface graphique (main.py)
        raise NotImplementedError("À implémenter dans l'interface utilisateur")
        
    def backup_to_github(self):
        """Sauvegarde la base de données vers GitHub via l'API"""
        if not hasattr(self, 'github_configured'):
            self._check_github_config()
            
        if not self.github_configured:
            return False

        try:
            # Lire le contenu de la base de données
            with open(self.local_db, 'rb') as f:
                db_content = f.read()
            
            # Utiliser la fonction push_to_github
            success = self._push_to_github(db_content, "Backup automatique de la base de donnée")
            
            if success:
                print("Sauvegarde vers GitHub réussie!")
                return True
            else:
                print("Échec de la sauvegarde vers GitHub")
                return False
        except Exception as e:
            print(f"Erreur lors de la sauvegarde: {e}")
            return False

    def _push_to_github(self, db_content, commit_message):
        """Envoie le contenu de la base de données vers GitHub via l'API"""
        url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/data_base.db"
        
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        # Vérifier d'abord le fichier existant pour obtenir son SHA
        response = requests.get(url, headers=headers)
        sha = response.json().get('sha', '') if response.status_code == 200 else ''
        
        data = {
            "message": commit_message,
            "content": base64.b64encode(db_content).decode('utf-8'),
            "sha": sha
        }
        
        response = requests.put(url, headers=headers, data=json.dumps(data))
        
        return response.status_code in [200, 201]

    def _check_github_config(self):
        """Vérifie si la configuration GitHub est valide"""
        self.github_configured = all([
            hasattr(self, 'GITHUB_TOKEN') and self.GITHUB_TOKEN,
            hasattr(self, 'REPO_OWNER') and self.REPO_OWNER,
            hasattr(self, 'REPO_NAME') and self.REPO_NAME
        ])
        
        if not self.github_configured:
            print("Configuration GitHub incomplète - sauvegarde désactivée")