"""
File: gui.py
Description: [Brief description of what this script does]
"""

# Third Party Libraries
import pandas as pd
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow

# Local Libraries
from MplTools import *
from QtWidgets import *

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setGeometry(1500,500,720,360)
        self.setWindowTitle("Main Window")
        self.initUI()
        self.data = None
    
    def initUI(self):
        # Create Central Widget - Main Container for all widgets within the Main Window
        centralWidget = makeCustomWidget(self)
        self.mainLayout = makeLayout("vertical")

        # Main Window Settings
        self.setCentralWidget(centralWidget)
        self.setMenuBar(makeMenuBar(self)) # Create Menu toolbar

        centralWidget.setLayout(self.mainLayout)

        # Create Widgets
        self.figure = None
        self.canvas = None
        self.searchBox = makeSearchBox(self, self.updateSelectionBox)
        self.selectedFileLabel = makeLabel(self)
        self.selectionBox = makeComboBox(self)
        self.plotButton = makeButton(self, "Plot Data", self.plot)
        self.table = makeTable(self)
        
        # Set certain widgets to hidden
        self.table.hide()
        self.searchBox.hide()
        self.selectionBox.hide()
        self.selectedFileLabel.hide()
        self.plotButton.hide()

        # Search Bar Layout
        self.searchLayout = makeLayout("horizontal")
        self.searchLayout.addWidget(self.searchBox)
        self.searchLayout.addWidget(self.plotButton)
 
        # Main Layout Order
        self.mainLayout.addLayout(self.searchLayout)
        self.mainLayout.addWidget(self.selectedFileLabel)
        self.mainLayout.addWidget(self.selectionBox)
        self.mainLayout.addWidget(self.table)

    # Callback methods
    def loadCsv(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if file_name:
            self.selectedFileLabel.setText(f'Selected file: {file_name}')
            self.data = pd.read_csv(file_name)
            self.selectionItems = self.data.keys()
            self.selectionBox.addItems(self.selectionItems)
            self.selectionBox.currentTextChanged.connect(self.updateTable)
            self.table.show()
            self.searchBox.show()
            self.selectionBox.show()
            self.selectedFileLabel.show()
            self.plotButton.show()
            self.update()

    def plot(self):
        selected_option = self.selectionBox.currentText()

        if self.canvas is None:  # Create canvas only once
            self.figure = makeFigure(6, 4)  # Create a new Figure object
            self.canvas = makeFigureCanvas(self, self.figure)
            self.toolbar = makeNavigationToolBar(self, self.canvas)
            self.plotWidget = PlotWidget(self, self.canvas, self.toolbar)
            self.ax = self.figure.add_subplot(111)  # Create subplot
                
            self.dockablePlot = makeDockablePlot(self, "Plot View")
            self.dockablePlot.setWidget(self.plotWidget)
            self.addDockWidget(Qt.RightDockWidgetArea, self.dockablePlot)  # Default position

        self.ax.clear()  # Clear previous plots before drawing a new one

        df = self.data[selected_option]
        try:
            self.ax.plot(df)
        except TypeError:
            print(f"Cannot plot {selected_option}")

        self.ax.set_title("Data Plot")
        self.canvas.draw()  # Refresh canvas with new plot

    def updateSelectionBox(self):
        searchText = self.searchBox.text().lower() # Get the text from the search box
        filtered_items = [item for item in self.selectionItems if searchText in item.lower()]
        
        # Clear and update the ComboBox
        self.selectionBox.clear()
        self.selectionBox.addItems(filtered_items)

    def updateTable(self):
        selectedColumn = self.selectionBox.currentText()

        if not selectedColumn:
            return
        
        self.table.clearContents()  # Clear previous data
        df = self.data[[selectedColumn]]

        self.table.setRowCount(df.shape[0])
        self.table.setColumnCount(len(df.keys()))
        self.table.setHorizontalHeaderLabels([selectedColumn])

        # Faster way to populate the table
        for row, values in enumerate(df.values.tolist()):
            for col, value in enumerate(values):
                self.table.setItem(row, col, makeTableWidgetItem(str(value)))

    def update(self):
        self.updateTable()
        self.selectedFileLabel.adjustSize()