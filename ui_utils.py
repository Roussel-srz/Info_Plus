# ui_utils.py
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QFont
from PyQt6.QtCore import QRect, Qt

def create_button(text, x, y, width, height, parent=None, font_size=12, object_name=None):
    button = QtWidgets.QPushButton(text, parent=parent)
    button.setGeometry(QRect(x, y, width, height))
    
    font = QFont()
    font.setPointSize(font_size)
    button.setFont(font)

    if object_name:
        button.setObjectName(object_name)
    
    return button

def create_label(text, x, y, width, height, parent=None, font_size=14, font_family="Arial", bold=True, align_center=True):
    label = QtWidgets.QLabel(text, parent=parent)
    label.setGeometry(QRect(x, y, width, height))
    font = QFont()
    font.setFamily(font_family)
    font.setPointSize(font_size)
    font.setBold(bold)
    label.setFont(font)

    if align_center:
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    return label

def titre(text, x=140, y=40, width=550, height=51, parent=None, font_size=30, font_family="Arial Black", bold=True, align_center=False):
    label = QtWidgets.QLabel(text, parent=parent)
    label.setGeometry(QRect(x, y, width, height))
    font = QFont()
    font.setFamily(font_family)
    font.setPointSize(font_size)
    font.setBold(bold)
    label.setFont(font)

    if align_center:
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    return label

def create_table(x, y, width, height, parent=None, row_count=0, column_count=0, headers=None, object_name=None):
    """
    Crée un QTableWidget avec les paramètres spécifiés.
    
    Args:
        x, y, width, height: Position et dimensions du tableau
        parent: Widget parent
        row_count: Nombre initial de lignes
        column_count: Nombre initial de colonnes
        headers: Liste des en-têtes de colonnes
        object_name: Nom d'objet pour le style CSS
    """
    table = QtWidgets.QTableWidget(parent)
    table.setGeometry(QRect(x, y, width, height))
    
    # Configurer le nombre de lignes et colonnes
    table.setRowCount(row_count)
    table.setColumnCount(column_count)
    
    # Définir les en-têtes si fournis
    if headers:
        table.setHorizontalHeaderLabels(headers)
    
    # Options d'affichage
    table.setAlternatingRowColors(False)
    table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
    table.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
    table.horizontalHeader().setStretchLastSection(True)
    table.verticalHeader().setVisible(False)
    
    if object_name:
        table.setObjectName(object_name)
    
    return table
def create_spinbox(x, y, width,parent=None, min_val=0, max_val=1000000, suffix=""):
    sb = QtWidgets.QSpinBox(parent=parent)
    sb.setGeometry(QtCore.QRect(x, y, width, 31))
    sb.setMinimum(min_val)
    sb.setMaximum(max_val)
    sb.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    sb.setSuffix(suffix)
    return sb