import sys
import pickle

from functools import partial
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QAction, QGroupBox, QVBoxLayout, QRadioButton, QCheckBox, QMainWindow, QLineEdit, QLabel, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

from modules.constructor import Constructor
from modules.modal import Dialog
from modules.table import Table
from modules.parser import Runner


class Main(QMainWindow):
    '''
    Main form class
    '''
    # TODO: create multi-language support
    # Enable macros support - done
    # Create log window
    def __init__(self):
        super(Main, self).__init__(None)
        self.setAcceptDrops(True)
        self.title = 'WebCrawler 🕸🕷 by Alexander Shashkov'
        self.left = 500
        self.top = 500
        self.width = 320
        self.height = 100
        self.initUI()

        # parameters of parse 

        self.saveAs = 'csv'
        self.headless = True
    
    def initUI(self):
        '''
        Default initialization
        '''

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        windowLayout = QHBoxLayout()
        self.createParameters()
        windowLayout.addWidget(self.parameters)
        windowLayout.addWidget(self.constructor)
        windowLayout.addWidget(self.table)
        widget = QWidget()
        widget.setLayout(windowLayout)
        self.setCentralWidget(widget)

        '''
        Top
        '''
        openAction = QAction("&Открыть", self)
        openAction.setShortcut("Ctrl+O")
        openAction.setStatusTip('Открыть сохраненный макрос')
        openAction.triggered.connect(self.openMacros)

        saveAction = QAction("&Сохранить как...", self)
        saveAction.setShortcut("Ctrl+S")
        saveAction.setStatusTip('Сохранить макрос')
        saveAction.triggered.connect(self.saveMacros)

        toggleParamsAction = QAction(f'&Скрыть/показать параметры', self)
        toggleParamsAction.triggered.connect(self.toggleParams)
        toggleMacrosActoin = QAction('&Скрыть/показать конструктор', self)
        toggleMacrosActoin.triggered.connect(self.toggleConstructor)
        toggleTableActoin = QAction('&Скрыть/показать таблицу', self)
        toggleTableActoin.triggered.connect(self.toggleTable)

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&Файл 🗃')
        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction)

        windowMenu = mainMenu.addMenu('&Окружение ⚙')
        windowMenu.addAction(toggleParamsAction)
        windowMenu.addAction(toggleMacrosActoin)
        windowMenu.addAction(toggleTableActoin)

        mainMenu.addMenu('&Справка ❔')
        mainMenu.addMenu('&О программе 🐱‍👤')
        
        self.show()

    def createParameters(self):
        '''
        Ex createSeparated
        Creates separated parameters window
        TODO: create a pop-up window or rebuild current window?
        '''
        self.parameters = QGroupBox("Параметры парсера")
        layout = QVBoxLayout()

        checkBox = QCheckBox("Скрытый режим")
        checkBox.toggle()
        checkBox.stateChanged.connect(self.checkBoxHandler)
        layout.addWidget(checkBox)

        label = QLabel('Макс. количество попыток\nпри time-out:')
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
        self.parameters.setMaximumWidth(200)

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
        self.table.setMaximumWidth(600)

    def radioHandler(self):
        '''
        Handles radiobuttons
        '''
        radioButton = self.sender()
        if radioButton.isChecked():
            print("Selected type {}".format(radioButton.type))

    def checkBoxHandler(self, state):
        '''
        Handles checkboxes
        '''
        if state:
            print("Headless mode")
            self.headless = True
        else:
            self.headless = False
    
    @pyqtSlot()
    @pyqtSlot(str)
    def on_click(self, param=None):
        def startWork():
            '''
            Internal function to start parse job
            '''
            self.run = Runner(self, self.headless, self.maxTimeoutTries.text())
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

    def saveMacros(self):
        '''
        Saves macroses
        '''
        work = self.inConstructor.getScenario()
        if work is not None:
            name = QFileDialog.getSaveFileName(self, 'Сохранить как', "", "Макрос (*.webmacr)|*.webmacr")[0]
            if name != '':
                work = [item[1:len(item)] for item in work]
                with open(name, 'wb') as f:
                    pickle.dump(work, f)

    def openMacros(self):
        '''
        Opens macroses
        '''
        name = QFileDialog.getOpenFileName(self, 'Открыть', "", "Макрос (*.webmacr)|*.webmacr")[0]
        if name != '':
            with open(name, 'rb') as f:
                work = pickle.load(f)
                print(work)
                for item in work:
                    self.inConstructor.on_click(item[len(item)-1])


    def toggleParams(self):
        status = self.parameters.isVisible
        self.parameters.setVisible(not status)
        self.parameters.isVisible = not status

    def toggleConstructor(self):
        status = self.constructor.isVisible
        self.constructor.setVisible(not status)
        self.constructor.isVisible = not status

    def toggleTable(self):
        status = self.table.isVisible
        self.table.setVisible(not status)
        self.table.isVisible = not status

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    sys.exit(app.exec_())
