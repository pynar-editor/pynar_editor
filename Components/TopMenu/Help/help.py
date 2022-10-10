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
from dialog import Dialog

class HelpDialog(Dialog):

    def __init__(self, parent=None,pView=None):
        super().__init__(parent,pView)
        c = Configuration()
        self.parent = parent
        self.view = pView
        self.setWindowIcon(QIcon(':/icon/images/help.png'))
        self.setWindowFlags(Qt.WindowMaximizeButtonHint | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
        mainLayout = QVBoxLayout()

        self.setObjectName("HelpWidget")
        self.setWindowTitle('Yardım')
        self.setMinimumSize(QSize(1200, 700))
        self.setLayout(mainLayout)
        self.setModal(False)

        font = QFont()
        font.setFamily(c.getEditorFont())
        font.setPointSize(c.getEditorFontSize())

        mainLayout.addWidget(self.view)
        self.center()


    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)
