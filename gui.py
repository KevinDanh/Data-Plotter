import sys
import pandas as pd
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QVBoxLayout, QWidget, QTableWidgetItem
from widgets import makeButton, makeTable, makeComboBox, makeLabel, makeSearchBox

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(1500,500,720,360)
        self.setWindowTitle("Main Window")
        self.initUI()
        self.data = None
    
    def initUI(self):
        centralWidget = QWidget() # Central Widget - Main Container for all widgets within the gui
        self.setCentralWidget(centralWidget) # Sets centralWidget as the main widget for our window

        # Layout
        layout = QVBoxLayout() # Organizes Widgets Vertically
        centralWidget.setLayout(layout)

        # Create Widgets
        self.table = makeTable(self)
        self.table.hide()
        self.searchBox = makeSearchBox(self, self.updateSelectionBox)
        self.searchBox.hide()
        self.selectionBox = makeComboBox(self)
        self.selectionBox.hide()
        self.selectedFileLabel = makeLabel(self)
        self.selectedFileLabel.hide()
        self.importButton = makeButton(self, "Import CSV", self.loadCsv)
        self.plotButton = makeButton(self, "Plot Data", self.plot)
        self.exitButton = makeButton(self, "Exit", self.exit)
        self.plotButton.hide()

        # Add Widgets to the layout
        # Order here changes how the widgets are stacked
        layout.addWidget(self.importButton)
        layout.addWidget(self.plotButton)
        layout.addWidget(self.searchBox)
        layout.addWidget(self.selectedFileLabel)
        layout.addWidget(self.selectionBox)
        layout.addWidget(self.table)
        layout.addWidget(self.exitButton)

    # Callback methods
    def loadCsv(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if file_name:
            self.selectedFileLabel.setText(f'Selected file: {file_name}')
            self.data = pd.read_csv(file_name)
            self.selectionBox.addItems(["All"])
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
        if selected_option == "All":
            for key in self.data.keys():
                plt.figure()
                try:
                    plt.plot(self.data[key])
                except TypeError:
                    print(f"Cannot plot: {key}")
        else:
            df = self.data[selected_option]
            plt.plot(df)
        plt.show()

    def updateSelectionBox(self):
        searchText = self.searchBox.text().lower() # Get the text from the search box
        filtered_items = [item for item in self.selectionItems if searchText in item.lower()]
        
        # Clear and update the ComboBox
        self.selectionBox.clear()
        self.selectionBox.addItems(filtered_items)

    def updateTable(self):
        selected_column = self.selectionBox.currentText()
        if selected_column:
            if selected_column == "All":
                self.table.setRowCount(self.data.shape[0])
                self.table.setColumnCount(len(self.data.keys()))
                self.table.setHorizontalHeaderLabels(self.data.keys())

                for row in range(self.data.shape[0]):
                    for col in range(self.data.shape[1]):
                        self.table.setItem(row, col, QTableWidgetItem(str(self.data.iloc[row, col])))
            else: 
                df = self.data[[selected_column]]  # Select column
                self.table.setRowCount(df.shape[0])
                self.table.setColumnCount(len(df.keys()))
                self.table.setHorizontalHeaderLabels([selected_column])

                for row in range(df.shape[0]):
                    self.table.setItem(row, 0, QTableWidgetItem(str(df.iloc[row, 0])))

    def update(self):
        self.updateTable()
        self.selectedFileLabel.adjustSize()
    
    def exit(self):
        plt.close('all')
        sys.exit()
    
def main():
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()