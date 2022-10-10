import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QProxyStyle, QStyle, QDesktopWidget)
from Components.ChatBotView.chatbot_engine import LoadChatbotPairs_Reflection
from Components.ChatBotView.chatbotview import LoadUserMessages
from Components.ChatBotView.Messages import LoadDialogButtons
from Components.StartPage.startpage import StartPage
from pynar import MainWindow
from Components.SplashScreen.splashscreen import UcSplashScreen
from Components.DetectOs.detectos import detectos
from PyQt5.QtCore import Qt, QTimer
from PyQt5 import QtCore
from configuration import Configuration
from os import environ


# Konsoldaki Qt Warning mesajlarını kapatmak için.
def suppress_qt_warnings():
    environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    environ["QT_SCALE_FACTOR"] = "1"

class Main():
    def __init__(self):

        return

if __name__ == '__main__':
    c = Configuration()
    detectos().writeIni()

    suppress_qt_warnings() # Konsoldaki Qt Warning mesajlarını kapatmak için.

    LoadChatbotPairs_Reflection()
    LoadUserMessages()
    LoadDialogButtons()
    app = QApplication(sys.argv)
    app.setStyleSheet(open(c.getHomeDir() + "qssfiles/style.qss", "r").read())

    splashscreen = UcSplashScreen()
    splashscreen.setWindowFlags(Qt.SplashScreen | Qt.FramelessWindowHint)
    splashscreen.show()

    QTimer.singleShot(2000, splashscreen.closeScreen)
    main = MainWindow()

    # Chatbot'ta sağ click menüsünü türkçeye çevirmek için
    translator = QtCore.QTranslator(app)
    locale = QtCore.QLocale.system().name()
    path = QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.TranslationsPath)
    translator.load('qtbase_%s' % locale, path)
    app.installTranslator(translator)

    sp = StartPage(main)

    sys.exit(app.exec_())

