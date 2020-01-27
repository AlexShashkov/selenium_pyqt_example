from PyQt5 import QtGui

from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QHBoxLayout, QLabel, QPlainTextEdit, QPushButton, QScrollArea, QSizePolicy, QMenu
from PyQt5.QtCore import Qt

from PyQt5.QtCore import pyqtSlot
from functools import partial


class TextEdit(QPlainTextEdit):
    '''
    Modified QPlainTextEdit
    '''
    def __init__(self, input, parent):
        QPlainTextEdit.__init__(self, parent)
        #self.setLineWrapMode(True)
        self.countOfRows = 1
        self.setPlainText(input)
        self.changeRows(1)

    def text(self):
        return self.toPlainText()

    def keyPressEvent(self, e):
        # Handles 'enter' key
        if e.key() == 16777220:
            self.countOfRows += 1
            self.changeRows(self.countOfRows)
            self.insertPlainText(e.text())
        elif e.key() == Qt.Key_Backspace:
            self.textCursor().deletePreviousChar()
        else:
            self.insertPlainText(e.text())

    def changeRows(self, num_rows):
        metrics = self.font()
        rowHeight = QtGui.QFontMetrics(metrics).lineSpacing()
        self.setFixedHeight(num_rows * rowHeight + 10)


class Pin(QWidget):
    '''
    Basic block
    '''
    def __init__(self, type, number, parent):
        QWidget.__init__(self, parent)

        # Var that stores everything
        self.holder = QHBoxLayout(self)
        # TODO - enable drops
        self.setAcceptDrops(True)
        self.number = number
        self.params = []
        self.type = type

        # type that will be created
        types = {'cond':self.createCondition, 'loop':self.createLoop, 'run':self.createExecute}
        types[type]()
     
    def createCondition(self):
        self.num = QLabel(str(self.number), self)
        self.label = QLabel('\tЕсли', self)
        self.input = TextEdit('', self)
        self.labelEqual = QLabel('Равно', self)
        self.inputEqual = TextEdit('', self)
        self.labelThen = QLabel('То', self)
        self.inputThen = TextEdit('', self)
        self.labelElse = QLabel('Иначе', self)
        self.inputElse = TextEdit('', self)

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
        self.input = TextEdit('', self)
        self.labelTo = QLabel('До', self)
        self.inputTo = TextEdit('', self)
        self.labelThen = QLabel('Выполнить', self)
        self.inputThen = TextEdit('', self)
        self.labelElse = QLabel('Иначе', self)
        self.inputElse = TextEdit('', self)

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
        self.input = TextEdit('', self)

        self.holder.addWidget(self.num)
        self.holder.addWidget(self.label)
        self.holder.addWidget(self.input)

        self.params = [self.num, self.input]

    def contextMenuEvent(self, event):
        # TODO: REARRANGE NUMERATION AFTER DELETE
        contextMenu = QMenu(self)
        deleteAction = contextMenu.addAction("Удалить")
        #moveAction = contextMenu.addAction("Переместить")

        action = contextMenu.exec_(self.mapToGlobal(event.pos()))
        if action == deleteAction:
            self.setParent(None)
        #elif action == moveAction:
        #    self.parent().

class Constructor(QWidget):
    '''
    Constructor window
    '''
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
        '''
        Parses users input
        '''
        # Scans all pins
        res_orig = self.main.findChildren(Pin)
        if len(res_orig) > 0:
            # Gets every pin
            res = [item.params for item in res_orig]
            # Reads content of every pin
            out = []
            for i in range(len(res)):
                pin = []
                for item in res[i]:
                    pin.append(item.text()[:-1].replace('\n', ' '))
                out.append(pin)

            for i in range(len(out)):
                out[i].append(res_orig[i].type)
            return out

    @pyqtSlot()
    @pyqtSlot(str)
    def on_click(self, param=None):
        def createCondition():
            self.mainLayout.addWidget(Pin('cond', len(self.main.findChildren(Pin)) + 1, self))
        def createLoop():
            self.mainLayout.addWidget(Pin('loop', len(self.main.findChildren(Pin)) + 1, self))
        def createExecute():
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
