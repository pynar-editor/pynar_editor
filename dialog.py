import sys, stat
import os
from PyQt5 import Qt
from PyQt5.QtCore import QSize, QRect, pyqtSignal
from PyQt5.QtWidgets import (QApplication, QWidget, QDialog, QHBoxLayout,
                             QVBoxLayout, QGridLayout, QLabel, QLineEdit,
                             QPushButton, QMainWindow, QCheckBox, QDesktopWidget,
                             QGroupBox, QSpinBox, QTextEdit, QTabWidget,
                             QDialogButtonBox, QMessageBox, QListWidget,
                             QListWidgetItem, QComboBox, QFontDialog)
from PyQt5.QtGui import (QFont, QPalette, QIcon)
from PyQt5.Qt import Qt
from configuration import Configuration
from widgets import (MessageBox, Label, RadioButton, PushButton,
                     ListWidget, WhiteLabel, TabWidget, TextEdit)
from deadcodechecker import DeadCodeChecker
from pycodechecker import PyCodeChecker
from natsort import natsorted
import urllib
from urllib import parse
import requests
import subprocess,json
from threading import Thread
import re
import configparser


class fontDialog(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setWindowIcon(QIcon(':/icon/images/headerLogo1.png'))

class Dialog(QDialog):

    def __init__(self, parent=None, textPad=None):
        super().__init__()
        palette = QPalette()
        role = QPalette.Background
        # palette.setColor(role, QColor('#2c2c2c'))
        self.setGeometry(parent.x() + 200 , parent.y() + 100, 500, 400)
        self.setPalette(palette)
        self.mainWindow = parent

class EnterDialog(QDialog):
    def __init__(self, parent, fileName, filePath, fileDir, fileInfo, rename=True, folderPath=None):
        super().__init__(parent)
        
        self.fileName = fileName
        self.filePath = filePath
        self.fileDir = fileDir
        self.fileInfo = fileInfo
        self.rename = rename
        self.folderPath = folderPath
        
        self.initUI()
        
    def initUI(self):
        self.setModal(True)
        
        if self.rename == True:
            if self.fileDir:
                self.setWindowTitle('Rename Directory')
            else:
                self.setWindowTitle('Rename File')
        
        elif self.rename == False:
            self.setWindowTitle('Create Directory')
        
        layout = QVBoxLayout()
        
        if self.rename == True:
            self.label = QLabel(self.fileName)
            
        elif self.rename == False:
            self.label = QLabel('in: ' + self.folderPath)
        
        self.text = QLineEdit()
        self.text.setPlaceholderText("Enter name")
        
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        
        layout.addWidget(self.label)
        layout.addWidget(self.text)
        layout.addWidget(self.buttonBox)
        
        self.setLayout(layout)
        
        if self.rename == True:
            self.buttonBox.accepted.connect(self.accept)
        elif self.rename == False:
            self.buttonBox.accepted.connect(self.acceptMakeFolder)
        
        # for both dialogs (rename / make)
        self.buttonBox.rejected.connect(self.onReject)
        
        self.fileName = self.checkPath(self.fileName)
        self.filePath = self.checkPath(self.filePath)
        

    def checkPath(self, path):
        if '\\' in path:
            path = path.replace('\\', '/')
        return path

    def accept(self):
        if self.fileDir:

            if self.label.text() == '..':
                self.close()
    
            newName = self.text.text()
            cutPaths = self.filePath.split('/')[:-1]
            path = '/'.join(cutPaths)
            newPathName = path +  '/' + newName
            if self.text.text() == '':
                return
            try:
                os.rename(self.filePath, newPathName)
            except Exception as e:
                q = MessageBox(QMessageBox.Critical, 'Hata', 'Yol yeniden adland??r??lamad??\n\n' + str(e),
                                QMessageBox.NoButton)
                q.exec_()
            
        if not self.fileDir:
            newName = self.text.text()
            oldFileName = self.filePath.split('/')[-1]
            path = self.filePath.split(oldFileName)[0]
            newFilename = path + newName
            
            # check if file exists
            for file in os.listdir(path):
                if file == newName:
                    result = MessageBox(QMessageBox.Question, 'Uyar??', 'Dosya zaten mevcut\n' +
                                                 'Devam et ?', QMessageBox.Yes | QMessageBox.No)

                    if (result.exec_() == QMessageBox.No):
                        return
            
            try:
                os.rename(self.filePath, newFilename)
            except Exception as e:
                q = MessageBox(QMessageBox.Critical, 'Hata', 'Dosya yeniden adland??r??lamad??\n\n' + str(e),
                                QMessageBox.NoButton)

                q.exec_()
           
        self.close() 
    
    def acceptMakeFolder(self):
        sourcePath = self.folderPath
        newPath = self.text.text()
        if newPath.startswith('/'):
            newPath = newPath.strip('/')
        fullNewPath = sourcePath + newPath
        try:
            os.mkdir(fullNewPath)
        except Exception as e:
            q = MessageBox(QMessageBox.Critical, 'Hata', 'Dizin olu??turulamad??\n\n' + str(e),
                                QMessageBox.NoButton)

            q.exec_()
        
        self.close()

    def onReject(self):
        self.close()


class FindDeadCodeDialog(QDialog):

    def __init__(self, parent, textPad, codeView):
        super().__init__()

        self.mainWindow = parent
        self.textPad = textPad
        self.codeView = codeView

        palette = QPalette()
        role = QPalette.Background
        # palette.setColor(role, QColor('#2c2c2c'))
        self.setGeometry(self.codeView.x() + 300, self.codeView.y() + 400, 400, 300)
        self.setPalette(palette)

        self.setWindowTitle('??l?? Kod Listesi')
        self.initUI()

    def initUI(self):
        filename = os.path.basename(self.textPad.filename)
        vbox = QVBoxLayout()

        self.label = WhiteLabel(filename + ' :\n\n')
        self.label.setAlignment(Qt.AlignCenter)

        self.listWidget = ListWidget()

        updateButton = PushButton('Kaydet + G??ncelle')
        updateButton.clicked.connect(self.update)
        okButton = PushButton('Tamam')
        okButton.clicked.connect(self.onClose)

        hbox = QHBoxLayout()
        # hbox.addWidget(updateButton)
        hbox.addWidget(okButton)

        vbox.addWidget(self.label)
        vbox.addWidget(self.listWidget)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.fillList()

        # signals
        self.listWidget.itemDoubleClicked.connect(self.gotoPos)

        self.show()

    def update(self):
        self.listWidget.clear()
        self.mainWindow.save()
        self.fillList()

    def fillList(self):
        filename = os.path.basename(self.textPad.filename)
        self.label.setText(filename)

        text = self.textPad.text()
        deadCodeChecker = DeadCodeChecker(text)
        outputList = deadCodeChecker.getList()

        self.lineNumberList = []
        self.codeList = []

        for elem in outputList:
            textList = elem.split(' ')
            self.lineNumberList.append(textList[0])
            codeText = ''

            for elem in textList[1:]:
                codeText += ' ' + elem

            self.codeList.append(codeText)

        i = 0
        for elem in self.codeList[0:-1]:
            item = QListWidgetItem()
            text = 'Sat??r: ' + str(self.lineNumberList[i]) + '\t-> ' + str(self.codeList[i])
            # pos = int(self.lineNumberList[i])
            item.setText(text)
            self.listWidget.addItem(item)
            i += 1

    def gotoPos(self):
        row = self.listWidget.currentRow()
        linenumber = int(str(self.lineNumberList[row]).replace(".",""))-1

        if linenumber >= 0:
            lineText = self.textPad.text(linenumber)
            rawcode = self.codeList[row]
            code = rawcode[rawcode.find("'") + 1:rawcode.rfind("'")]

            x = self.textPad.findFirst(code, False, True, False, True, True,
                                       line=linenumber, index=0)

            self.listWidget.clearSelection()
            self.textPad.setFocus()

    def onClose(self):
        self.destroy()
        self.close()  # hata ay??klay??c?? ekran?? ????kt??????nda ekran kapat??lsada program ask??da kal??yordu, close fonk eklendi.


class PyCodeCheckerDialog(QDialog):
    
    def __init__(self, parent, textPad, codeView):
        super().__init__()

        self.mainWindow = parent
        self.textPad = textPad
        self.codeView = codeView
        
        palette = QPalette()
        role = QPalette.Background
        # palette.setColor(role, QColor('#2c2c2c'))
        self.setGeometry(self.codeView.x()+ 200, self.codeView.y(), 400, 300)
        self.setPalette(palette)

        self.setWindowTitle('Kod Stili Kontrol?? Yap (pyton yaz??m denetleyicisi kullanarak)')
        self.initUI()

    
    def initUI(self):
        filename = os.path.basename(self.textPad.filename)
        vbox = QVBoxLayout()
        
        self.label = WhiteLabel(filename + ' :\n\n')
        self.label.setAlignment(Qt.AlignCenter)

        self.listWidget = ListWidget()
        
        updateButton = PushButton('Kaydet + G??ncelle')
        updateButton.clicked.connect(self.update)
        okButton = PushButton('Tamam')
        okButton.clicked.connect(self.onClose)
        
        hbox = QHBoxLayout()
        hbox.addWidget(updateButton)
        hbox.addWidget(okButton)
        
        vbox.addWidget(self.label)
        vbox.addWidget(self.listWidget)
        vbox.addLayout(hbox)
        
        self.setLayout(vbox)
        
        self.fillList()
        
        # signals
        self.listWidget.itemDoubleClicked.connect(self.gotoPos)
        
        self.show()

    def update(self):
        self.listWidget.clear()
        self.mainWindow.save()
        self.fillList()

    def fillList(self):
        filename = os.path.basename(self.textPad.filename)
        self.label.setText(filename)
        
        check = PyCodeChecker(filename)
        text = check.getString()
        self.lineList, self.cursorList, self.textList = check.getListFromString(text)

        i = 0
        for elem in self.textList:
            item = QListWidgetItem()
            try:
                text = 'Sat??r: ' + str(self.lineList[i]) + '  Pozisyon: ' + str(self.cursorList[i]) + \
                        '  ' + str(self.textList[i])
                item.setText(text)
                self.listWidget.addItem(item)

            except Exception as e:
                item.destroy()

            i += 1
    
    def gotoPos(self):
        row = self.listWidget.currentRow()
        
        line = self.lineList[row]
        cursor = self.cursorList[row]
        
        self.textPad.setSelection(int(line)-1, int(cursor)-1, int(line)-1, int(cursor))

        
    def onClose(self):
        self.destroy()

class Main(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        dialog = SettingsDialog(self)
        sys.exit(dialog.exec_())



if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    sys.exit(app.exec_())
