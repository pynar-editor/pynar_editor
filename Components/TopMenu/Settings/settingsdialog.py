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
from dialog import Dialog,fontDialog

class SettingsDialog(Dialog):
    def __init__(self, parent=None, textPad=None):
        super().__init__(parent, textPad)
        self.parent = parent
        self.textPad = textPad
        self.c = Configuration()
        self.setWindowTitle('Editör Ayarları')
        self.setWindowIcon(QIcon(':/icon/images/settings_i.png'))
        self.setStyleSheet("background-color: #CAD7E0;")
        self.setMinimumSize(QSize(560, 333))
        self.setMaximumSize(QSize(560, 333))
        self.initUI()

    def initUI(self):
        font = QFont()
        font.setFamily(self.c.getEditorFont())
        font.setPointSize(self.c.getEditorFontSize())

        self.codeFontDialog = QFontDialog()

        self.editorFontDialog = QFontDialog()

        groupBox = QWidget()
        groupBox.setFont(font)
        groupBox.setGeometry(QRect(0, 0, 500, 300))
        groupBox.setStyleSheet(" background-color: rgb(255, 255, 255);")
        groupBox.setObjectName("settingsTab")

        labelEditor = Label(groupBox)
        labelEditor.setGeometry(QRect(30, 38, 200, 25))
        labelEditor.setText('Editör Yazı Tipi ve Boyutu:')
        labelEditor.setFont(font)
        labelEditor.setObjectName("settingsMenu")

        self.editorBox = QLineEdit(groupBox)
        self.editorBox.setGeometry(QRect(240, 40, 150, 25))
        self.editorBox.setReadOnly(True)
        self.editorBox.setText(self.c.getEditorFont())
        self.editorBox.setFont(font)

        self.editorSizeBox = QLineEdit(groupBox)
        self.editorSizeBox.setGeometry(QRect(400, 40, 30, 25))
        self.editorSizeBox.setReadOnly(True)
        self.editorSizeBox.setText(str(self.c.getEditorFontSize()))
        self.editorSizeBox.setFont(font)


        labelChangeEditor = clickableLabel(groupBox)
        labelChangeEditor.setGeometry(QRect(440, 40, 100, 22))
        labelChangeEditor.setText("[" + "<a href=#>Değiştir</a>" + "]")
        labelChangeEditor.setFont(font)
        labelChangeEditor.clicked.connect(self.changeEditorFont)
        labelChangeEditor.setObjectName("settingsMenu")

        labelCode = Label(groupBox)
        labelCode.setGeometry(QRect(30, 68, 200, 25))
        labelCode.setText('Kod Yazı Tipi ve Boyutu:')
        labelCode.setFont(font)
        labelCode.setObjectName("settingsMenu")

        self.codeBox = QLineEdit(groupBox)
        self.codeBox.setGeometry(QRect(240, 70, 150, 25))
        self.codeBox.setReadOnly(True)
        self.codeBox.setText(self.c.getCodeFont())
        self.codeBox.setFont(font)

        self.codeSizeBox = QLineEdit(groupBox)
        self.codeSizeBox.setGeometry(QRect(400, 70, 30, 25))
        self.codeSizeBox.setReadOnly(True)
        self.codeSizeBox.setText(str(self.c.getFontSize()))
        self.codeSizeBox.setFont(font)

        labelChangeCode = clickableLabel(groupBox)
        labelChangeCode.setGeometry(QRect(440, 70, 100, 22))
        labelChangeCode.setText("[" + "<a href=#>Değiştir</a>" + "]")
        labelChangeCode.setFont(font)
        labelChangeCode.clicked.connect(self.changeCodeFont)
        labelChangeCode.setObjectName("settingsMenu")

        label1 = Label(groupBox)
        label1.setGeometry(QRect(30, 98, 265, 25))
        label1.setText('<Tab> Tuşu Genişliği:')
        label1.setFont(font)
        label1.setObjectName("settingsMenu")


        self.tabWidthBox = QSpinBox(groupBox)
        self.tabWidthBox.setMinimum(2)
        self.tabWidthBox.setMaximum(10)
        self.tabWidthBox.setGeometry(QRect(240, 101, 42, 22))
        self.tabWidthBox.setFont(font)
        tab = int(self.c.getTab())
        self.tabWidthBox.setValue(tab)
        self.tabWidthBox.setObjectName("settingsSpinBox")


        self.loggingCase = QCheckBox(groupBox)
        self.loggingCase.setGeometry(QRect(240, 134, 20, 20))
        self.loggingCase.setStyleSheet("color:rgb(82, 95, 99)")
        self.loggingCase.setFont(font)
        self.loggingCase.setCheckState(0 if self.c.getParam('Logging', 'logging') == "False" else 1)
        self.loggingCase.setTristate(0)
        self.loggingCase.setObjectName("settingsCheckBox")


        labelLogging = WhiteLabel(groupBox)
        labelLogging.setGeometry(QRect(30, 131, 195, 22))
        labelLogging.setText('Kullanım Verilerini Kaydet')
        labelLogging.setFont(font)
        labelLogging.setObjectName("settingsMenu")

        labelYes = WhiteLabel(groupBox)
        labelYes.setGeometry(QRect(262, 132, 70, 22))
        labelYes.setText('Evet')
        labelYes.setFont(font)
        labelYes.setObjectName("settingsMenu")

        labelData = WhiteLabel(groupBox)
        labelData.setGeometry(QRect(30, 161, 200, 22))
        labelData.setText("Kullanım Verileri")
        labelData.setFont(font)
        labelData.setObjectName("settingsMenu")

        labelDelete = clickableLabel(groupBox)
        labelDelete.setGeometry(QRect(240, 161, 140, 22))
        labelDelete.setText("[" + "<a href=#>Tüm Verileri Sil</a>" + "]")
        labelDelete.setFont(font)
        labelDelete.clicked.connect(self.deleteAllLogFolder)
        labelDelete.setObjectName("settingsMenu")

        labelDataLocal = WhiteLabel(groupBox)
        labelDataLocal.setGeometry(QRect(30, 191, 200, 22))
        labelDataLocal.setText("Kullanım Verileri Konumu")
        labelDataLocal.setFont(font)
        labelDataLocal.setObjectName("settingsMenu")

        labelOpen = clickableLabel(groupBox)
        labelOpen.setGeometry(QRect(240, 191, 150, 22))
        labelOpen.setText("[" + "<a href=#>Veri Klasörünü Aç</a>" + "]")
        labelOpen.setFont(font)
        labelOpen.clicked.connect(self.openLogFolder)
        labelOpen.setObjectName("settingsMenu")

        okButton = PushButton(groupBox)
        okButton.setGeometry(QRect(30, 240, 141, 41))
        okButton.setText('TAMAM')
        okButton.setFont(font)
        okButton.setStyleSheet("QPushButton { color: white;padding: 5px;margin: 4px 2px;border-radius: 4px; background-color: rgb(0, 170, 255);} " \
                      "QPushButton::hover{background-color:rgb(4, 124, 184)}")
        okButton.setObjectName("settingsMenu")


        okButton.pressed.connect(self._okButton)
        self.loggingCase.stateChanged.connect(self.logging)


        layout = QVBoxLayout()
        layout.addWidget(groupBox)
        self.setLayout(layout)
        self.center()

    def changeCodeFont(self):
        font = QFont()
        font.setFamily(self.c.getCodeFont())
        font.setPointSize(int(self.c.getFontSize()))

        font, ok = self.codeFontDialog.getFont(font, fontDialog(), "Font Ayarları", QFontDialog.MonospacedFonts)
        if ok:
            fontData = font.toString().split(',')
            self.c.setCodeFont(fontData[0])
            self.c.updateConfig('Size', 'size', str(round(float(fontData[1]))))
            self.codeBox.setText(self.c.getCodeFont())
            self.codeSizeBox.setText(str(self.c.getFontSize()))

    def changeEditorFont(self):
        try:
            font = QFont()
            font.setFamily(self.c.getEditorFont())
            font.setPointSize(self.c.getEditorFontSize())

            font, ok = self.editorFontDialog.getFont(font, fontDialog(), "Font Ayarları", QFontDialog.ProportionalFonts)
            if ok:
                fontData = font.toString().split(',')
                self.c.setEditorFont(fontData[0])
                self.c.updateConfig('Size', 'editorsize', str(round(float(fontData[1]))))
                self.editorBox.setText(self.c.getEditorFont())
                self.editorSizeBox.setText(str(self.c.getEditorFontSize()))
        except Exception as err:
            print("changeEditorFont {0}".format(err))


    def _okButton(self):
        messageBox = QMessageBox(QMessageBox.Information, "text", "text")
        messageBox.setWindowIcon(QIcon(':/icon/images/headerLogo1.png'))
        messageBox.setStandardButtons(QMessageBox.Ok)
        messageBox.setWindowTitle("Dikkat !!!")
        messageBox.setText("Bu ayarlarda yaptığınız değişiklikler Pynar Editörünü tekrar başlattığınızda geçerli olacaktır.")
        messageBox.exec()
        self.close()

    def deleteAllLogFolder(self):
        try:
            messageBox = QMessageBox(QMessageBox.Question, "text", "text")
            messageBox.setWindowIcon(QIcon(':/icon/images/headerLogo1.png'))
            messageBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            messageBox.setWindowTitle("Dikkat !!!")
            messageBox.setText("Tüm Kullanım ve Hata Verileriniz Silinecek\n\t\"Onaylıyor musunuz ?\"")
            messageBox.setIcon(QMessageBox.Question)
            messageBox.setDefaultButton(QMessageBox.No)
            messageBox = messageBox.exec()
            if messageBox == QMessageBox.Yes:
                logDir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))) + "/Log/"
                filelist = [f for f in os.listdir(logDir) if f.endswith(".json")]
                for f in filelist:
                    os.remove(os.path.join(logDir, f))
                messageBox = QMessageBox(QMessageBox.Information, "text", "text")
                messageBox.setWindowIcon(QIcon(':/icon/images/headerLogo1.png'))
                messageBox.setStandardButtons(QMessageBox.Ok)
                messageBox.setWindowTitle("Tamamlandı")
                messageBox.setText("Tüm Kullanım Verileri Silindi")
                messageBox.setIcon(QMessageBox.Information)
                messageBox.exec()

        except Exception as err:
            print("deleteAllLogFolder {0}".format(err))

    def openLogFolder(self):
        try:
            if self.c.getSystem() == "windows":
                subprocess.call("explorer " + os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))) + "\Log", shell = True)
            elif self.c.getSystem() == "mac":
                os.system("open " + os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))) + "/Log")
            else:
                os.system("xdg-open " + os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))) + "/Log")

        except Exception as err:
            print("openLogFolder {0}".format(err))

    def logging(self):
        cs = bool(self.loggingCase.checkState())
        self.c.updateConfig('Logging', 'logging', str(cs))

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)

    def close(self):
        tab = self.tabWidthBox.value()
        self.c.updateConfig('Tab', 'tab', str(tab))
        self.done(1)

class clickableLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self,parent=None):
        super().__init__(parent)

    def mousePressEvent(self, ev):
        self.clicked.emit()
