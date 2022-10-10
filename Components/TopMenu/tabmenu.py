from PyQt5.QtWidgets import QTabWidget, QLabel
from PyQt5 import QtCore, QtGui
from Components.TopMenu.toolbar import ToolBar
from configuration import Configuration
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtGui import QFont


class TabMenu(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.mainWindow = parent
        self.layout_widget = QVBoxLayout(self)

        c = Configuration()

        font = QFont()
        font.setFamily(c.getEditorFont())
        font.setPointSize(c.getEditorFontSize())

        self.PynarTabs = QTabWidget()
        self.PynarTabs.setFont(font)
        self.PynarTabs.setStyleSheet(open(c.getHomeDir() + "qssfiles/qtabwidget.qss", "r").read())
        self.PynarTabs.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.tabFile = QWidget()
        self.tabSetting = QWidget()
        self.tabCloud = QWidget()
        self.tabHelp = QWidget()

        self.PynarTabs.addTab(self.tabFile, "Dosya")
        self.PynarTabs.addTab(self.tabSetting, "Ayarlar")
        self.PynarTabs.addTab(self.tabCloud, "Bulut")
        self.PynarTabs.addTab(self.tabHelp, "Yardım")

        self.tabFile_layout = QVBoxLayout()
        self.tabSetting_layout = QVBoxLayout()
        self.tabCloud_layout = QVBoxLayout()
        self.tabHelp_layout = QVBoxLayout()

        self.layout_widget.addWidget(self.PynarTabs)
        self.setLayout(self.layout_widget)

    def AddAllToolBar(self, fileToolbar,settingsToolbar,cloudToolbar,helpToolbar):

        self.tabFile_layout.addWidget(fileToolbar)
        self.tabFile.setLayout(self.tabFile_layout)

        self.tabSetting_layout.addWidget(settingsToolbar)
        self.tabSetting.setLayout(self.tabSetting_layout)

        self.tabCloud_layout.addWidget(cloudToolbar)
        self.tabCloud.setLayout(self.tabCloud_layout)

        self.tabHelp_layout.addWidget(helpToolbar)
        self.tabHelp.setLayout(self.tabHelp_layout)
