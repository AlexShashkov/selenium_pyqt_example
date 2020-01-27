import time
import csv

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement

class Methods():
    '''
    Methods for parsing
    '''
    def __init__(self, parent, headless, max_tries):
        #super(Methods, self).__init__(parent)
        self.opts = Options()
        print('Running in headess:', headless)
        self.opts.headless = headless
        self.opts.add_argument('log-level=3')
        self.browser = Chrome(options=self.opts)

        self.parent = parent
        self.table = self.parent.inTable

        # To store variables
        self.variables = {}
        # Count of tries before canceling
        self.max_tries = int(max_tries)

    def back(self):
        '''
        Return to the previos page
        '''
        self.get(self.last)

    def get(self, input):
        '''
        Load page
        '''
        input = self.checkIfVarExists(input)
        self.last = self.browser.current_url
        self.browser.get(input)

    def goto(self, input):
        '''
        Goto to jump from cell to cell
        '''
        input = self.checkIfVarExists(input)
        self.execute(self.work[int(input)-1])

    def iterationalGet(self, input, change):
        '''
        iterational load
        '''
        input = self.checkIfVarExists(input)
        if(self.currentLoopIteration is not None):
            input = input.replace(change, str(self.currentLoopIteration))
            self.get(input)
        else:
            print('ДЛЯ ИСПОЛЬЗОВАНИЯ iterGet СОЗДАЙТЕ ЦИКЛ')
            self.stop()

    def click(self):
        '''
        Clicks at object or objects
        '''
        if type(self.object) == WebElement:
            self.last = self.browser.current_url
            self.object.click()
        else:
            # Checks that given cycle
            if self.currentLoopIteration is not None:
                self.last = self.browser.current_url
                self.object[self.currentLoopIteration].click()
            else:
                print('ДЛЯ ИСПОЛЬЗОВАНИЯ click НА НЕСКОЛЬКИХ ОБЪЕКТАХ СОЗДАЙТЕ ЦИКЛ')
                self.stop()

    def objectLen(self, input=None):
        '''
        Get length of object
        '''
        if input is not None:
            input = self.checkIfVarExists(input)
            return len(input)
        if type(self.object) == WebElement:
            return 1
        else:
            return len(self.object)

    def getXpathText(self, input):
        '''
        Get text by xpath
        '''
        input = self.checkIfVarExists(input)
        self.getByXpath(input)
        val = self.getText()
        return val

    def getClassText(self, input):
        '''
        Get text by class name
        '''
        input = self.checkIfVarExists(input)
        self.getByClassName(input)
        val = self.getText()
        return 

    def getByXpath(self, input):
        '''
        Get object by xpath
        '''
        self.object = self.getObject(input, By.XPATH, 0)

    def getByClassName(self, input):
        '''
        Get object by class name
        '''
        self.object = self.getObject(input, By.CLASS_NAME, 0)

    def getById(self, input):
        '''
        Get object by class name
        '''
        self.object = self.getObject(input, By.ID, 0)

    def getObject(self, input, type, tries):
        '''
        Get object
        '''
        inp = None
        try:
            
            inp = WebDriverWait(self.browser, 1).until(EC.presence_of_element_located((type, input)))
        except TimeoutException:
            if tries < self.max_tries:
                print(f'TIMEOUT: ПОПЫТКА {tries} ИЗ {self.max_tries}')
                inp = self.getObject(input, type, tries + 1)
            else:
                print(f'ЭЛЕМЕНТ {input} НЕ НАЙДЕН')
                inp = None
        return inp


    def getMultipleByClassName(self, input):
        def get(tries):
            inp = None
            try:
                inp = WebDriverWait(self.browser, 1).until(EC.presence_of_element_located((By.CLASS_NAME, input)))
                inp = self.browser.find_elements_by_class_name(input)
            except TimeoutException:
                if tries < self.max_tries:
                    print(f'TIMEOUT: ПОПЫТКА {tries} ИЗ {self.max_tries}')
                    inp = get(tries + 1)
                else:
                    print(f'ЭЛЕМЕНТ {input} НЕ НАЙДЕН')
                    inp = None
            return inp

        input = self.checkIfVarExists(input)
        self.object = get(0)

    def getText(self):
        if self.object is None:
            return ''
        else:
            return self.object.text

    def test(self):
        print('its a test')

    ###

    def addRow(self):
        self.table.addRow()

    def editCell(self, val1, val2=None, value=None):
        if value is None:
            value = self.getText()
        if val2 is None:
            val1 = int(val1)
            self.table.editCell(value, self.table.table.rowCount() - 1, val1)
        else:
            val1 = int(val1)
            val2 = int(val2)
            self.table.editCell(value, val1, val2)

    def savePicture(self, input, path):
        input = self.checkIfVarExists(input)
        path = self.checkIfVarExists(path)
        pass

    def createVar(self, name, value):
        self.variables[name] = value

    def deleteVar(self, name):
        self.variables.pop(name)
    
    def checkIfVarExists(self, input):
        if input in self.variables.keys():
            return self.variables[input]

        return input

class Runner(Methods):
    '''
    Class that runs input of user
    '''
    def __init__(self, parent, headless, max_tries):
        super(Runner, self).__init__(parent, headless, max_tries)
        self.running = False
        self.object = None

        self.commands = {
            # List of all commands
            'goto':self.goto, 'test':self.test, 'stop':self.stop,
            'get':self.get, 'back':self.back, 'iterGet':self.iterationalGet,
            'getX':self.getByXpath, 'getClass':self.getByClassName, 'getId':self.getById,
            'getClassMulti':self.getMultipleByClassName,
            'getXText':self.getXpathText, 'getClassText':self.getClassText, 'click':self.click,
            'getLen':self.objectLen, 'addRow':self.addRow, 'delRow':self.test,
            'writeCell':self.editCell, 'clearRow':self.test, 'picture':self.savePicture,
            'value':self.createVar, 'delVal':self.deleteVar
            }

    def pre_execute(self, work):
        print(work)
        self.work = work
        self.running = True
        if work is None:
            self.stop()

        if self.running:
            for item in work:
                if self.running:
                    res = self.execute(item)
                else:
                    break

    def execute(self, function):
        '''
        Executes input of user
        '''
        if function[len(function)-1] == 'run':
            pre = function[1].split('; ')
            if len(pre) > 1:
                it = []
                for new_item in pre:
                    it.append([function[0], new_item, function[2]])
                items = it
                for item in items:
                    self.execute(item)
            else:
                parameters = []
                function = function[1].split(' ')
                parameters = function[1:]
                function = function[0]
                return self.run(function, parameters)
        elif function[len(function)-1] == 'loop':
            self.runLoop(function)
        elif function[len(function)-1] == 'cond':
            self.runCondition(function)

    def run(self, function, parameters=None):
        '''
        Run command
        '''
        if parameters is not None:
            return self.commands[function](*parameters)
        else:
            return self.commands[function]()

    def runLoop(self, function):
        '''
        Method that executes loop
        '''
        print(function)
        frm = function[1]
        to = function[2]
        exec = function[3]
        other = function[4]

        keys = self.commands.keys()

        if any(key in frm for key in keys):
            frm = self.execute([None, frm, 'run'])
        else:
            frm = int(frm)
        if any(key in to for key in keys):
            to = self.execute([None, to, 'run'])
        else:
            to = int(to)

        for i in range(frm, to, 1):
            self.currentLoopIteration = i
            self.execute([None, exec, 'run'])
        if len(other)>0:
            self.execute([None, other, 'run'])
        self.currentLoopIteration = None

    def runCondition(self, function):
        '''
        Method that executes condition
        '''
        print(function)
        first = function[1]
        second = function[2]
        exec = function[3]
        other = function[4]

        keys = self.commands.keys()

        if any(key in first for key in keys):
            first = self.execute([None, first, 'run'])
        if any(key in second for key in keys):
            second = self.execute([None, second, 'run'])

        if first == second:
            self.execute([None, exec, 'run'])
        else:
            if len(other)>0:
                self.execute([None, other, 'run'])

    def writeToCell(self, input):
        '''
        Changes cell? Possibly topology
        '''
        pass

    def stop(self):
        '''
        Stops job
        '''
        self.browser.quit()
        self.running = False
