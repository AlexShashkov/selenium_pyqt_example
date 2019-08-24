import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, QVBoxLayout, QRadioButton, QCheckBox, QMainWindow, QLineEdit, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

from functools import partial

from modules.constructor import Constructor
from modules.modal import Dialog
from modules.table import Table
from modules.parser import Runner


class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__(None)
        self.setAcceptDrops(True)
        self.title = 'WebCrawler - Александр Шашков, 2019'
        self.left = 500
        self.top = 500
        self.width = 320
        self.height = 100
        self.initUI()

        # parameters of parse 

        self.saveAs = 'csv'
        self.headless = True
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.createSeparated()
        
        windowLayout = QHBoxLayout()
        windowLayout.addWidget(self.parameters)
        windowLayout.addWidget(self.constructor)
        windowLayout.addWidget(self.table)
        widget = QWidget()
        widget.setLayout(windowLayout)
        self.setCentralWidget(widget)

        
        self.show()

    def createSeparated(self):
        self.parameters = QGroupBox("Параметры парсера")
        layout = QVBoxLayout()

        #radiobutton = QRadioButton("Сохранить в csv формате")
        #radiobutton.setChecked(True)
        #radiobutton.type = "csv"
        #radiobutton.toggled.connect(self.radioHandler)
        #layout.addWidget(radiobutton)
        
        #radiobutton = QRadioButton("Сохранить в txt формате")
        #radiobutton.type = "txt"
        #radiobutton.toggled.connect(self.radioHandler)
        #layout.addWidget(radiobutton)

        checkBox = QCheckBox("Скрытый режим")
        checkBox.toggle()
        checkBox.stateChanged.connect(self.checkBoxHandler)
        layout.addWidget(checkBox)

        label = QLabel('Макс. количество попыток time-out:')
        layout.addWidget(label)
        self.maxTimeoutTries = QLineEdit('2', self)
        layout.addWidget(self.maxTimeoutTries)


        label = QLabel('Имя файла:')
        layout.addWidget(label)
        self.fileName = QLineEdit('', self)
        layout.addWidget(self.fileName)

        button = QPushButton('Сохранить таблицу', self)
        button.clicked.connect(partial(self.on_click, 'save'))
        layout.addWidget(button)
        
        button = QPushButton('Запустить парсер', self)
        button.clicked.connect(partial(self.on_click, 'start'))
        layout.addWidget(button)
        
        layout.addStretch()
        self.parameters.setLayout(layout)

        #################################

        self.constructor = QGroupBox("Конструктор макросов")
        layout = QVBoxLayout()

        self.inConstructor = Constructor()
        layout.addWidget(self.inConstructor)
        
        self.constructor.setLayout(layout)

        ##################################

        self.table = QGroupBox("Работа с таблицей")
        layout = QVBoxLayout()

        self.inTable = Table()
        layout.addWidget(self.inTable)

        button = QPushButton('Очистить', self)
        button.clicked.connect(partial(self.on_click, 'clear_table'))
        layout.addWidget(button)

        button = QPushButton('Параметры столбцов', self)
        button.clicked.connect(partial(self.on_click, 'new_column'))
        layout.addWidget(button)

        self.table.setLayout(layout)

    def radioHandler(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            print("Selected type {}".format(radioButton.type))

    def checkBoxHandler(self, state):
        if state:
            print("Headless mode")
            self.headless = True
        else:
            self.headless = False
    
    @pyqtSlot()
    @pyqtSlot(str)
    def on_click(self, param=None):
        def startWork():
            self.run = Runner(self, self.headless, self.maxTimeoutTries.text())
            #self.run.execute('get', 'https://www.youtube.com/watch?v=LH5ay10RTGY')
            print('START')
            work = self.inConstructor.getScenario()
            try:
                self.run.pre_execute(work)
            except Exception as ex:
                print('ОШИБКА:', ex)
                self.run.stop()
            print('END')

        def clearTable():
            self.inTable.clear()

        def newColumn():
            self.dialog = Dialog(self, 'Добавить столбец', 'Название')
            self.dialog.exec_()

        def save():
            self.inTable.writeCsv(self.fileName.text())

        params = {'start':startWork, 'new_column':newColumn, 'clear_table':clearTable, 'save':save}
        params[param]()

    def test(self):
        print('mainform test')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    sys.exit(app.exec_())
