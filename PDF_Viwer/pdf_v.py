import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QFileDialog, QToolBar, QStatusBar, QMessageBox)
from PyQt6.QtPdf import QPdfDocument
from PyQt6.QtPdfWidgets import QPdfView
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
from PyQt6.QtCore import Qt, QStandardPaths
from PyQt6.QtGui import QAction, QIcon
from PyQt6 import QtGui


class PDFViewer(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Visualiseur PDF")
        self.setGeometry(100, 100, 800, 600)
        # self.setWindowTitle("PDF_viwer")
        self.setWindowIcon(QtGui.QIcon("./logo.png"))
        
        # Créer le widget central et le layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Créer le visualiseur PDF avec le parent
        self.pdf_view = QPdfView(central_widget)
        layout.addWidget(self.pdf_view)
        
        # Document PDF avec le parent
        self.pdf_doc = QPdfDocument(self)
        self.pdf_view.setDocument(self.pdf_doc)
        
        # Créer la barre d'outils
        self.create_toolbar()
        
        # Créer la barre de statut
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
    def create_toolbar(self):
        toolbar = QToolBar("Barre d'outils principale")
        self.addToolBar(toolbar)
        
        # Action pour ouvrir un fichier
        open_action = QAction(QIcon.fromTheme("document-open"), "Ouvrir", self)
        open_action.triggered.connect(self.open_file)
        toolbar.addAction(open_action)
        
        # Action pour imprimer
        print_action = QAction(QIcon.fromTheme("document-print"), "Imprimer", self)
        print_action.triggered.connect(self.print_document)
        toolbar.addAction(print_action)
        
        # Action pour quitter
        quit_action = QAction(QIcon.fromTheme("application-exit"), "Quitter", self)
        quit_action.triggered.connect(self.close)
        toolbar.addAction(quit_action)
    
    def open_file(self):
        # Obtenir le dossier Documents par défaut
        docs_path = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DocumentsLocation)
        
        # Ouvrir la boîte de dialogue pour sélectionner un fichier PDF
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Ouvrir un fichier PDF", 
            docs_path, 
            "Fichiers PDF (*.pdf)"
        )
        
        if file_path:
            # Charger le document PDF
            self.pdf_doc.load(file_path)
            
            # Mettre à jour le titre de la fenêtre
            self.setWindowTitle(f"Visualiseur PDF - {file_path}")
            
            # Afficher un message dans la barre de statut
            self.status_bar.showMessage(f"Fichier chargé: {file_path}", 3000)
    
    def print_document(self):
        if self.pdf_doc.pageCount() == 0:
            QMessageBox.warning(self, "Avertissement", "Aucun document à imprimer.")
            return
        
        # Créer un objet QPrinter
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        
        # Configurer la boîte de dialogue d'impression
        print_dialog = QPrintDialog(printer, self)
        print_dialog.setOption(QPrintDialog.PrintDialogOption.PrintToFile)
        
        if print_dialog.exec() == QPrintDialog.DialogCode.Accepted:
            # Imprimer le document
            from PyQt6.QtGui import QPainter
            painter = QPainter()
            if painter.begin(printer):
                # Rendre chaque page du PDF
                for page in range(self.pdf_doc.pageCount()):
                    if page != 0:
                        printer.newPage()
                    
                    # Récupérer la taille de la page PDF
                    page_size = self.pdf_doc.pageSize(page)
                    
                    # Ajuster la taille pour l'impression
                    target_rect = printer.pageRect(QPrinter.Unit.DevicePixel)
                    source_rect = page_size.toRect()
                    
                    # Calculer le ratio de mise à l'échelle
                    x_scale = target_rect.width() / source_rect.width()
                    y_scale = target_rect.height() / source_rect.height()
                    scale = min(x_scale, y_scale)
                    
                    painter.save()
                    painter.translate(target_rect.center())
                    painter.scale(scale, scale)
                    painter.translate(-source_rect.width()/2, -source_rect.height()/2)
                    
                    # Rendre la page
                    self.pdf_doc.render(page, painter)
                    painter.restore()
                
                painter.end()
                
                self.status_bar.showMessage("Document envoyé à l'imprimante", 3000)
            else:
                QMessageBox.critical(self, "Erreur", "Impossible de démarrer l'impression.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Configurer le style par défaut
    try:
        with open("./style_dark.qss", "r") as file:
            app.setStyleSheet(file.read())
    except FileNotFoundError:
        print("Le fichier style.qss n'a pas été trouvé.")
    
    viewer = PDFViewer()
    viewer.show()
    
    sys.exit(app.exec())