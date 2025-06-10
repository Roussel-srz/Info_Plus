import sqlite3
class NotesManager:
    def __init__(self, data_base):
        """Initialise la connexion à la base de données pour les notes."""
        self.conn = sqlite3.connect(data_base)
        self.cursor = self.conn.cursor()
        self._create_table()

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

    def add_note(self, date, titre, description, importance=1):
        """Ajoute une nouvelle note."""
        self.cursor.execute('''
        INSERT INTO notes (date, titre, description, importance)
        VALUES (?, ?, ?, ?)
        ''', (date, titre, description, importance))
        self.conn.commit()

    def get_all_notes(self):
        """Récupère toutes les notes triées par date décroissante (notes les plus récentes en premier)."""
        self.cursor.execute('SELECT * FROM notes ORDER BY date DESC')
        return self.cursor.fetchall()

    def get_notes_by_date(self, date):
        """Récupère les notes pour une date spécifique."""
        self.cursor.execute('SELECT * FROM notes WHERE date = ? ORDER BY importance ASC', (date,))
        return self.cursor.fetchall()

    def delete_note(self, note_id):
        """Supprime une note par son ID."""
        self.cursor.execute('DELETE FROM notes WHERE id = ?', (note_id,))
        self.conn.commit()

    def update_note(self, note_id, titre, description, importance):
        """Met à jour une note existante."""
        self.cursor.execute('''
        UPDATE notes
        SET titre = ?, description = ?, importance = ?
        WHERE id = ?
        ''', (titre, description, importance, note_id))
        self.conn.commit()

    def close(self):
        """Ferme la connexion à la base de données."""
        self.conn.close()
