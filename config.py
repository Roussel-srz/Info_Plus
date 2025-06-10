import os

# Chemins des fichiers
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Logo
LOGO_PATH = os.path.join(BASE_DIR, "logo.png")  # Chemin absolu vers le logo
BASE_DE_DONNEE = "data_base.db"

# Paramètres de l'App
APP_NAME = "Info Plus"

# Configuration GitHub (à remplir par l'utilisateur)
REPO_OWNER = "Roussel-srz"  # Votre nom d'utilisateur GitHub
REPO_NAME = "Info_Plus"     # Nom de votre dépôt
GITHUB_TOKEN = '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'
