import sqlite3

# Connexion à la base de données
conn = sqlite3.connect('ma_base.db')
cursor = conn.cursor()

# Vider la table (supprimer toutes les lignes)
cursor.execute("DELETE FROM nom_table;")

# Valider les changements
conn.commit()

# Fermer la connexion
conn.close()