import os

# Chemins des fichiers
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Logo
LOGO_PATH = os.path.join(BASE_DIR, "logo.png")  # Chemin absolu vers le logo
BASE_DE_DONNEE = "data_base.db"

# Paramètres de l'App
APP_NAME = "Info Plus"
# DEBUG = True