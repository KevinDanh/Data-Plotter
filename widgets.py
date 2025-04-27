from PyQt5.QtWidgets import QComboBox, QTableWidget, QPushButton, QSizePolicy, QHeaderView, QLabel, QLineEdit

def makeButton(parent, buttonText, callback=None):
    button = QPushButton(buttonText, parent)
    button.setText(buttonText)
    button.clicked.connect(callback)
    return button

def makeTable(parent):
    table = QTableWidget(parent)
    table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
    return table

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