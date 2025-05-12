"""
File: QtWidgets.py
Description: Wrapper for PyQt5 Widgets
"""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QSizePolicy, 
    QVBoxLayout, QHBoxLayout, QGridLayout,
    QWidget, 
    QComboBox, QTableWidget, QTableWidgetItem, 
    QHeaderView, QPushButton,QLabel, 
    QLineEdit, QDockWidget, QMenuBar,
    QAction, QFileDialog
)

class PlotWidget(QWidget):
    def __init__(self, parent=None, canvas=None, toolbar=None):
        super().__init__(parent)
        
        self.canvas = canvas
        self.toolbar = toolbar

        # Layout to combine toolbar & canvas
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)  # Toolbar at the top
        layout.addWidget(self.canvas)  # Canvas below it
        self.setLayout(layout)

def makeCustomWidget(parent):
    return QWidget(parent)

def makeLayout(layout_type="vertical"):
    # Select layout type
    if layout_type == "vertical":
        layout = QVBoxLayout()
    elif layout_type == "horizontal":
        layout = QHBoxLayout()
    elif layout_type == "grid":
        layout = QGridLayout()
    else:
        raise ValueError("Invalid layout type. Choose 'vertical', 'horizontal', or 'grid'.")
    return layout

def makeButton(parent, buttonText, callback=None):
    button = QPushButton(buttonText, parent)
    button.setMaximumWidth(150)
    button.setText(buttonText)
    button.clicked.connect(callback)
    return button

def makeTable(parent):
    table = QTableWidget(parent)
    table.setMinimumHeight(250)
    table.setMaximumHeight(1000)
    table.setMaximumWidth(1000)
    table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
    table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
    return table

def makeTableWidgetItem(string):
    return QTableWidgetItem(string)

def makeComboBox(parent):
    return QComboBox(parent)

def makeLabel(parent, text="", font_size=12):
    label = QLabel(parent)
    label.setText(text)
    label.setStyleSheet(f"font-size: {font_size}px;")
    return label

def makeSearchBox(parent, callback=None, placeholder="Type to search..."):
    searchBox = QLineEdit(parent)
    searchBox.setPlaceholderText(placeholder)
    searchBox.textChanged.connect(callback)
    return searchBox

def makeDockablePlot(parent, dockName="Unnamed"):
    dock = QDockWidget(dockName, parent)
    dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea | Qt.TopDockWidgetArea | Qt.BottomDockWidgetArea)
    dock.setFloating(False) # If this is set to True docking becomes unavailable
    dock.setMinimumWidth(350)
    dock.setMinimumHeight(350)
    dock.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    return dock 

def makeFileDialogOptions():
    return QFileDialog.Options()

def makeMenuBar(parent):
    menu_bar = QMenuBar(parent)

    fileMenu = menu_bar.addMenu("File")
    openAction = QAction("Import CSV", parent)
    openAction.triggered.connect(parent.loadCsv)
    fileMenu.addAction(openAction)

    exitAction = QAction("Exit", parent)
    exitAction.triggered.connect(parent.close)
    fileMenu.addAction(exitAction)

    return menu_bar