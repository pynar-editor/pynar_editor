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
        self.setLayout(mainLayout)
        self.setModal(False)
        self.frameGeometry()

        self.pagesWidget = QStackedWidget()
        self.pagesWidget.addWidget(TanimSayfasi(dosyaAdi))
        mainLayout.addWidget(self.pagesWidget)




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
