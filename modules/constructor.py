from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QScrollArea, QSizePolicy, QMenu
from PyQt5.QtCore import Qt

from PyQt5.QtCore import pyqtSlot
from functools import partial

class Pin(QWidget):
    def __init__(self, type, number, parent):
        QWidget.__init__(self, parent)
        self.holder = QHBoxLayout(self)
        self.setAcceptDrops(True)
        # Номер
        # Параметры
        # Тип
        self.number = number
        self.params = []
        self.type = type

        types = {'cond':self.createCondition, 'loop':self.createLoop, 'run':self.createExecute}
        types[type]()
     
    def createCondition(self):
        self.num = QLabel(str(self.number), self)
        self.label = QLabel('\tЕсли', self)
        self.input = QLineEdit('', self)
        self.labelEqual = QLabel('Равно', self)
        self.inputEqual = QLineEdit('', self)
        self.labelThen = QLabel('То', self)
        self.inputThen = QLineEdit('', self)
        self.labelElse = QLabel('Иначе', self)
        self.inputElse = QLineEdit('', self)

        self.holder.addWidget(self.num)
        self.holder.addWidget(self.label)
        self.holder.addWidget(self.input)
        self.holder.addWidget(self.labelEqual)
        self.holder.addWidget(self.inputEqual)
        self.holder.addWidget(self.labelThen)
        self.holder.addWidget(self.inputThen)
        self.holder.addWidget(self.labelElse)
        self.holder.addWidget(self.inputElse)

        self.params = [self.num, self.input, self.inputEqual, self.inputThen, self.inputElse]

    def createLoop(self):
        self.num = QLabel(str(self.number), self)
        self.label = QLabel('\tОт', self)
        self.input = QLineEdit('', self)
        self.labelTo = QLabel('До', self)
        self.inputTo = QLineEdit('', self)
        self.labelThen = QLabel('Выполнить', self)
        self.inputThen = QLineEdit('', self)
        self.labelElse = QLabel('Иначе', self)
        self.inputElse = QLineEdit('', self)

        self.holder.addWidget(self.num)
        self.holder.addWidget(self.label)
        self.holder.addWidget(self.input)
        self.holder.addWidget(self.labelTo)
        self.holder.addWidget(self.inputTo)
        self.holder.addWidget(self.labelThen)
        self.holder.addWidget(self.inputThen)
        self.holder.addWidget(self.labelElse)
        self.holder.addWidget(self.inputElse)

        self.params = [self.num, self.input, self.inputTo, self.inputThen,
                      self.inputElse]
        
    def createExecute(self):
        self.num = QLabel(str(self.number), self)
        self.label = QLabel('\tВыполнить', self)
        self.input = QLineEdit('', self)

        self.holder.addWidget(self.num)
        self.holder.addWidget(self.label)
        self.holder.addWidget(self.input)

        self.params = [self.num, self.input]

    #def mousePressEvent(self, e):
    #    QWidget.mousePressEvent(self, e)

    #    if e.button() == Qt.RightButton:
    #        print('Pin menu call')

    def contextMenuEvent(self, event):
        contextMenu = QMenu(self)
        deleteAction = contextMenu.addAction("Удалить")
        #moveAction = contextMenu.addAction("Переместить")

        action = contextMenu.exec_(self.mapToGlobal(event.pos()))
        if action == deleteAction:
            self.setParent(None)
        #elif action == moveAction:
        #    self.parent().

class Constructor(QWidget):
    def __init__(self, parent=None):
        super(Constructor, self).__init__(parent)
        self.setAcceptDrops(True)

        scroll = QScrollArea()
        self.main = QWidget()
        pins = QWidget()
        
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

        # Buttons from drag n drop
        button = QPushButton('Условие', self)
        button.type = 'cond'
        button.clicked.connect(partial(self.on_click, button.type))
        pinsLayout.addWidget(button)
        button = QPushButton('Цикл', self)
        button.type = 'loop'
        button.clicked.connect(partial(self.on_click, button.type))
        pinsLayout.addWidget(button)
        button = QPushButton('Выполнение', self)
        button.type = 'run'
        button.clicked.connect(partial(self.on_click, button.type))
        pinsLayout.addWidget(button)
        button = QPushButton('Очистить', self)
        button.type = 'clear'
        button.clicked.connect(partial(self.on_click, button.type))
        pinsLayout.addWidget(button)
        
        holderLayout.addWidget(pins)
        holderLayout.addWidget(scroll)

        print('Constructor created')

    def getScenario(self):
        res_orig = self.main.findChildren(Pin)
        if len(res_orig) > 0:
            res = [item.params for item in res_orig]
            res = [[item.text() for item in res[i]] for i in range(len(res))]
            for i in range(len(res)):
                res[i].append(res_orig[i].type)
            return res

    @pyqtSlot()
    @pyqtSlot(str)
    def on_click(self, param=None):
        def createCondition():
            print('CREATING CONDITION')
            #self.mainLayout.addWidget(Pin('My name is jeff', self))
            self.mainLayout.addWidget(Pin('cond', len(self.main.findChildren(Pin)) + 1, self))
        def createLoop():
            print('CREATING LOOP')
            #self.mainLayout.addWidget(Pin('My name is jeff', self))
            self.mainLayout.addWidget(Pin('loop', len(self.main.findChildren(Pin)) + 1, self))
        def createExecute():
            print('CREATING EXEC')
            #self.mainLayout.addWidget(Pin('My name is jeff', self))
            self.mainLayout.addWidget(Pin('run', len(self.main.findChildren(Pin)) + 1, self))
        def clear():
            res = []
            for i in reversed(range(self.mainLayout.count())):
                res.append(self.mainLayout.takeAt(i).widget())
            print(res)
            for item in res: 
                if item is not None:
                    print(item, type(item))
                    item.setParent(None)
                print('cleared')
        
        params = {'cond':createCondition, 'loop':createLoop, 'run':createExecute, 'clear':clear}

        params[param]()
