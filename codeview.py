import sys
import ast
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QMainWindow,
                            QVBoxLayout, QListWidget, QListWidgetItem,
                            QMenu, QAction)

from PyQt5.QtGui import QColor
from PyQt5.Qt import Qt
from dialog import FindDeadCodeDialog, PyCodeCheckerDialog
import py_compile

class CodeView(QListWidget):
    ''' ListWidget to view elements in the code '''
    def __init__(self, parent=None, notebook=None):
        ''' init CodeView '''
        super().__init__()
        self.notebook = notebook
        self.mainWindow = parent
        self.mainWindow.setObjectName("codeViewMainWidget")
        self.verticalScrollBar().setObjectName("codeViewScrollBarV")
        self.horizontalScrollBar().setObjectName("codeViewScrollBarH")

        # Contextmenu
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.openMenu)

        self.popMenu = QMenu()
        self.popMenu.setObjectName("codeViewPopMenu")

        codeAction = QAction('Geçersiz dosya bulundu ', self)
        codeAction.triggered.connect(self.onCode)
        codeCheckAction = QAction('Kod Stil Kontrolü Yap (pyton yazım denetleyicisi kullanarak)', self)
        codeCheckAction.triggered.connect(self.onCodeCheck)
        compileAction = QAction('Derle', self)
        compileAction.triggered.connect(self.onCompile)

        self.popMenu.addAction(codeAction)
        self.popMenu.addSeparator()
        self.popMenu.addAction(codeCheckAction)
        self.popMenu.addSeparator()
        self.popMenu.addAction(compileAction)


        # signals
        self.itemDoubleClicked.connect(self.gotoPos)


    def openMenu(self, position):
        # -> open contextMenu
        self.popMenu.exec_(self.mapToGlobal(position))

    def onCode(self):
        self.clearSelection()

        if not self.notebook.textPad:
            return

        self.mainWindow.save()

        textPad = self.notebook.textPad
        filename = textPad.filename

        if filename:
            try:
                findDeadCode = FindDeadCodeDialog(self.mainWindow, textPad, self)
                findDeadCode.setModal(False)
                textPad.debugging = True
                findDeadCode.exec_()
            except Exception as e:
                print("Ölü kod bulunurken hata oluştu: {0}".format(e))

                # self.mainWindow.showMessage(str(e), 3000)
        else:
            self.mainWindow.statusBar.showMessage("Dosya adı olmadan kullanılmayan kod bulunamıyor!", 3000)

        textPad.debugging = False

    def onCodeCheck(self):
        self.clearSelection()

        if not self.notebook.textPad:
            return

        self.mainWindow.save()

        textPad = self.notebook.textPad
        filename = textPad.filename

        if filename:
            try:
                c = PyCodeCheckerDialog(self.mainWindow, textPad, self)
                c.setModal(False)
                textPad.debugging = True
                c.exec_()
            except Exception as e:
                self.mainWindow.showMessage(str(e), 3000)
        else:
            self.mainWindow.statusBar.showMessage("dosya adı olmadan kodu kontrol edemez!", 3000)

        textPad.debugging = False

    def onCompile(self):
        self.clearSelection()

        if not self.notebook.textPad:
            return

        self.mainWindow.save()

        textPad = self.notebook.textPad
        filename = textPad.filename

        if filename:
            py_compile.compile(filename)
            self.mainWindow.statusBar.showMessage('Bitti !', 3000)
        else:
            self.mainWindow.statusBar.showMessage("dosya adı olmadan derlenemez!", 3000)



    def makeDictForCodeView(self, text=''):
        codeViewDict = {}
        textList = text.splitlines()

        i = 1
        for x in textList:
            if x.strip().startswith('class ') or x.strip().startswith('def '):
                codeViewDict[i] = x.strip()

            i += 1

        return codeViewDict

    def updateCodeView(self, codeViewDict):
        self.clear()
        self.code = list(codeViewDict.values())
        self.linenumbers = list(codeViewDict.keys())

        # for line in self.code:
        #
        #     if line.strip().startswith('class'):
        #         item = QListWidgetItem()
        #         text = line.strip()
        #         text = text.strip(':')
        #         item.setText(text)
        #         # item.setForeground(QColor('#ffff00'))
        #         self.addItem(item)
        #
        #     elif line.strip().startswith('def'):
        #         item = QListWidgetItem()
        #         text = line.strip()
        #         text = text.strip(':')
        #         item.setText('->   ' + text)
        #         # item.setForeground(QColor('light blue'))
        #         self.addItem(item)

    def gotoPos(self):
        row = self.currentRow()
        linenumber = self.linenumbers[row] - 1
        textPad = self.notebook.textPad
        if linenumber >= 0:
            y = textPad.lineLength(linenumber) - 1
            textPad.setCursorPosition(linenumber, y)
            textPad.setFocus()

        self.clearSelection()

    def refresh(self):
        self.clearSelection()
        


class Main(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.view = CodeView()
        widget = QWidget()
        widget.setObjectName("codeViewWidget")

        layout = QVBoxLayout()
        layout.addWidget(self.view)
        self.setCentralWidget(widget)
        widget.setLayout(layout)
        self.show()


if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    main = Main()
    sys.exit(app.exec_())
