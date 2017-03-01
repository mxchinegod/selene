import sys, os
from PyQt5.QtWidgets import (QMainWindow, QTextEdit, 
    QAction, QFileDialog, QApplication, QLabel)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QThread, pyqtSignal

class OtherThread(QThread):

    # This is where I setup my signals to communicate to the main program class. The 'str' parameter means that the signal will emit a string object to whatever function we connect it to in the main program thread.
    to_log = pyqtSignal(str)

    def __init__(self, driver, parent=None):
        
        super(OtherThread, self).__init__(parent)
        # any other __init__ code here. Be careful what you pass to your QThread in the init, because it may tie it back to the main program thread. Better to create the class, and then assign variables from the main program class afterwards.
        self.driver = driver
        
    def run(self):
        import se
        from selenium.webdriver.common.keys import Keys
        from selenium import webdriver
#        config=[]
#        with open("settings.conf","r") as f:
#            for each in f:
#                config.append(each)
#        f.close()
#        driver = str(config[0].replace('\n',''))
        c = webdriver.Chrome(self.driver)
        c.implicitly_wait(10)
        se.browse("http://google.com",c)
        se.grab("""//*[@id="lst-ib"]""","click",c)
        se.keys("hello world",c,1)
        se.keys(Keys.ENTER,c,1)


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
        
        lbl3 = QLabel('version 1.0', self)
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
        
        if os.path.isfile("chromedriver.exe"):
            cwd = os.getcwd()
            init_msg = " [ + ] 'chromedriver.exe' found!"
            with open("settings.conf","w") as f:
                f.write(cwd.replace('\\','/')+"/chromedriver.exe\n")
            f.close()
        else:
            init_msg = " [ + ] 'chromedriver.exe' missing in Selene directory!\n\n"
        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)
        
        self.statusBar()
        
        openFile = QAction(QIcon('open.png'), 'Open...', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open automation schedule')
        openFile.triggered.connect(self.fileDialog)
        
        openInfo = QAction(QIcon('info.png'), 'About Selene', self)
        openInfo.setShortcut('Ctrl+I')
        openInfo.setStatusTip('Program version & info')
        openInfo.triggered.connect(self.infoDialog)

        runSelene = QAction(QIcon('run.png'), 'Run...', self)
        
        setDriver = QAction(QIcon('chrome.png'), 'Select driver...', self)
        setDriver.setShortcut('Ctrl+D')
        setDriver.setStatusTip('Select Chrome driver (default is working directory)')
        setDriver.triggered.connect(self.selectDialog)
        
        runSelene.setShortcut('Ctrl+R')
        runSelene.setStatusTip('Run Selene using current settings')
        runSelene.triggered.connect(self.runSelene)

        self.setWindowIcon(QIcon('icon.png'))        
        menubar = self.menuBar()
        
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)  
        fileMenu.addAction(setDriver) 
        
        runMenu = menubar.addMenu('&Program')
        runMenu.addAction(runSelene)
        
        runMenu = menubar.addMenu('&Info')
        runMenu.addAction(openInfo)
        
        self.setGeometry(300, 300, 500, 300)
        self.setWindowTitle('Selene - Launcher')
        self.show()
        self.textEdit.setText(init_msg+"\n")
        

    def runSelene(self):

        # Check config for needed info
        config=[]
        with open("settings.conf","r") as f:
            for each in f:
                config.append(each)
        f.close()
        if len(config)==1:
            pass
            self.textEdit.setText(" [ ! ] No automation file selected! Ctrl+O to select file from your computer.\n\n")
        else:
            self.textEdit.setText("Running Selene...\n\n")
            self.textEdit.append(" [ + ] Using "+str(config[1])+"\n")
            self.textEdit.append(" [ + ] Loading "+str(config[0])+"\n")
            config=[]
            with open("settings.conf","r") as f:
                for each in f:
                    config.append(each)
            f.close()
            driver = str(config[0].replace('\n',''))
            # Make sure you make the QThread part of the main class scope so it isn't garbage collected once the click_start() method has finished.
            self.worker = OtherThread(driver)
            # Optional: assign variables needed by the worker.
            #self.worker.load_urls(list_of_urls)
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
                with open("settings.conf","a") as f:
                    f.write(fname[0])
                f.close()

                
    def selectDialog(self):
        
        dname = QFileDialog.getOpenFileName(self, 'Select driver', '/chromedriver.exe')
        if dname[0].split('.')[1]=="exe":
            self.textEdit.setText(" [ + ] Chrome driver loaded!\n\n")
            with open("settings.conf","w") as f:
                f.write(dname[0]+'\n')
            f.close()
        else:
            self.textEdit.setText(" [ ! ] File was not an executable. Please make sure it's the proper 'chromedriver.exe' file.")        
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = GUI()
    sys.exit(app.exec_())