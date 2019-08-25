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
    def __init__(self, parent, headless, max_tries):
        #super(Methods, self).__init__(parent)
        self.opts = Options()
        print('Running in headess:', headless)
        self.opts.headless = headless
        self.opts.add_argument('log-level=3')
        self.browser = Chrome(options=self.opts)

        self.max_tries = int(max_tries)

        self.parent = parent
        self.table = self.parent.inTable

    def back(self):
        self.get(self.last)

    def get(self, input):
        self.last = self.browser.current_url
        self.browser.get(input)

    def iterationalGet(self, input, change):
        if(self.currentLoopIteration is not None):
            input = input.replace(change, str(self.currentLoopIteration))
            self.get(input)
        else:
            print('ДЛЯ ИСПОЛЬЗОВАНИЯ iterGet СОЗДАЙТЕ ЦИКЛ')
            self.stop()

    def click(self):
        if type(self.object) == WebElement:
            self.last = self.browser.current_url
            self.object.click()
        else:
            if self.currentLoopIteration is not None:
                self.last = self.browser.current_url
                self.object[self.currentLoopIteration].click()
            else:
                print('ДЛЯ ИСПОЛЬЗОВАНИЯ click НА НЕСКОЛЬКИХ ОБЪЕКТАХ СОЗДАЙТЕ ЦИКЛ')
                self.stop()

    def objectLen(self, input=None):
        if input is not None:
            return len(input)
        if type(self.object) == WebElement:
            return 1
        else:
            return len(self.object)

    def getXpathText(self, input):
        self.getByXpath(input)
        val = self.getText()
        return val

    def getClassText(self, input):
        self.getByClassName(input)
        val = self.getText()
        return 

    def getByXpath(self, input):
        self.object = self.getObject(input, By.XPATH, 0)

    def getByClassName(self, input):
        self.object = self.getObject(input, By.CLASS_NAME, 0)

    def getById(self, input):
        self.object = self.getObject(input, By.ID, 0)

    def getObject(self, input, type, tries):
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

class Runner(Methods):
    def __init__(self, parent, headless, max_tries):
        super(Runner, self).__init__(parent, headless, max_tries)
        self.running = False
        self.object = None

        self.commands = {
            'goto':self.goto, 'test':self.test, 'stop':self.stop, 'get':self.get, 'back':self.back, 'iterGet':self.iterationalGet,
            'getX':self.getByXpath, 'getClass':self.getByClassName, 'getId':self.getById,
            'getClassMulti':self.getMultipleByClassName,
            'getXText':self.getXpathText, 'getClassText':self.getClassText, 'click':self.click,
            'getLen':self.objectLen, 'addRow':self.addRow, 'delRow':self.test, 'writeCell':self.editCell, 'clearRow':self.test
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
        if parameters is not None:
            return self.commands[function](*parameters)
        else:
            return self.commands[function]()

    def runLoop(self, function):
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
        pass

    def goto(self, input):
        self.execute(self.work[int(input)-1])

    def stop(self):
        self.browser.quit()
        self.running = False
