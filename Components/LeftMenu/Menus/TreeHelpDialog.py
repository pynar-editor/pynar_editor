#!/usr/bin/env python
import os

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import (QApplication, QDialog, QHBoxLayout, QListView, QListWidget, QListWidgetItem, QPushButton,
                             QStackedWidget, QVBoxLayout, QWidget)
from configuration import Configuration

descriptions = {}


class TanimSayfasi(QWidget):
    def __init__(self, dosyaAdi):
        super(TanimSayfasi, self).__init__()
        mainLayout = QVBoxLayout()
        self.view = QWebEngineView()
        self.c = Configuration()  # bundan sonra dosya yolunu configuration'dan alalım.
        dosyaPath = self.c.getHomeDir() + self.c.getHtmlHelpPath("html_help_path")
        url = QtCore.QUrl.fromLocalFile(dosyaPath + dosyaAdi.split("#")[0])
        url.setFragment(dosyaAdi.split("#")[1])
        self.view.load(url)
        mainLayout.addWidget(self.view)
        mainLayout.addStretch(1)
        self.setLayout(mainLayout)

    def resizeEvent(self, event):
        self.view.setFixedHeight(self.height())


class TreeHelpDialog(QDialog):

    def __init__(self, dosyaAdi):
        super(TreeHelpDialog, self).__init__()

        dosyaAdi = self.getKey(dosyaAdi)
        self.c = Configuration()
        self.setWindowTitle("Yardım Menüsü")
        self.setWindowIcon(QIcon(':/icon/images/helpwinIcon.png'))


        mainLayout = QVBoxLayout()
        self.setMinimumSize(QSize(800, 500))
        self.setLayout(mainLayout)
        self.setModal(False)
        self.frameGeometry()

        closeButton = QPushButton("Kapat")
        font = QFont()
        font.setFamily(self.c.getEditorFont())
        font.setPointSize(self.c.getEditorFontSize())
        closeButton.setFont(font)
        closeButton.setStyleSheet("QPushButton { color: white;padding: 5px;margin: 2px;border-radius: 4px; background-color: rgb(0, 170, 255);} QPushButton::hover{background-color:rgb(4, 124, 184)}")
        self.setStyleSheet("background-color: #CAD7E0;")

        closeButton.setFixedWidth(70)
        closeButton.setFixedHeight(41)
        closeButton.setLayoutDirection(Qt.RightToLeft)
        closeButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        closeButton.clicked.connect(self.close)

        self.pagesWidget = QStackedWidget()
        self.pagesWidget.addWidget(TanimSayfasi(dosyaAdi))
        mainLayout.addWidget(self.pagesWidget)
        mainLayout.addWidget(closeButton)




    def changePage(self, current, previous):
        if not current:
            current = previous
        self.pagesWidget.setCurrentIndex(self.contentsWidget.row(current))

    def getKey(self, val):
        for key, value in descriptions.items():
            if val == value:
                return key


def TreeViewItemFill(des):
    descriptions.update(des)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
