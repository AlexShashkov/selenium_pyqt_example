from PyQt5.QtWidgets import QDialog, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QScrollArea
from PyQt5.QtCore import Qt

from PyQt5.QtCore import pyqtSlot
from functools import partial

class Input(QWidget):
    def __init__(self, parent, type, name, inp=''):
        QWidget.__init__(self, parent)
        self.holder = QHBoxLayout(self)
        self.params = []
        self.type = type
        self.name = name
        self.inp = inp

        types = {'string':self.createString}
        types[type]()

    def createString(self):
        self.label = QLabel(self.name, self)
        self.input = QLineEdit(self.inp, self)
        self.deleteButton = QPushButton('удалить', self)
        self.deleteButton.clicked.connect(self.delete)

        self.holder.addWidget(self.label)
        self.holder.addWidget(self.input)
        self.holder.addWidget(self.deleteButton)

        self.params = [self.input]

    def delete(self):
        self.setParent(None)


class Dialog(QDialog):
    def __init__(self, parent, name, input):
        super(Dialog, self).__init__(parent)
        self.setWindowTitle("Параметры таблицы")
        self.setWindowModality(Qt.ApplicationModal)
        
        self.name = name
        self.input = input
        self.main = QWidget()
        pins = QWidget()
        scroll = QScrollArea()
        
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        holderLayout = QVBoxLayout(self)
        pinsLayout = QHBoxLayout(self)
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.addStretch()

        pins.setLayout(pinsLayout)
        self.main.setLayout(self.mainLayout)

        scroll.setWidgetResizable(True)
        scroll.setWidget(self.main)
        self.pins = 1

		# Buttons
        button = QPushButton('Готово', self)
        button.clicked.connect(self.okDone) #self.parent().test
        pinsLayout.addWidget(button)

        button = QPushButton(name, self)
        button.clicked.connect(partial(self.create, self.input, param='string', input=''))
        pinsLayout.addWidget(button)

        holderLayout.addWidget(pins)
        holderLayout.addWidget(scroll)

        self.setLayout(holderLayout)

        #Граб из таблицы и добавление
        items = [self.parent().inTable.table.horizontalHeaderItem(i).text() for i in range(self.parent().inTable.table.columnCount())]
        for i in range(len(items)): self.create(self.input, 'string', input=items[i])  

        #self.show()

    @pyqtSlot()
    @pyqtSlot(str)
    def create(self, name, param=None, input=''):
	    def createInput():
		    print('CREATING MODAL INPUT')
		    #self.mainLayout.addWidget(Pin('My name is jeff', self))
		    self.mainLayout.addWidget(Input(self, 'string', name, input))

	    params = {'string':createInput}
	    params[param]()

    def okDone(self, param=None):
        res_orig = self.main.findChildren(Input)
        res = [item.params for item in res_orig]
        res = [item[0].text() for item in res]
        print(res)
        self.parent().inTable.setHeader(res)
        self.close()