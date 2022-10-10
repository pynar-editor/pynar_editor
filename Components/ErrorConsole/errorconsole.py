import os, sys
import tempfile

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor, QFont
from PyQt5.Qsci import QsciScintilla
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
from pathlib import Path

from Components.SyntaxChecker.SyntaxCheck import writeLog
from configuration import Configuration
from soundlib import playsound # ses için
from threading import Thread

class PushButton(QPushButton):
    def __init__(self, parent=None):
        super(PushButton, self).__init__(parent)
        self.parentdir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
        self.setIcon(QIcon(self.parentdir + "/images/close-hover.png"))

    def enterEvent(self, event):
        self.setIcon(QIcon(self.parentdir + "/images/close.png"))

    def leaveEvent(self, event):
        self.setIcon(QIcon(self.parentdir + "/images/close-hover.png"))

class ErrorConsole(QWidget):
    def __init__(self):
        super().__init__()
        self.message = ""
        self.c = Configuration()
        self.createTable()


    def createTable(self):

        font = QFont()
        font.setFamily(self.c.getEditorFont())
        font.setPointSize(self.c.getEditorFontSize())

        errorList = QLineEdit()
        errorList.setFont(font)
        errorList.setText("  Hata Listesi")
        errorList.setReadOnly(True)
        errorList.setStyleSheet("background-color: rgb(248,220,143);")

        self.closeButton = PushButton()
        self.closeButton.setStyleSheet("background-color: rgb(248,220,143);")
        self.closeButton.setIconSize(QtCore.QSize(23, 18))
        self.closeButton.setText("")
        self.closeButton.setCheckable(True)
        self.closeButton.setDefault(False)
        self.closeButton.setAutoDefault(False)
        self.closeButton.setMouseTracking(True)

        hBox = QHBoxLayout()
        hBox.setContentsMargins(0, 0, 0, 0)
        hBox.addWidget(errorList)
        hBox.addWidget(self.closeButton)
        hBox.setSpacing(0)


        self.tableWidget = QTableWidget()
        self.tableWidget.setFont(font)

        self.tableWidget.setColumnCount(4)

        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.setWordWrap(True)

        self.tableWidget.setTextElideMode(Qt.ElideNone)

        self.tableWidget.setHorizontalHeaderLabels(['','Hata Mesajı', 'Dosya', 'Satır'])
        self.tableWidget.horizontalHeaderItem(1).setTextAlignment(Qt.AlignLeft)
        self.tableWidget.horizontalHeaderItem(2).setTextAlignment(Qt.AlignLeft)
        self.tableWidget.horizontalHeaderItem(3).setTextAlignment(Qt.AlignLeft)
        headerFont = """QHeaderView::section {
                                        background-color: lightgray;
                                        color: black;
                                        padding-left: 4px;
                                        border: 1px solid #ffffff;
                                        font-weight: bold;
                                    }               
            """

        self.tableWidget.horizontalHeader().setStyleSheet(headerFont)
        self.tableWidget.horizontalHeader().setFont(font)

        self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tableWidget.setSelectionMode(QTableWidget.SingleSelection)
        self.tableWidget.setSelectionBehavior(QTableWidget.SelectRows)

        self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)

        self.tableWidget.horizontalHeader().setMinimumWidth(20)
        self.tableWidget.verticalHeader().setMaximumSectionSize(300)


        self.tableWidget.horizontalHeader().resizeSection(0, 10)
        self.tableWidget.horizontalHeader().resizeSection(3, 45)

        self.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
        self.tableWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setSectionResizeMode(3, QHeaderView.Fixed)


        self.tableWidget.cellClicked.connect(self.Indicator)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(hBox)
        layout.addWidget(self.tableWidget)

        self.setLayout(layout)

    def add(self, message, textPad, sound = True):
        self.message = message
        self.textPad = textPad
        self.clear()
        messLen = len(message)
        self.tableWidget.setRowCount(messLen)
        parentdir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
        for i in range(messLen):
            icon = QTableWidgetItem()
            if str(message[i]['severity']) == 'error' or str(message[i]['severity']) == 'runtime error':
                icon.setIcon(QIcon(parentdir+r'/images/error.png'))
            elif str(message[i]['severity']) == 'warning':
                icon.setIcon(QIcon(parentdir + r'/images/warning.png'))
            else:
                icon.setIcon(QIcon(parentdir + r'/images/close-hover.png'))
            fileName = str(Path(str(message[i]['file']))).replace('\\','/')
            self.tableWidget.setItem(i, 0, icon)
            self.tableWidget.setItem(i, 2, QTableWidgetItem(fileName[fileName.rfind('/') + 1:]))
            self.tableWidget.setItem(i, 3, QTableWidgetItem(str(message[i]['range']['start']['line'] + 1)))

            if message[i]['message'] == '"(" ifadesi kapatılmadı':
                with open(tempfile.gettempdir() + "/hata.txt", "r", encoding='utf-8') as f:
                    engMsg = f.read()

                parent = self.parent().parent().parent()
                logAndInd = writeLog(self, os.path.dirname(os.path.realpath(__file__)), parent.errorConsole,
                                     parent.splitterV)

                tmp = logAndInd.showCmdMessage(engMsg, parent.textPad).split('\n')
                tmp = [x for x in tmp if x]
                message[i]['message'] = tmp[-1]


            self.tableWidget.setItem(i, 1, QTableWidgetItem(str(message[i]['message'])))

        self.tableWidget.resizeRowsToContents()
        if sound:
            a = Thread(target=playsound, args=[parentdir + '/Data/Sounds/error.mp3'], daemon=True)
            a.start() # bell

    def addCmdMessage(self, message, textPad):
        self.message = message
        self.textPad = textPad
        self.clear()
        messLen = len(message)
        self.tableWidget.setRowCount(messLen)
        parentdir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
        for i in range(messLen):
            icon = QTableWidgetItem()
            if str(message[i]['severity']) == 'error' or str(message[i]['severity']) == 'runtime error':
                icon.setIcon(QIcon(parentdir+r'/images/error.png'))
            elif str(message[i]['severity']) == 'warning':
                icon.setIcon(QIcon(parentdir + r'/images/warning.png'))
            else:
                icon.setIcon(QIcon(parentdir + r'/images/close-hover.png'))
            fileName = str(Path(str(message[i]['file']))).replace('\\','/')
            self.tableWidget.setItem(i, 0, icon)
            self.tableWidget.setItem(i, 1, QTableWidgetItem(str(message[i]['message'])))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(fileName[fileName.rfind('/') + 1:]))
            self.tableWidget.setItem(i, 3, QTableWidgetItem(str(message[i]['range']['start']['line'] + 1)))
        self.tableWidget.resizeRowsToContents()

        a = Thread(target=playsound, args=[parentdir + '/Data/Sounds/error.mp3'], daemon=True)
        a.start() # bell

    def Indicator(self, row, column):
        self.textPadClear(self.textPad)
        indicatorLine = self.message[row]['range']
        errStartLine = indicatorLine['start']['line']
        errStartChar = indicatorLine['start']['character']
        errEndLine = indicatorLine['end']['line']
        errEndChar = indicatorLine['end']['character']
        self.textPad.setCursorPosition(errStartLine, 0)
        self.textPad.indicatorDefine(QsciScintilla.ThickCompositionIndicator, 1)
        self.textPad.setIndicatorForegroundColor((QColor('#ff0000')), 1)
        self.textPad.fillIndicatorRange(errStartLine, 0, errEndLine, self.textPad.lineLength(errEndLine) - 1, 1)


    def textPadClear(self,textPad):
        textPad.clearIndicatorRange(0, 0, textPad.lines() - 1, textPad.lineLength(textPad.lines() - 1), 1)

    def clear(self):
        self.tableWidget.setRowCount(0)

    def closeTab(self,textPad):
        self.textPadClear(textPad)
        self.tableWidget.selectionModel().clearSelection()
