from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui
from configuration import Configuration


def CustomizeMessageBox_Yes_No(message, clickAccept=None, clickCancel=None, yes='Evet', no='Hayır', icon="question"):
    c = Configuration()
    msgBox = QMessageBox()

    msgBox.setText(f"<table cellpadding='2'><tr valign='middle'><td ><img src=':icon/images/{icon}.png'/></td><td>{message}</td></tr></table>")
    msgBox.setWindowFlags(msgBox.windowFlags() |Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)
    msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    font = QFont()
    font.setFamily(c.getEditorFont())
    font.setPointSize(c.getEditorFontSize())
    msgBox.setFont(font)
    if icon == "critical":
        msgBox.setProperty("state", icon)
    elif icon == "warning" or icon == "question":
        msgBox.setProperty("state", "question")
    else:
        msgBox.setProperty("state", "normal")

    msgBox.setStyleSheet(open(c.getHomeDir() + "qssfiles/qmessagebox.qss", "r").read())
    BtnOk = msgBox.button(QMessageBox.Ok)
    msgBox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    BtnOk.setText(yes)
    BtnOk.setFont(font)
    BtnCancel = msgBox.button(QMessageBox.Cancel)
    BtnCancel.setText(no)
    BtnCancel.setFont(font)
    if clickAccept:
        msgBox.accepted.connect(clickAccept)
    if clickCancel:
        msgBox.rejected.connect(clickCancel)

    msgBox.exec()


#Sol menünün dragEnterEvent'ı içerisinde bu fonksiyon çağrılıyor ise messagebox'ı exec yapmamalı return etmelidir. control değişkeni onun kontrolü için kullanılıyor
def CustomizeMessageBox_Ok(message, icon="question", control=False):
    c = Configuration()
    msgBox = QMessageBox()
    msgBox.setText(f"<table cellpadding='2'><tr valign='middle'><td ><img src=':icon/images/{icon}.png'/></td><td>{message}</td></tr></table>")
    msgBox.setWindowFlags(msgBox.windowFlags() | Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)
    msgBox.setStandardButtons(QMessageBox.Ok)
    font = QFont()
    font.setFamily(c.getEditorFont())
    font.setPointSize(c.getEditorFontSize())
    msgBox.setFont(font)
    if icon == "critical":
        msgBox.setProperty("state", icon)
    elif icon == "warning" or icon == "question":
        msgBox.setProperty("state", "question")
    else:
        msgBox.setProperty("state", "normal")

    msgBox.setStyleSheet(open(c.getHomeDir() + "qssfiles/qmessagebox.qss", "r").read())
    BtnOk = msgBox.button(QMessageBox.Ok)
    BtnOk.setText('Tamam')
    BtnOk.setFont(font)
    msgBox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

    if control:
        return msgBox
    else:
        msgBox.exec()


def CustomizeMessageBox_Yes_No_Cancel(message, icon="question"):
    c = Configuration()
    msgBox = QMessageBox()

    msgBox.setText(f"<table cellpadding='2'><tr valign='middle'><td ><img src=':icon/images/{icon}.png'/></td><td>{message}</td></tr></table>")
    msgBox.setWindowFlags(msgBox.windowFlags() | Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)
    msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
    font = QFont()
    font.setFamily(c.getEditorFont())
    font.setPointSize(c.getEditorFontSize())
    msgBox.setFont(font)

    if icon == "critical":
        msgBox.setProperty("state", icon)
    elif icon == "warning" or icon == "question":
        msgBox.setProperty("state", "question")
    else:
        msgBox.setProperty("state", "normal")

    msgBox.setStyleSheet(open(c.getHomeDir() + "qssfiles/qmessagebox.qss", "r").read())

    BtnOk = msgBox.button(QMessageBox.Yes)
    msgBox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    BtnOk.setText('Evet')
    BtnOk.setFont(font)
    BtnCancel = msgBox.button(QMessageBox.No)
    BtnCancel.setText('Hayır')
    BtnCancel.setFont(font)

    BtnClose = msgBox.button(QMessageBox.Cancel)
    BtnClose.setText('Vazgeç')
    BtnClose.setFont(font)

    return msgBox
