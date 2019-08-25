from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import QSize, Qt
import csv

class Table(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        
        self.grid = QVBoxLayout()
        self.setLayout(self.grid)

        self.table = QTableWidget(self)
        self.grid.addWidget(self.table)

    def editCell(self, value, row, column):
        print('Editing cell {}{}'.format(row, column))
        item = QTableWidgetItem(str(value)) 
        self.table.setItem(row, column, item)

    def setHeader(self, row):
        self.table.setColumnCount(len(row))
        self.table.setHorizontalHeaderLabels(row)

    def addRow(self):
        count = self.table.rowCount() + 1
        self.table.setRowCount(count)

    def clear(self):
        self.table.setRowCount(0)

    def writeCsv(self, name):
        def write(row, name, mode_in):
            with open(name, mode=mode_in, newline='', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(row)

        cols = self.table.columnCount()
        try:
            items = [self.table.horizontalHeaderItem(i).text() for i in range(self.table.columnCount())]
            write(items, name, 'w')
            
            for i in range(self.table.rowCount):
                print(self.table.columnCount())
                items = [self.table.item(i, j).text() if self.table.item(i, j) is not None else ' ' for j in range(self.table.columnCount())]
                test = [(i, j) for j in range(self.table.columnCount())]
                print(items)
                print(test)
                write(items, name, 'a+')
        except Exception as e:
            print('While saving', e)



