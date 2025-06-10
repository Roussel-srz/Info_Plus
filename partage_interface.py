import os
import requests
import base64
import json
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QListWidget, QPushButton,
    QFileDialog, QMessageBox, QLabel, QProgressBar
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from config import GITHUB_TOKEN, REPO_OWNER, REPO_NAME

class PartageWorker(QThread):
    progress_updated = pyqtSignal(int)
    operation_completed = pyqtSignal(bool, str)

    def __init__(self, operation, *args):
        super().__init__()
        self.operation = operation
        self.args = args
        self.MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB limite

    def run(self):
        try:
            if self.operation == "download":
                self._download_file(*self.args)
            elif self.operation == "upload":
                self._upload_file(*self.args)
            elif self.operation == "delete":
                self._delete_file(*self.args)
        except Exception as e:
            self.operation_completed.emit(False, str(e))

    def _download_file(self, file_name, download_path):
        try:
            self.progress_updated.emit(5)
            
            # Configuration des headers
            headers = {
                "Authorization": f"token {GITHUB_TOKEN}",
                "Accept": "application/vnd.github.v3.raw"
            }
            
            # URL de téléchargement direct (raw)
            download_url = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/main/Partage/{file_name}"
            
            # Téléchargement avec stream
            self.progress_updated.emit(10)
            with requests.get(download_url, headers=headers, stream=True, timeout=30) as r:
                r.raise_for_status()
                
                # Vérification de la taille
                total_size = int(r.headers.get('content-length', 0))
                if total_size > self.MAX_FILE_SIZE:
                    raise ValueError(f"Fichier trop volumineux ({total_size//(1024*1024)}MB > {self.MAX_FILE_SIZE//(1024*1024)}MB max)")
                
                # Écriture par chunks avec progression
                self.progress_updated.emit(20)
                downloaded = 0
                with open(download_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):  # 8KB chunks
                        if self.isInterruptionRequested():
                            raise Exception("Téléchargement annulé")
                            
                        if chunk:  # filter out keep-alive chunks
                            f.write(chunk)
                            downloaded += len(chunk)
                            progress = 20 + int(70 * (downloaded / total_size))
                            self.progress_updated.emit(progress)
            
            self.progress_updated.emit(95)
            # Vérification finale
            if os.path.getsize(download_path) == total_size:
                self.operation_completed.emit(True, f"Téléchargement réussi: {file_name} ({total_size//1024} KB)")
            else:
                raise Exception("Téléchargement incomplet")
                
        except requests.exceptions.RequestException as e:
            self.operation_completed.emit(False, f"Erreur réseau: {str(e)}")
        except Exception as e:
            # Nettoyage en cas d'erreur
            if os.path.exists(download_path):
                os.remove(download_path)
            self.operation_completed.emit(False, f"Erreur de téléchargement: {str(e)}")

    def _upload_file(self, file_path, file_name):
        try:
            self.progress_updated.emit(5)
            
            # Vérification de la taille
            file_size = os.path.getsize(file_path)
            if file_size > self.MAX_FILE_SIZE:
                raise ValueError(f"Fichier trop volumineux ({file_size//(1024*1024)}MB > {self.MAX_FILE_SIZE//(1024*1024)}MB max)")
            
            # 1. Vérifier si le fichier existe déjà
            self.progress_updated.emit(10)
            url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/Partage/{file_name}"
            headers = {
                "Authorization": f"token {GITHUB_TOKEN}",
                "Accept": "application/vnd.github.v3+json"
            }
            
            sha = None
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                sha = response.json().get('sha')
            
            # 2. Lecture par blocs avec progression
            self.progress_updated.emit(20)
            chunks = []
            total_read = 0
            with open(file_path, 'rb') as f:
                while True:
                    if self.isInterruptionRequested():
                        raise Exception("Upload annulé")
                        
                    chunk = f.read(1024*1024)  # 1MB chunks
                    if not chunk:
                        break
                    chunks.append(chunk)
                    total_read += len(chunk)
                    progress = 20 + int(40 * (total_read / file_size))
                    self.progress_updated.emit(progress)
            
            # 3. Encodage base64
            self.progress_updated.emit(65)
            content = b''.join(chunks)
            encoded_content = base64.b64encode(content).decode('utf-8')
            
            # 4. Préparation requête
            self.progress_updated.emit(75)
            data = {
                "message": f"Ajout du fichier {file_name}",
                "content": encoded_content
            }
            if sha:
                data["sha"] = sha
            
            # 5. Envoi
            self.progress_updated.emit(85)
            response = requests.put(url, headers=headers, json=data, timeout=60)
            response.raise_for_status()
            
            self.progress_updated.emit(100)
            self.operation_completed.emit(True, f"Fichier uploadé: {file_name} ({file_size//1024} KB)")
            
        except requests.exceptions.RequestException as e:
            self.operation_completed.emit(False, f"Erreur réseau: {str(e)}")
        except Exception as e:
            self.operation_completed.emit(False, f"Erreur d'upload: {str(e)}")


    def _delete_file(self, file_name):
        try:
            self.progress_updated.emit(10)
            
            # 1. Récupérer le SHA du fichier
            url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/Partage/{file_name}"
            headers = {
                "Authorization": f"token {GITHUB_TOKEN}",
                "Accept": "application/vnd.github.v3+json"
            }
            
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                raise Exception("Fichier non trouvé sur GitHub")
            
            sha = response.json().get('sha')
            if not sha:
                raise Exception("Impossible de récupérer le SHA du fichier")
            
            self.progress_updated.emit(50)
            
            # 2. Envoyer la requête de suppression
            data = {
                "message": f"Suppression du fichier {file_name}",
                "sha": sha
            }
            
            response = requests.delete(url, headers=headers, json=data)
            response.raise_for_status()
            
            self.progress_updated.emit(100)
            self.operation_completed.emit(True, f"Fichier supprimé: {file_name}")
            
        except requests.exceptions.RequestException as e:
            self.operation_completed.emit(False, f"Erreur réseau: {str(e)}")
        except Exception as e:
            self.operation_completed.emit(False, f"Erreur de suppression: {str(e)}")


class PartageDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Partage de fichiers")
        self.setMinimumSize(700, 500)
        
        self.local_dir = "Partage"
        os.makedirs(self.local_dir, exist_ok=True)
        self.current_worker = None
        
        self.init_ui()
        self.load_github_files()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Titre
        title = QLabel("Gestion des fichiers partagés")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-weight: bold; font-size: 16px;")
        layout.addWidget(title)
            
        # Liste des fichiers GitHub
        self.github_list = QListWidget()
        self.github_list.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        layout.addWidget(QLabel("Fichiers disponibles sur GitHub:"))
        layout.addWidget(self.github_list)
        
        # Boutons
        btn_layout = QHBoxLayout()
        
        self.download_btn = QPushButton("Télécharger")
        self.download_btn.clicked.connect(self.download_file)
        btn_layout.addWidget(self.download_btn)
        
        self.upload_btn = QPushButton("Importer")
        self.upload_btn.clicked.connect(self.upload_file)
        btn_layout.addWidget(self.upload_btn)
        
        self.delete_btn = QPushButton("Supprimer")
        self.delete_btn.clicked.connect(self.delete_file)
        btn_layout.addWidget(self.delete_btn)
        
        self.refresh_btn = QPushButton("Actualiser")
        self.refresh_btn.clicked.connect(self.load_github_files)
        btn_layout.addWidget(self.refresh_btn)
        
        self.download_btn.setFixedHeight(30) 
        self.upload_btn.setFixedHeight(30) 
        self.delete_btn.setFixedHeight(30)
        self.refresh_btn.setFixedHeight(30) 
        
        layout.addLayout(btn_layout)
        
        # Barre de progression
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        layout.addWidget(self.progress)
        
        # Status label
        self.status_label = QLabel()
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)
      

    def load_github_files(self):
        if not all([GITHUB_TOKEN, REPO_OWNER, REPO_NAME]):
            QMessageBox.warning(self, "Configuration manquante", 
                              "Veuillez configurer les informations GitHub dans config.py")
            return
            
        try:
            self.status_label.setText("Chargement de la liste des fichiers...")
            url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/Partage"
            headers = {"Authorization": f"token {GITHUB_TOKEN}"}
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            files = [item['name'] for item in response.json() if item['type'] == 'file']
            
            self.github_list.clear()
            self.github_list.addItems(files)
            self.status_label.setText(f"{len(files)} fichiers disponibles")
            
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible de charger les fichiers: {str(e)}")
            self.status_label.setText("Erreur de chargement")
    
    def download_file(self):
        selected_items = self.github_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Aucune sélection", "Veuillez sélectionner un fichier à télécharger")
            return
            
        file_name = selected_items[0].text()
        save_path = os.path.join(self.local_dir, file_name)
        
        # Vérifier si le fichier existe déjà localement
        if os.path.exists(save_path):
            reply = QMessageBox.question(
                self,
                "Fichier existant",
                f"Le fichier {file_name} existe déjà. Voulez-vous le remplacer?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.No:
                return
        
        # Lancer le téléchargement
        self.progress.setVisible(True)
        self.progress.setValue(0)
        self.set_buttons_enabled(False)
        self.status_label.setText(f"Téléchargement de {file_name}...")
        
        self.current_worker = PartageWorker("download", file_name, save_path)
        self.current_worker.progress_updated.connect(self.progress.setValue)
        self.current_worker.operation_completed.connect(self.on_operation_complete)
        self.current_worker.start()
    
    def upload_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Sélectionner un fichier à importer",
            "", 
            "Tous les fichiers (*)"
        )
        
        if not file_path:
            return
            
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        
        # Vérifier la taille
        if file_size > 100 * 1024 * 1024:  # 100MB
            QMessageBox.warning(self, "Fichier trop volumineux", 
                              "Les fichiers de plus de 100MB ne sont pas supportés")
            return
        
        # Lancer l'upload
        self.progress.setVisible(True)
        self.progress.setValue(0)
        self.set_buttons_enabled(False)
        self.status_label.setText(f"Envoi de {file_name} ({file_size//1024} KB)...")
        
        self.current_worker = PartageWorker("upload", file_path, file_name)
        self.current_worker.progress_updated.connect(self.progress.setValue)
        self.current_worker.operation_completed.connect(self.on_operation_complete)
        self.current_worker.start()
  
     
    def delete_file(self):
        selected_items = self.github_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Aucune sélection", "Veuillez sélectionner un fichier à supprimer")
            return
            
        file_name = selected_items[0].text()
        
        # Confirmation de suppression
        reply = QMessageBox.question(
            self,
            "Confirmation",
            f"Êtes-vous sûr de vouloir supprimer {file_name} du dépôt GitHub?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.No:
            return
        
        # Lancer la suppression
        self.progress.setVisible(True)
        self.progress.setValue(0)
        self.set_buttons_enabled(False)
        self.status_label.setText(f"Suppression de {file_name}...")
        
        self.current_worker = PartageWorker("delete", file_name)
        self.current_worker.progress_updated.connect(self.progress.setValue)
        self.current_worker.operation_completed.connect(self.on_operation_complete)
        self.current_worker.start()
    
    def on_operation_complete(self, success, message):
        self.progress.setVisible(False)
        self.set_buttons_enabled(True)
        self.status_label.setText(message)
        
        if success:
            QMessageBox.information(self, "Succès", message)
            self.load_github_files()  # Rafraîchir la liste
        else:
            QMessageBox.critical(self, "Erreur", message)
    
    def set_buttons_enabled(self, enabled):
        self.download_btn.setEnabled(enabled)
        self.upload_btn.setEnabled(enabled)
        self.delete_btn.setEnabled(enabled)
        self.refresh_btn.setEnabled(enabled)
    
    def closeEvent(self, event):
        """Arrêter les opérations en cours lors de la fermeture"""
        if self.current_worker and self.current_worker.isRunning():
            self.current_worker.requestInterruption()
            self.current_worker.wait()
        event.accept()