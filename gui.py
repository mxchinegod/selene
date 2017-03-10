import sys, os, modules
from PyQt5.QtWidgets import (QMainWindow, QTextEdit,
    QAction, QFileDialog, QApplication, QLabel, QInputDialog, QLineEdit)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QThread, pyqtSignal

class OtherThread(QThread):

    to_log = pyqtSignal(str)

    def __init__(self, driver, instructions, mod, timer, parent=None):

        super(OtherThread, self).__init__(parent)

        self.driver = driver
        self.instructions = instructions
        self.mod = mod
        self.timer = timer

    def run(self):

        if self.mod == "craigslist":
            self.start = modules.craigslist(self.driver,self.instructions,self.timer)
            self.start()

class About(QMainWindow):

    def __init__(self, parent=None):

        super(About, self).__init__(parent)

        self.setGeometry(100, 120, 380, 120)

        lbl1 = QLabel('Selene', self)
        lbl1.resize(300,30)
        lbl1.move(10, 2)

        lbl5 = QLabel('http://thisiswhereidostuff.com',self)
        lbl5.resize(300,30)
        lbl5.move(10, 79)

        lbl2 = QLabel('______', self)
        lbl2.resize(300,30)
        lbl2.move(10, 4)

        lbl3 = QLabel('version 1.20', self)
        lbl3.resize(300,30)
        lbl3.move(10, 30)

        lbl4 = QLabel('Dylan Moore', self)
        lbl4.resize(300,30)
        lbl4.move(10, 54)

        self.setWindowTitle('About Selene')


class GUI(QMainWindow):

    def __init__(self):

        super().__init__()
        self.initUI()

    def initUI(self):

        if os.path.isfile("modules\chromedriver.exe"):
            cwd = os.getcwd()
            init_msg = " [ + ] 'chromedriver.exe' found!"
            self.driver = str(cwd+"\modules\chromedriver.exe")
        else:
            init_msg = " [ + ] 'chromedriver.exe' missing in Selene directory!\n\n"
        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)

        self.statusBar()

        selectMod = QAction(QIcon('img/craigslist.png'), 'Craigslist', self)
        selectMod.setStatusTip('Select the craigslist post bot')
        selectMod.triggered.connect(self.craigSelect)

        openFile = QAction(QIcon('img/open.png'), 'Open...', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open automation schedule')
        openFile.triggered.connect(self.fileDialog)

        openInfo = QAction(QIcon('img/info.png'), 'About Selene', self)
        openInfo.setShortcut('Ctrl+I')
        openInfo.setStatusTip('Program version & info')
        openInfo.triggered.connect(self.infoDialog)

        runSelene = QAction(QIcon('img/run.png'), 'Run...', self)

        setDriver = QAction(QIcon('img/chrome.png'), 'Select driver...', self)
        setDriver.setShortcut('Ctrl+D')
        setDriver.setStatusTip('Select Chrome driver (default is working directory)')
        setDriver.triggered.connect(self.selectDialog)

        timerSelect = QAction(QIcon('img/timer.png'), 'Set timer...', self)
        timerSelect.setShortcut('Ctrl+T')
        timerSelect.setStatusTip('Set automation interval in seconds...')
        timerSelect.triggered.connect(self.timerSelect)

        runSelene.setShortcut('Ctrl+R')
        runSelene.setStatusTip('Run Selene using current settings')
        runSelene.triggered.connect(self.runSelene)

        self.setWindowIcon(QIcon('img/icon.png'))
        menubar = self.menuBar()

        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)
        fileMenu.addAction(setDriver)

        runMenu = menubar.addMenu('&Program')
        runMenu.addAction(runSelene)
        runMenu.addAction(timerSelect)

        fileMenu = menubar.addMenu('&Modules')
        fileMenu.addAction(selectMod)
        fileMenu.addAction(openFile)

        runMenu = menubar.addMenu('&Info')
        runMenu.addAction(openInfo)

        self.setGeometry(300, 300, 500, 300)
        self.setWindowTitle('Selene - Launcher')
        self.show()
        self.textEdit.setText(init_msg+"\n")


    def runSelene(self):

        if self.instructions == '':
            self.textEdit.setText(" [ ! ] No automation file selected! Ctrl+O to select file from your computer.\n\n")
        elif self.mod == '':
            self.textEdit.setText(" [ ! ] No module selected! Use the module drop-down to select a pre-configured mod.\n\n" )
        elif self.driver == '':
            self.textEdit.setText(" [ ! ] No driver loaded! Select the 'chromedriver.exe' file from your computer.\n\n" )
        elif self.timer == '':
            self.textEdit.setText(" [ ! ] No timer set! Use the Program menu to select interval.\n\n" )
        else:
            self.textEdit.setText("Running Selene...\n\n")
            self.textEdit.append(" [ + ] Using "+str(self.instructions)+".\n")
            self.textEdit.append(" [ + ] Loading "+str(self.driver)+".\n")
            self.textEdit.append(" [ + ] Selected "+str(self.mod)+" mod.\n" )
            self.textEdit.append(" [ + ] Timer set for "+str(self.timer)+" seconds.\n" )
            self.worker = OtherThread(self.driver, self.instructions, self.mod, self.timer)
            self.worker.start()

    def infoDialog(self):

        self.dialog = About(self)
        self.dialog.show()

    def fileDialog(self):

        fname = QFileDialog.getOpenFileName(self, 'Open file', '/*.csv')
        if fname[0]:
            self.textEdit.setText(" [ + ] "+fname[0]+" selected.\n\n")
            if fname[0].split('.')[1]!="csv":
                self.textEdit.setText(" [ ! ] File is not a compatible .csv!\n\n")
            else:
                self.instructions = str(fname[0])

    def selectDialog(self):

        dname = QFileDialog.getOpenFileName(self, 'Select driver', '/chromedriver.exe')
        if dname[0].split('.')[1]=="exe":
            self.textEdit.setText(" [ + ] Chrome driver loaded!\n\n")
            self.driver = str(dname[0])
        else:
            self.textEdit.setText(" [ ! ] File was not an executable. Please make sure it's the proper 'chromedriver.exe' file.")

    def craigSelect(self):

        self.mod = "craigslist"
        self.textEdit.setText(" [ + ] Craigslist module selected!\n\n")

    def timerSelect(self):
            timer, okPressed = QInputDialog.getText(self, "Interval","Timer (in seconds):", QLineEdit.Normal, "")
            if okPressed and timer != '':
                self.timer = int(timer)
                self.textEdit.setText(" [ + ] Timer set for "+str(self.timer)+" seconds!\n\n")

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = GUI()
    sys.exit(app.exec_())
