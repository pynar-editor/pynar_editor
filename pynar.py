import sys
import os
import platform
import uuid
import subprocess

from PyQt5 import QtWidgets, QtCore
from PyQt5.uic.properties import QtGui
from Components.Flowchart.flower import *
from Components.LeftMenu.Menus.TreeHelpDialog import TreeHelpDialog
from Components.StartPage.emptyrecent import UcEmptyRecent
from Components.TopMenu.uc_sp_recentitem import UcSpRecentItem
from widgets import MessageBox
from Components.TopMenu.uc_sp_examitem import UcSpExamItem

plt = platform.system()
from PyQt5.QtCore import QSize, QModelIndex
from Components.LoginProcesses.login import UserLabel
import icons_rc
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout, QToolBar, QAction, QSplitter, QFileDialog,
                             QStatusBar, QDialog, QSizePolicy, QPushButton, QLineEdit, QDesktopWidget, QShortcut,
                             QVBoxLayout, QFrame,
                             QProxyStyle, QStyle, QSpacerItem, QMessageBox, QAbstractItemView, QListWidgetItem)
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.Qt import Qt, QTimer
from PyQt5.QtPrintSupport import QPrintDialog
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.Qsci import QsciPrinter
from PyQt5 import QtGui
from pathlib import Path

from codeeditor import CodeEditor
from tabwidget import TabWidget
from codeview import CodeView
from runthread import RunThread
from threading import Thread, Timer
from configuration import Configuration
from dialog import EnterDialog
from Components.TopMenu.Settings.settingsdialog import SettingsDialog
from Components.TopMenu.Settings.packagemanager import PMDialog
from Components.TopMenu.Help.glplicense import GPLDialog
from Components.TopMenu.Help.help import HelpDialog
from Components.ChatBotView.chatbotview import UcChatBotView
from Components.LeftMenu.Menus.uc_lm_menus import UcLMMenus
from Components.StartPage.recentmanager import RecentManager
from Components.LoginProcesses.login import LoginWindow
from Components.FindReplace.findreplacedialog import FindReplaceDialog
from Components.SyntaxChecker.SyntaxCheck import writeLog
from Components.ErrorConsole.errorconsole import ErrorConsole
# from pyqt5_material import apply_stylesheet
from configuration import Configuration
from Components.TopMenu.tabmenu import TabMenu
from Components.TopMenu.toolbar import ToolBar
from Components.ErrorConsole.error_outputs_to_db import error_outputs_to_db
from Components.ExamProcesses.examClassic import *

activePage = None

##LOGFUNC START
from datetime import datetime
import json
from PyQt5.QtGui import QKeySequence
import tempfile
import requests
import random

file_to_write = ""
main_pointer = None

def generate_system_id():
    mac_address = uuid.getnode()
    system_id = (mac_address & 0xffffffffff)
    return system_id

def initialize_log():
    c = Configuration()
    global file_to_write
    time = datetime.now()
    timestamp = time.strftime('%Y_%m_%d-%H_%M_%S.%f')[:-3]
    data_folder = os.path.dirname(os.path.realpath(__file__))
    data_folder = Path(data_folder)
    # data_folder = data_folder / "log"
    data_folder = data_folder / c.getLogFolder()
    try:
        data_folder.mkdir(parents=True, exist_ok=False)
    except Exception as err:
        pass
    file_to_write = data_folder / (str(generate_system_id()) + "-" + str(timestamp) + ".json")
    return file_to_write

# Tab menu hover button
class HoverButton(QtWidgets.QToolButton):
    def __init__(self, parent=None):
        super(HoverButton, self).__init__(parent)
        self.setStyleSheet('''QToolButton{border-image: url(":/icon/images/run_i.png")}''')
        self.setFixedWidth(55)
        self.setFixedHeight(55)
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

    def resizeEvent(self, event):
        self.setMask(QtGui.QRegion(self.rect(), QtGui.QRegion.Ellipse))
        QtWidgets.QToolButton.resizeEvent(self, event)


# CodeEditor Overwrite
class CodeEditor(CodeEditor):
    def __init__(self, parent=None, logAndInd=None, menus=None):
        super().__init__(parent)
        self.logAndInd = logAndInd
        self.menus = menus
        self.parent = self.parent()

    def paste(self):
        super().paste()
        logfunc("Yapıştır: " + QApplication.clipboard().text(), parent=self.parent)

    def keyPressEvent(self, event):
        prev_position = self.getCursorPosition()
        super().keyPressEvent(event)
        position = self.getCursorPosition()
        self.logAndInd.clearIndıcator(self)
        if (event.key() == Qt.Key_Tab):
            key_pressed = "TAB"
        elif (event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return):
            key_pressed = "ENTER"
            self.logAndInd.updateLines(self, prev_position, position)
        elif (event.key() == Qt.Key_Space):
            key_pressed = "SPC"
        elif (event.key() == Qt.Key_Alt):
            key_pressed = "ALT"
        elif (event.key() == Qt.Key_Home):
            key_pressed = "HOME"
        elif (event.key() == Qt.Key_Insert):
            key_pressed = "INSERT"
        elif (event.key() == Qt.Key_End):
            key_pressed = "END"
        elif (event.key() == Qt.Key_Delete):
            key_pressed = "DELETE"
            self.logAndInd.updateLines(self, prev_position, position)
        elif (event.key() == Qt.Key_Control):
            key_pressed = "CTRL"
        elif (event.key() == Qt.Key_Up):
            key_pressed = "UP"
        elif (event.key() == Qt.Key_Down):
            key_pressed = "DOWN"
        elif (event.key() == Qt.Key_Left):
            key_pressed = "LEFT"
        elif (event.key() == Qt.Key_Right):
            key_pressed = "RIGHT"
        elif (event.key() == Qt.Key_Escape):
            key_pressed = "ESC"
        elif (event.key() == Qt.Key_Backspace):
            key_pressed = "BCKSPC"
            self.logAndInd.updateLines(self, prev_position, position)
        else:
            key_pressed = event.text()
        MOD_MASK = (Qt.CTRL | Qt.ALT | Qt.META)
        modifiers = int(event.modifiers())
        if (
                modifiers and modifiers & MOD_MASK == modifiers and event.key() > 0 and event.key() != Qt.Key_Shift and event.key() != Qt.Key_Alt and event.key() != Qt.Key_Control and event.key() != Qt.Key_Meta):
            key_pressed = QKeySequence(modifiers + event.key()).toString()

        if "Ctrl" in key_pressed or "CTRL" in key_pressed or event.key() == 16777273:
            self.parent.tab_widget.PynarTabs.setCurrentIndex(0)
            if event.key() == 16777273:
                self.parent.interpreter()

        # Tus kombinasyonlarinda modifier tusu logda gozukmesin
        if (key_pressed == "Ctrl+V"):
            logfunc("Yapıştır: " + QApplication.clipboard().text(), parent=self.parent)
            return
        if (event.key() != Qt.Key_Shift and event.key() != Qt.Key_Alt and event.key() != Qt.Key_Control and event.key() != Qt.Key_Meta):
            t = "Basılan Tuş: " + key_pressed
            logfunc(t, parent=self.parent)

    def keyReleaseEvent(self, event):
        self.redoUndosetEnabled()

    def redoUndosetEnabled(self):
        self.parent.toolbar.redoAction.setEnabled(self.parent.textPad.isRedoAvailable())
        self.parent.toolbar.undoAction.setEnabled(self.parent.textPad.isUndoAvailable())


    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("text/plain"):
            if isinstance(event.source(),QTreeView) and self.menus.forceNewPage and len(self.text())>0:
                mess = "Sürüklemek istediğiniz sayfada yazılmış kodlar var. Bu kod örneğini çalıştırmak için <b> yeni bir sayfa</b> oluşturup o sayfaya <b>sürükleyebilirsiniz.</b>"
                self.mess = CustomizeMessageBox_Ok(mess, "critical", True)
                self.mess.show()
            else:
                event.accept()
        else:
            event.ignore()

    # Sürükleme log
    def dropEvent(self, event):
        super().dropEvent(event)
        message = "Sürükle: " + event.mimeData().text()
        self.move_cursor_to_end()
        logfunc(message, parent=self.parent)

    def move_cursor_to_end(self):
        pos = self.getCursorPosition()
        self.setCursorPosition(pos[0], pos[1])
        self.ensureCursorVisible()
        self.ensureLineVisible(pos[0])

    def messenger(self, string):
        logfunc(string, parent=self.parent)


    def mousePressEvent(self, event):
        super(CodeEditor, self).mousePressEvent(event)
        self.parent.tab_widget.PynarTabs.setCurrentIndex(0)

# Solmenü override
class UcLMMenus(UcLMMenus):
    def __init__(self, main=None, parent=None):
        super().__init__(parent)
        self.main = main

    def MenuActionClick(self, jsonFile, index, clean):
        super().MenuActionClick(jsonFile, index, clean)
        message = self.toolButtons[index].text()
        message = "Solmenü_Tıkla: " + message.replace("\n", "")
        logfunc(message, parent=self.main)


# QAction Overwrite
class QAction(QAction):
    def __init__(self, a=None, b=None, parent=None):
        self.a = a
        if parent:
            super().__init__(a, b, parent)
        elif b:
            super().__init__(b, parent)
        elif a:
            super().__init__(parent)
        # QAction her çalıştığında logfunction fonksiyonunu çalıştır
        self.triggered.connect(self.log_action)

    # Çalıştırılan QAction'ı log dosyasına kaydet.
    def log_action(self, extra=""):
        if (self.sender().text() == "Aç"):
            return
        message = "Eylem: " + self.sender().text()
        logfunc(message, parent=self.a)


# Loga yazma fonksiyonu
def logfunc(input_message, filestr="", error_grid_info="", parent=None):
    if (main_pointer.notebook.textPad == None):
        return
    c = Configuration()
    if (c.getLogEnabled() == "False" and c.getExamLogEnabled() == "False"):
        return
    text_size = len(main_pointer.notebook.textPad.text())
    line_count = main_pointer.notebook.textPad.lines()
    time = datetime.now()
    timestamp = time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]
    message = {'MachineId': str(generate_system_id()), 'time': timestamp, 'action': input_message,
               'totalchars': text_size, 'totallines': line_count}
    if (c.getLogEnabled() == "True"):
        if (filestr != ""):
            message['file'] = filestr
        if (error_grid_info != ""):
            message['hata listesi'] = error_grid_info
        checker = True
        if (not os.path.exists(file_to_write)):
            checker = False
            with open(file_to_write, 'w', encoding='utf-8') as file:
                file.write("[\n]")
        with open(file_to_write, 'rb+') as file:
            file.seek(0, 2)
            size = file.tell()
            file.truncate(size - 1)
        with open(file_to_write, "a+", encoding='utf-8') as file:
            if checker:
                file.write(',\n')
            json.dump(message, file, ensure_ascii=False, indent=4)
            file.write(']')

    if (c.getExamLogEnabled() == "True"):
        if parent !=None and parent.ExamWindow != None and parent.ExamWindow.isStarted == True:
            examLogFile = parent.ExamWindow.file_to_write

            if not os.path.exists(examLogFile):
                with open(examLogFile, 'w', encoding='utf-8') as file:
                    file.write("[\n]")
            with open(examLogFile, 'rb+') as file:
                file.seek(0, 2)
                size = file.tell()
                file.truncate(size - 1)
            with open(examLogFile, "a+", encoding='utf-8') as file:
                if os.path.getsize(examLogFile)>3:
                    file.write(',\n')

                json.dump(message, file, ensure_ascii=False, indent=4)
                file.write(']')


##LOGFUNC END

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.token = None
        self.ExamWindow = None
        self.openExam = None
        self.examList = []
        self.exCount = 0
        self.activeErrorCount = 0
        self.previousErrorCount = 0
        self.btnRun = HoverButton(self)
        self.splitter = QSplitter(Qt.Horizontal)
        self.hBoxLayout = QtWidgets.QHBoxLayout()
        self.loginWindow = None
        self.c = Configuration()
        # self.setObjectName("mainWidget")
        path = os.path.abspath(__file__)
        # self.HOME = os.path.dirname(path) + '/'
        self.setWindowIcon(QIcon(':/icon/images/headerLogo1.png'))

        # change to Home Path
        home = str(os.chdir(Path.home()))

        #LOG baslat, mainwindow pointeri ata
        self.log = initialize_log()
        global main_pointer
        main_pointer = self

        # self.fileBrowser = None
        self.initUI(self)
        self.centerOnScreen()

        helpAction = QAction(self)
        helpAction.setShortcut('F1')
        helpAction.triggered.connect(self.help)

        self.addAction(helpAction)
        self.rm = RecentManager()

        self.loginWindow = LoginWindow(self,self.lbl_img_user)
        self.loginWindow.readToken()
        self.setExamImage()

        self.time_left_int = int(self.c.getDurationExamsRefresh())
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.timerTimeout)
        self.timer.start(1000)

    def timerTimeout(self):
        self.time_left_int -= 1
        if self.time_left_int == 0:
            self.setExamImage()
            self.time_left_int = int(self.c.getDurationExamsRefresh())


    def setExamImage(self):
        self.fetchExams()
        img = ':/icon/images/exam.png'
        self.lbl_exam_text.setText('')
        if self.token is not None:
            self.exCount = self.getCount()
            img = ':/icon/images/exam_number.png'
            self.lbl_exam_text.setText(str(self.exCount))
        self.lbl_exam.setPixmap(QPixmap(img))

    def getCount(self):
        count = 0
        for k in self.examList:
            if k['started_at'] is None:
                contDateStart = datetime(*tuple([int(x) for x in k['start_date'][:10].split('-')]) + tuple( [int(x) for x in k['start_date'][11:].split(':')]))
                contDateStop = datetime(*tuple([int(x) for x in k['due_date'][:10].split('-')]) + tuple(  [int(x) for x in k['due_date'][11:].split(':')]))
                if contDateStart < datetime.now() and contDateStop > datetime.now():
                    count += 1
        return count

    def UserLoginClick(self, i=None):
        if i and i.text() == 'Hayır':
            return
        else:
            if self.loginWindow is None:
                self.loginWindow = LoginWindow(self,self.lbl_img_user)

            self.loginWindow.move(int(self.x() + (
                        self.lbl_img_user.width() * (self.width() / self.lbl_img_user.width())) - self.loginWindow.width()),
                                  int(self.y() + self.lbl_img_user.height() * 2))
            self.loginWindow.show()

    def initUI(self, MainWindow):
        self.header = QtWidgets.QMenuBar()
        self.header.setFixedHeight(120)
        self.header.setStyleSheet("""
            QMenuBar {background-color: #394b58;}
            QMenuBar::item {background-color: #394b58;}
            QMenu {icon-size: 80px;}
            QMenu::item {background: transparent;}
        """)
        self.header.setObjectName("header")
        MainWindow.setMenuBar(self.header)

        self.hBoxLayout.setObjectName("hBoxLayout")
        self.vBoxLayout = QtWidgets.QVBoxLayout(self.header)
        self.vBoxLayout.addLayout(self.hBoxLayout)

        self.lbl_img_logo = QtWidgets.QLabel(self.header)
        self.lbl_img_logo.setMaximumSize(QtCore.QSize(100, 95))
        self.lbl_img_logo.setMinimumSize(QtCore.QSize(100, 95))
        self.lbl_img_logo.setPixmap(QPixmap(':/icon/images/headerLogo1.png'))
        self.lbl_img_logo.setContentsMargins(10, 10, 0, 0)
        self.lbl_img_logo.setScaledContents(True)
        self.lbl_img_logo.setFixedWidth(85)
        self.lbl_img_logo.mouseReleaseEvent = lambda event: self.LogoClick()
        self.lbl_img_logo.setToolTip("Sürüm Bilgisi")
        self.lbl_img_logo.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.hBoxLayout.addWidget(self.lbl_img_logo)

        verticalSpacer = QSpacerItem(13, 40, QSizePolicy.Fixed, QSizePolicy.Expanding)

        self.hBoxLayout.addItem(verticalSpacer)

        self.tab_widget = TabMenu(MainWindow)
        self.tab_widget.setMinimumWidth(935)  # self.tab_widget.setFixedWidth(850)
        self.tab_widget.setFixedHeight(125)
        self.hBoxLayout.addWidget(self.tab_widget)

        self.btnRun.setObjectName("btnRun")
        self.btnRun.setToolTip('Çalıştır')
        self.btnRun.setShortcut('F12')
        self.btnRun.clicked.connect(self.run)
        self.hBoxLayout.addWidget(self.btnRun)


        self.lbl_exam = UserLabel()
        self.lbl_exam_text = QLabel(self.lbl_exam)
        self.lbl_exam_text.setGeometry(25, 0, 25, 20)
        self.lbl_exam_text.setAlignment(Qt.AlignCenter)
        self.lbl_exam.setPixmap(QPixmap(':/icon/images/exam.png'))
        self.lbl_exam.setStyleSheet("")

        self.lbl_exam.setStyleSheet(""" QLabel{background-color:transparent; font-size: 20px; color:#ffffff;}
                                        QToolTip { background-color: white;color: black;border: black solid 1px}""")
        self.lbl_exam.setToolTip("Sınavlarınız")

        self.lbl_exam.setMaximumSize(QtCore.QSize(55, 55))
        self.lbl_exam.setMinimumSize(QtCore.QSize(55, 55))
        self.lbl_exam.setScaledContents(True)
        self.lbl_exam.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.hBoxLayout.addWidget(self.lbl_exam)
        self.hBoxLayout.setContentsMargins(0, 0, 10, 0)
        self.lbl_exam.clicked.connect(self.exams)
        self.lbl_img_user = UserLabel(self.header)
        self.lbl_img_user.setMaximumSize(QtCore.QSize(55, 55))
        self.lbl_img_user.setMinimumSize(QtCore.QSize(55, 55))
        self.lbl_img_user.setPixmap(QPixmap(':/icon/images/user.png'))
        self.lbl_img_user.setScaledContents(True)
        self.lbl_img_user.setToolTip("Kullanıcı Girişi")

        self.lbl_img_user.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.hBoxLayout.addWidget(self.lbl_img_user)
        self.hBoxLayout.setContentsMargins(0,0,10,0)
        self.lbl_img_user.clicked.connect(self.UserLoginClick)

        self.hBoxLayout2 = QtWidgets.QHBoxLayout()
        self.hBoxLayout2.setObjectName("hBoxLayout2")
        lbl1 = QtWidgets.QLabel()
        lbl1.setStyleSheet("background-color:#acd33b;")
        self.hBoxLayout2.addWidget(lbl1)
        self.hBoxLayout2.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.addLayout(self.hBoxLayout2)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)

        #MainWindow.resize(1600, 900)
        MainWindow.setMinimumSize(QtCore.QSize(1250, 800))

        self.setWindowTitle('PyNar Kod Editörü')

        # ---------------------------------------
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.setStyleSheet("QSplitter::handle{width: 0px; height: 0px; border:none}")
        self.splitterV = QSplitter(Qt.Vertical)
        self.splitterV.setStyleSheet("QSplitter::handle{width: 0px; height: 0px; border:none}")
        # -------------------------------------------
        # widgets
        self.notebook = TabWidget(self)
        self.codeView = CodeView(self, self.notebook)
        self.menus = UcLMMenus(main=self, parent=self.notebook)
        self.menus.solGenislik(self.menus)
        self.chatbotview = UcChatBotView(self)
        self.chatbotview.setFixedWidth(335)
        self.notebook.newTab(codeView=self.codeView)

        # ------------------------------------------------------
        self.notebook.currentChanged.connect(self.tabChanged)
        self.notebook.closingTab.connect(self.tabClosed)
        # -------------------------------------------
        self.textPad = self.notebook.textPad

        # --------------------------------------------
        self.errorConsole = ErrorConsole()

        self.splitterV.addWidget(self.notebook)
        self.splitterV.addWidget(self.errorConsole)
        self.splitterV.setStyleSheet("border:none")
        self.splitterV.handle(0).setEnabled(True)
        self.splitterV.handle(1).setEnabled(False)
        self.splitterV.setSizes([0, 0])

        self.splitterV.splitterMoved.connect(self.errorMoved)
        # --------------------------------------------

        # Chatbot kapandığında sağ taraftaki chatbot ikonu görüntülenir..
        self.label_robot = QtWidgets.QLabel()
        self.label_robot.setObjectName("LabelFold")
        self.label_robot.mousePressEvent = self.closeChatBotView
        self.chatbotview.form.setVisible(False)
        pixmap = QtGui.QPixmap(":/icon/images/robot-rotate.png")
        pixmap2 = pixmap.scaled(pixmap.width() // 3, pixmap.height() // 3)
        self.label_robot.setPixmap(pixmap2)
        self.label_robot.setAlignment(Qt.AlignTop)
        # self.label_robot.setVisible(True)


        self.splitter.addWidget(self.menus)
        self.splitter.addWidget(self.splitterV)
        self.splitter.addWidget(self.label_robot)
        self.splitter.addWidget(self.chatbotview)
        # self.splitter.setStyleSheet("border:none")
        self.splitter.handle(1).setEnabled(False)
        self.splitter.handle(2).setEnabled(False)

        hbox = QHBoxLayout()
        hbox.addWidget(self.splitter)
        self.splitter.setStretchFactor(1, 10)
        self.setCentralWidget(self.splitter)

        # log
        self.logAndInd = writeLog(self, os.path.dirname(os.path.realpath(__file__)), self.errorConsole, self.splitterV)
        self.logAndInd.closeButton.pressed.connect(self.closeErrorConsole)

        # Dosya toolbar oluşturuluyor..
        self.toolbar = ToolBar(MainWindow, self.tab_widget)

        # Skip(Atla) butonuna basıldığında toolbar menu butonlarını pasif eder.
        self.changeToolbarButtonActive(False)

        # make statusbar
        self.statusBar = QStatusBar()
        self.statusBar.setMinimumHeight(30)
        self.statusBar.setObjectName("mainStatusBar")
        self.setStatusBar(self.statusBar)

        statusBtn = QPushButton()
        statusBtn.move(120, 70)
        statusBtn.resize(100, 40)
        statusBtn.setText("Kısayollar")
        statusBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        statusBtn.clicked.connect(self.statusBtnClick)
        statusBtn.setStyleSheet("QPushButton{background-color:rgb(0, 96, 132);color: white; border:none}")

        resetFontSc = QShortcut(QKeySequence('Ctrl+G'), self)
        resetFontSc.activated.connect(self.fontReset)

        self.statusBar.addPermanentWidget(statusBtn)
        self.errorToDb = error_outputs_to_db()
        self.isNewPythonFile = False

    def fontReset(self):
        mess = "Pynar editör font ayarları varsayılan hale getirilecek ve editör yeniden başlatılacaktır devam etmek istiyor musunuz?"
        CustomizeMessageBox_Yes_No(mess, clickAccept=self.fontResetClick, yes='Evet', no='Hayır', icon="information")

    def fontResetClick(self):
        self.c.setCodeFont("Consolas")
        self.c.updateConfig('Size', 'size', str("16"))

        self.c.setEditorFont("Tahoma")
        self.c.updateConfig('Size', 'editorsize', str("10"))

        QtCore.QCoreApplication.quit()
        pynarBasePath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
        status = QtCore.QProcess.startDetached(pynarBasePath + os.sep + "pynar")

    def statusBtnClick(self):
        message = """<font color=gray><table border=0 bordercolor=\"#acd33b\" cellspacing=\"0\" cellpadding=\"2\">
                  <tr><th>Tuş Kombinasyonu </th><th> Görevi </th></tr>
                  <tr><td>CTRL ve X </td><td> Kes </td></tr>
                  <tr><td>CTRL ve V </td><td> Yapıştır </td></tr>
                  <tr><td>CTRL ve Z </td><td> Geri Al </td></tr>
                  <tr><td>CTRL ve K </td><td> Yorum satırı yap</td></tr>
                  <tr><td>CTRL ve N </td><td> Yeni Sekme Oluştur</td></tr>
                  <tr><td>CTRL ve O </td><td> Python Kodu Aç</td></tr>
                  <tr><td>CTRL ve H </td><td> Dosya geçmişi</td></tr>
                  <tr><td>CTRL ve F </td><td> Bul ve Değiştir</td></tr>
                  <tr><td>CTRL ve W </td><td> Sekmeyi Kapat</td></tr>
                  <tr><td>CTRL ve P </td><td>  Yazdır</td></tr>
                  <tr><td>CTRL ve S </td><td> Kaydet</td></tr>
                  <tr><td>CTRL ve + </td><td> Yakınlaştır</td></tr>
                  <tr><td>CTRL ve - </td><td> Uzaklaştır</td></tr>
                  <tr><td>CTRL ve G </td><td> Font ayarlarını sıfırla</td></tr>
                  <tr><td>CTRL ve SHIFT ve S </td><td>  Farklı Kaydet</td></tr>
                  <tr><td>CTRL ve SHIFT ve Z </td><td> İleri al</td></tr></table></font>"""

        CustomizeMessageBox_Yes_No(message, clickCancel=self.detailInfoClick, yes='Tamam', no='Detaylı Bilgi',
                                           icon="information")

    def detailInfoClick(self):
        c = Configuration()
        view = QWebEngineView()
        dosyaPath = c.getHomeDir() + c.getHtmlHelpPath("html_help_path")
        url = QtCore.QUrl.fromLocalFile(dosyaPath + 'PyNarKilavuz/Yardim_Bolum2.html')
        url.setFragment('klavye-kısayolları')
        view.load(url)
        self.helpDialog = HelpDialog(self, view)
        self.helpDialog.show()

    def LogoClick(self):
        self.showReleaseInfo()

    def closeChatBotView(self, event):
        isVisible = self.chatbotview.closeForm()
        if isVisible:  # chatbot ekranı açık ise label ı gizle
            self.label_robot.setVisible(False)
        else:
            self.label_robot.setVisible(True)

    def changeToolbarButtonActive(self, activeState):
        self.toolbar.changeToolbarButtonActive(activeState)
        self.btnRun.setEnabled(activeState)

    def errorMoved(self, pos, index):
        size = self.splitterV.sizes()
        if (size[1] == 0):
            self.logAndInd.clearIndıcator(self.textPad)

    def tabChanged(self):
        try:
            self.logAndInd.newErrorConsole(self.textPad)
        except:
            pass

    def tabClosed(self):
        self.logAndInd.removeError(self.notebook.textPad)

    def closeErrorConsole(self):
        self.logAndInd.closePressed(self.textPad)

    def new(self):
        if self.ExamWindow is None or self.ExamWindow.isStarted == False:
            editor = CodeEditor(parent=self, logAndInd=self.logAndInd, menus=self.menus)
            editor.filename = None
            self.notebook.newTab(editor)
            x = self.notebook.count()
            index = x - 1
            self.notebook.setCurrentIndex(index)
            self.textPad = editor
            self.notebook.textPad = editor
            self.mainWindow = self.textPad.mainWindow
            self.changeToolbarButtonActive(True)
        else:
            mess = "Aktif Sınavınız varken yeni pencere açamazsınız"
            CustomizeMessageBox_Ok(mess, "critical")

    def close(self):
        self.notebook.closeTab(self.notebook.currentIndex())

    def open(self, starter=None, getPath=None):
        self.isNewPythonFile = True
        if self.ExamWindow is None or self.ExamWindow.isStarted == False:
            dialog = QFileDialog(self)
            dialog.setViewMode(QFileDialog.List)

            if plt == "Windows":
                documents_dir = os.path.join(os.environ['USERPROFILE'] + "/Documents/PynarKutu/")
            elif plt == "Linux":
                documents_dir = subprocess.check_output(["xdg-user-dir", "DOCUMENTS"], universal_newlines = True).strip() + "/PynarKutu"

            if not os.path.exists(documents_dir):
                os.makedirs(documents_dir)

            if starter:
                filePath = getPath
                filename = (filePath, "*")
            else:
                filename = dialog.getOpenFileName(self, "Aç", documents_dir, filter="Python scripts (*.py)")

            ret = self.openFile(filename[0])
            return ret
        else:
            mess = "Aktif Sınavınız varken yeni pencere açamazsınız"
            CustomizeMessageBox_Ok(mess, "critical")

        self.isNewPythonFile = False

    def openPythonFiles(self, starter=None, getPath=None):
        self.isNewPythonFile = True
        if self.ExamWindow is None or self.ExamWindow.isStarted == False:
            dialog = QFileDialog(self)
            dialog.setViewMode(QFileDialog.List)

            if plt == "Windows":
                documents_dir = os.path.join(os.environ['USERPROFILE'] + "/Documents/PynarKutu/")
            elif plt == "Linux":
                documents_dir = subprocess.check_output(["xdg-user-dir", "DOCUMENTS"], universal_newlines = True).strip() + "/PynarKutu"

            if not os.path.exists(documents_dir):
                os.makedirs(documents_dir)

            if starter:
                filePath = getPath
                filename = (filePath, "*")
            else:
                filename = dialog.getOpenFileNames(self, "Aç", documents_dir, filter="Python scripts (*.py)")

            for file in filename[0]:
                self.openFile(file)
        else:
            mess = "Aktif Sınavınız varken yeni pencere açamazsınız"
            CustomizeMessageBox_Ok(mess, "critical")

        self.isNewPythonFile = False

    def openFile(self, filePath):
        if self.ExamWindow is None or self.ExamWindow.isStarted == False:
            filePath = filePath
            try:
                with open(filePath, 'r', encoding='utf-8') as f:
                    text = f.read()

                editor = CodeEditor(self, logAndInd=self.logAndInd, menus=self.menus)
                editor.setText(text)
                editor.filename = filePath

                self.notebook.newTab(editor)
                x = self.notebook.count()  # number of tabs
                index = x - 1
                self.notebook.setCurrentIndex(index)

                tabName = os.path.basename(editor.filename)
                self.notebook.setTabText(x, tabName)
                # self.textPad = editor
                self.notebook.textPad = editor
                self.textPad = self.notebook.textPad

                self.rm.addItem(tabName, filePath)

                #Log open action
                logfunc("Eylem: Aç", str(filePath), parent=self)
                #

            except Exception as e:
                self.statusBar.showMessage(str(e), 3000)

            self.changeToolbarButtonActive(True)
            return True
        else:
            mess = "Aktif Sınavınız varken yeni pencere açamazsınız"
            CustomizeMessageBox_Ok(mess, "critical")

    def save(self):
        filename = self.textPad.filename
        index = self.notebook.currentIndex()
        tabText = self.notebook.tabText(index)

        if not filename:
            self.saveAs()

        else:
            text = self.textPad.text()
            try:
                with open(filename, 'w', newline='',
                          encoding='utf-8') as file:  # dosyaya boş satır eklemeyi önlemek için newline='' olarak atandı
                    file.write(text)
                    self.statusBar.showMessage(filename + " kaydedildi", 3000)

                    # remove '*' in tabText
                    fname = os.path.basename(filename)
                    self.notebook.setTabText(index, fname)

                    self.rm.addItem(fname, filename)

            except Exception as e:
                self.statusBar.showMessage(str(e), 3000)
                self.saveAs()

    def saveAs(self):
        dialog = QFileDialog(self)
        dialog.setViewMode(QFileDialog.List)

        if plt == "Windows":
            documents_dir = os.path.join(os.environ['USERPROFILE'] + "/Documents/PynarKutu/")
        elif plt == "Linux":
            documents_dir = subprocess.check_output(["xdg-user-dir", "DOCUMENTS"], universal_newlines = True).strip() + "/PynarKutu"

        if not os.path.exists(documents_dir):
            os.makedirs(documents_dir)

        filename = dialog.getSaveFileName(self, "Kaydet", documents_dir, "Python scripts (*.py)")

        if filename[0]:
            fullpath = filename[0]
            text = self.textPad.text()
            if(not fullpath.endswith(".py")):
                fullpath += ".py"
            try:
                with open(fullpath, 'w', newline='',
                          encoding='utf-8') as file:  # dosyaya boş satır eklemeyi önlemek için newline='' olarak atandı
                    file.write(text)
                    self.statusBar.showMessage(fullpath + " kaydedildi", 3000)

                    # update all widgets

                    self.textPad.filename = fullpath
                    self.refresh(self.textPad)
                    # self.fileBrowser.refresh()
                    fname = os.path.basename(fullpath)
                    index = self.notebook.currentIndex()
                    self.notebook.setTabText(index, fname)

                    self.rm.addItem(fname, fullpath)
            except Exception as e:
                self.statusBar.showMessage(str(e), 3000)

        else:
            self.statusBar.showMessage('Dosya kayıt edilemedi !', 3000)

    def saveAsExample(self):

        dialog = QFileDialog(self)
        dialog.setViewMode(QFileDialog.List)

        if plt == "Windows":
            documents_dir = os.path.join(os.environ['USERPROFILE'] + "/Documents/PynarKutu/")
        elif plt == "Linux":
            documents_dir = subprocess.check_output(["xdg-user-dir", "DOCUMENTS"], universal_newlines = True).strip() + "/PynarKutu"

        if not os.path.exists(documents_dir):
            os.makedirs(documents_dir)

        if plt == "Windows":
            dialog.setDirectory(os.path.join(os.environ['USERPROFILE'] + "/Documents/PynarKutu/"))
            self.logPath = os.path.abspath(os.path.dirname(os.environ['USERPROFILE'] + "/Documents/PynarKutu/"))
        elif plt == "Linux":
            dialog.setDirectory(os.path.join(os.environ['HOME'] + "/Documents/"))
            self.logPath = os.path.abspath(os.path.dirname(os.environ['HOME'] + "/Documents/PynarKutu/"))


        init_filename = os.path.join(self.logPath, "merhabadunya.py")
        saveList = dialog.getSaveFileName(self, "Kaydet", init_filename, "Python scripts (*.py)")
        self.text = """print("Merhaba Dünya")"""

        if saveList[0]:
            self.fullpath = saveList[0]
            if(not self.fullpath.endswith(".py")):
                self.fullpath += ".py"
            try:
                with open(self.fullpath, 'w', newline='',
                          encoding='utf-8') as file:  # dosyaya boş satır eklemeyi önlemek için newline='' olarak atandı
                    file.write(self.text)
                    self.statusBar.showMessage(self.fullpath + " kaydedildi", 3000)

                with open(self.fullpath, 'r', encoding='utf-8') as f:
                    text = f.read()

                editor = CodeEditor(self, logAndInd=self.logAndInd, menus=self.menus)
                editor.setText(text)
                editor.filename = self.fullpath

                self.notebook.newTab(editor)
                x = self.notebook.count()  # number of tabs
                index = x - 1
                self.notebook.setCurrentIndex(index)

                tabName = os.path.basename(editor.filename)
                self.notebook.setTabText(x, tabName)
                # self.textPad = editor
                self.notebook.textPad = editor
                self.textPad = self.notebook.textPad

                self.rm.addItem(tabName, self.fullpath)
                self.changeToolbarButtonActive(True)
                return True
            except Exception as err:
                print(err)
                return False
        return False

    def onPrint(self):
        doc = QsciPrinter()
        dialog = QPrintDialog(doc, self)
        dialog.setWindowTitle('Print')

        if (dialog.exec_() == QDialog.Accepted):
            self.textPad.setPythonPrintStyle()
            try:
                doc.printRange(self.textPad)
            except Exception as e:
                print(str(e))

        else:
            return

        self.textPad.setPythonStyle()

    def undo(self):
        self.textPad.undo()
        self.textPad.redoUndosetEnabled()

    def redo(self):
        self.textPad.redo()
        self.textPad.redoUndosetEnabled()

    def zoomIn(self):
        self.textPad.zoomIn()

    def zoomOut(self):
        self.textPad.zoomOut()

    def history(self):
        self.historyWindow = QDialog()
        self.historyWindow.setWindowFlags(Qt.FramelessWindowHint | Qt.Popup)
        self.historyWindow.setMinimumSize(QSize(415, 218))
        self.historyWindow.setMaximumSize(QSize(415, 218))

        self.historyLayout = QtWidgets.QHBoxLayout()
        self.scrollArea = QtWidgets.QScrollArea()

        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.gridLayoutHistory = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.historyLayout.addWidget(self.scrollArea)

        self.font_history_menu = QFont()
        self.font_history_menu.setFamily(self.c.getEditorFont())
        self.font_history_menu.setPointSize(self.c.getHistoryMenuFontSize() + 6)
        self.font_history_menu.setWeight(75)

        self.lbl_title_recent = QtWidgets.QLabel()
        self.lbl_title_recent.setObjectName("lblTitleRecent")
        self.lbl_title_recent.setText("Son Kullanılan Dosyalar")
        self.lbl_title_recent.setStyleSheet('color:#0070ba;')
        self.lbl_title_recent.setFont(self.font_history_menu)
        self.lbl_title_recent.setContentsMargins(0, 0, 0, 0)
        self.gridLayoutHistory.addWidget(self.lbl_title_recent, 0, 0)

        self.lw_recent = QtWidgets.QListWidget()
        self.lw_recent.setMinimumWidth(400)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lw_recent.sizePolicy().hasHeightForWidth())
        self.lw_recent.setSizePolicy(sizePolicy)
        self.lw_recent.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lw_recent.itemClicked.connect(self.onClickRecentItem)
        self.lw_recent.setStyleSheet("QListWidget{ background-color: #f0f0f0;}QListWidget::item{}QListWidget::item:hover{background-color:#d0d7da;}; ")
        self.lw_recent.setSelectionMode(QAbstractItemView.NoSelection)
        self.gridLayoutHistory.addWidget(self.lw_recent, 0, 0)


        self.rm = RecentManager()
        self.loadRecents()

        if self.lw_recent.count() == 0:
            self.emptyrecent = UcEmptyRecent(self.historyWindow)
            rightVLayout = QtWidgets.QVBoxLayout(self.historyWindow)
            rightVLayout.addWidget(self.emptyrecent)
        else:
            rightVLayout = QtWidgets.QVBoxLayout(self.historyWindow)
            rightVLayout.addWidget(self.lbl_title_recent)
            rightVLayout.addWidget(self.lw_recent)
            rightVLayout.setStretch(1, 2)
            rightVLayout.setSpacing(10)
        self.historyWindow.move(self.geometry().x()+240, self.geometry().y()+107)
        self.historyWindow.exec()

    def onClickRecentItem(self, item):
        p = item.data(QtCore.Qt.UserRole)
        self.removeItemPath = str(p['filepath'])
        if os.path.exists(self.removeItemPath):
            self.openFile(self.removeItemPath)
            self.historyWindow.close()
        else:
            mess = "<b>Dosya bulunamadı </br><b>Son kullanılan dosyalar listesinden çıkarmak ister misiniz ?"
            CustomizeMessageBox_Yes_No(mess, clickAccept=self.removeItemClick)

    def removeItemClick(self):
        if self.rm.removeItem(self.removeItemPath):
            self.loadRecents()

    def loadRecents(self):
        self.rm.removeAllItemNotExist()
        try:
            self.lw_recent.clear()
            self.c = Configuration()
            jsonFile = self.c.getHomeDir() + self.c.getJsonPath("recentJson")

            if not os.path.exists(jsonFile):
                self.rm.createRecentJson()

            with open(jsonFile) as json_file:
                data = json.load(json_file)

                for p in data['files']:
                    recentItem = UcSpRecentItem(self)
                    recentItem.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

                    if len(p['filename']) > 28:
                        p['filename'] = p['filename'][:25] + "..."
                    if len(p['filepath']) > 75:
                        p['filepath'] = p['filepath'][:75] + "..."

                    recentItem.setValue(p['filename'], p['filepath'], p['opendate'])

                    item = QListWidgetItem(self.lw_recent)

                    item.setData(QtCore.Qt.UserRole, p)
                    item.setSizeHint(recentItem.sizeHint())
                    self.lw_recent.addItem(item)
                    self.lw_recent.setItemWidget(item, recentItem)
        except Exception as err:
            print("error: {0}".format(err))

        self.lw_recent.setCurrentIndex(QModelIndex())

    def showSettings(self):
        try:
            dialog = SettingsDialog(self, self.textPad)
            dialog.setModal(False)
            dialog.exec_()
        except Exception as err:
            print("error show settings: {0}".format(err))

    def showPackage(self):
        try:
            PMDialog(self, self.textPad)
            #dialog = PMDialog(self, self.textPad)
            #dialog.exec_()
        except Exception as err:
            print("error show package: {0}".format(err))

    def showLicense(self):
        try:
            c = Configuration()
            view = QWebEngineView()
            dosyaPath = c.getHomeDir() + c.getLicenseFiles("license_files")
            view.load(QtCore.QUrl.fromLocalFile(dosyaPath + 'license.html'))

            dialog = GPLDialog(self, view)
            dialog.exec_()

        except Exception as err:
            print("error show license: {0}".format(err))

    def showHelp(self):
        try:
            c = Configuration()
            view = QWebEngineView()
            dosyaPath = c.getHomeDir() + c.getHtmlHelpPath("html_help_path")
            view.load(QtCore.QUrl.fromLocalFile(dosyaPath + 'PyNarKilavuz/index.html'))

            self.dialog = HelpDialog(self, view)
            self.dialog.show()

        except Exception as err:
            print("error show license: {0}".format(err))

    # Buluta Gönder
    def sendCloud(self):
        try:
            self.loginWindow.uploadCloud(self.textPad, self.log)
            if self.loginWindow.returnValue == 1:
                filename = self.textPad.filename
                index = self.notebook.currentIndex()
                fname = os.path.basename(filename)
                self.notebook.setTabText(index, fname)
                self.rm.addItem(fname, filename)
            elif self.loginWindow.returnValue == 2:
                os.remove(self.textPad.filename)
                self.textPad.filename = None
        except Exception as err:
            print("error show settings: {0}".format(err))


    # Buluttan İndir
    def installCloud(self):
        try:
            self.loginWindow.downloadCloud()
        except Exception as err:
            print("error show settings: {0}".format(err))

    # Öğretmene Gönder
    def sendTeacher(self):
        try:
            self.loginWindow.teacherUpCloud(self.textPad)
            if self.loginWindow.returnValue == 1:
                filename = self.textPad.filename
                index = self.notebook.currentIndex()
                fname = os.path.basename(filename)
                self.notebook.setTabText(index, fname)
                self.rm.addItem(fname, filename)
            elif self.loginWindow.returnValue == 2:
                os.remove(self.textPad.filename)
                self.textPad.filename = None
        except Exception as err:
            print("error show settings: {0}".format(err))

    # Pynar Kutusu
    def pynarBox(self):
        import subprocess
        c = Configuration()
        try:
            if c.getSystem() == "windows":
                box_path = os.path.expanduser("~\Documents\PynarKutu")
                if not os.path.exists(box_path):
                    os.makedirs(box_path)
                subprocess.call("explorer " + box_path, shell = True)
            else:
                box_path = subprocess.check_output(["xdg-user-dir", "DOCUMENTS"], universal_newlines = True).strip()
                if not os.path.exists(box_path + "/PynarKutu"):
                    os.makedirs(box_path + "/PynarKutu")
                subprocess.call(["xdg-open", box_path + "/PynarKutu"])
        except Exception as err:
            print("openLogFolder {0}".format(err))


    def interpreter(self):
        c = Configuration()
        system = c.getSystem()
        python_exe = c.getSelectedPythonExe()
        command = c.getInterpreter(system).format(python_exe)
        thread = RunThread(command)
        thread.start()

    def flowchart(self):
        self.save()
        if self.textPad.filename is not None and self.textPad.filename != '':
            source = open(self.textPad.filename, 'r', encoding="utf-8").read()
            try:
                f = FlowchartMaker(source)
                if f.isExcept:
                    CustomizeMessageBox_Ok("Akış Şeması Oluşturulamadı. Lütfen yazdığınız kodda hata olmamasına dikkat ediniz.","critical")
                else:
                    f.show()
            except Exception as err:
                print("error flowchart: {0}".format(err))
                
    def debugger(self):
        self.save()
        c = Configuration()
        system = c.getSystem()
        python_exe = c.getSelectedPythonExe()
        command = c.getRun(system).format(self.textPad.filename, python_exe)


        if self.textPad.filename is not None and self.textPad.filename != '':
            source = open(self.textPad.filename, 'r', encoding="utf-8").read()
            try:
                compile(source, '<string>', 'exec', dont_inherit=True)

                breakpointLine = self.notebook.getCurrentTextPad().breakpointLine
                if breakpointLine is not None:
                    breakpointLine_code = self.textPad.text()
                    gui_libs=['appjar','pyqt','tkinter']
                    if any(x in breakpointLine_code.lower() for x in gui_libs): #gui kodlarda pencere kapatılmazsa pdb devam etmiyor.
                        mess = "Bu kodlar <b>PyQt, Tkinter, AppJar</b> gibi görsel bileşenler içerdiği için hata ayıklayıcının bir sonraki satıra devam edebilmesi için kod çalıştırma sırasında oluşan pencerenin kapatılması gerekmektedir. Pencere kapatılmaz ise kod bir sonraki satıra ilerlemez !"
                        CustomizeMessageBox_Ok(mess, "information")
                        #return
                    c = Configuration()
                    system = c.getSystem()
                    python_exe = c.getSelectedPythonExe()


                    pdbrc_file_path = Path(os.path.expanduser("~") + os.sep + ".pdbrc")
                    pdbrc_file_content = """
        m=  "-------------------------------------------------\\n"
        m=m+"|    iLK {0} SATIR CALISTI...                     |\\n"
        m=m+"|    DEVAM iCiN c ve enter TUSUNA ...           |\\n"
        m=m+"|    CIKIS iCiN q TUSUNA BASINIZ.               |\\n"
        m=m+"-------------------------------------------------\\n"
        !(lambda: exec(\'import gc, pdb; next(o for o in gc.get_objects() if isinstance(o, pdb.Pdb)).prompt = \">> \"\',##))()
        b {1}
        !print('=================PROGRAM CIKTISI=================')
        {2}
        !print(m)
        """
                    with open(pdbrc_file_path, 'w', encoding='utf-8') as file:
                        file.write(pdbrc_file_content.format(breakpointLine-1,breakpointLine,'c' if breakpointLine!=1 else '').replace('##','{}'))
                    command = c.getInterpreter(system).format(python_exe)+ ' -m pdb ' + self.textPad.filename
                    thread = RunThread(command)
                    thread.start()

                else:
                    mess = "Hata ayıklayıcıyı çalıştırmak için lütfen bir satırı işaretleyiniz!\n\nKodlarınız işaretlediğiniz satıra kadar çalışacak ve  işaretli satırda bekleyecektir.\n\nBir satırı işaretlemek için satır numarasının bitimindeki boş alana tıklayınız. Kırmızı Ok sembolü göründüğünde işaretlenmiş olacaktır."
                    CustomizeMessageBox_Ok(mess, "critical")

            except:
                mess= "Debug etmek istediğiniz kodlarda hata bulunmaktadır, lütfen hataları düzelterek tekrar deneyiniz!"
                CustomizeMessageBox_Ok(mess, "critical")
                self.run()

    def terminal(self):
        c = Configuration()
        system = c.getSystem()
        command = c.getTerminal(system)

        thread = RunThread(command)
        thread.start()

    def run(self):
        self.errorConsole.message = None
        self.errorConsole.clear()
        self.splitterV.handle(1).setEnabled(True)
        self.save()
        c = Configuration()
        system = c.getSystem()
        python_exe = c.getSelectedPythonExe()
        command = c.getRun(system).format(self.textPad.filename,python_exe)
        #Kodun içinde syntax hatası varmı compile ederek kontrol et, hata varsa cmd minimize olsun
        #Hata yok ise cmd görünsün, runtime hatalarında işe yaramaz.
        if not self.textPad.filename:
            self.statusBar.showMessage("Dosya adı olmadan çalıştırılamaz!", 3000)
            return
        source = open(self.textPad.filename, 'r', encoding="utf-8").read()
        try:
            compile(source, '<string>', 'exec', dont_inherit=True)
        except:
            command = command.replace("cmd.exe", "/min cmd.exe")

        if not self.textPad.filename:
            self.statusBar.showMessage("Dosya adı olmadan çalıştırılamaz!", 3000)
            return
        self.logAndInd.clearIndıcator(self.textPad)
        logfunc("Eylem: Çalıştır", self.textPad.filename, parent=self)

        thread = Thread(target=self.command(command, tempfile.gettempdir() + "/hata.txt"), daemon=True)
        thread.start()
        logFile = Thread(target=self.logAndInd.parser(self.textPad), daemon=True)
        logFile.start()
        self.timer = QTimer()
        self.timer.timeout.connect(lambda: self.showMessage(self.textPad, tempfile.gettempdir() + "/hata.txt"))
        self.timer.start(1)

        self.currentErrorsChange()
        if self.errorConsole.tableWidget.rowCount() > 0:
            self.styntaxError = True
        else:
            self.styntaxError = False

        if self.activeErrorCount == 0 and self.previousErrorCount > 0:
            self.chatbotview.ErrorButtonsClear(chatClear=True)

        if not self.isRun and self.logAndInd.cmdControl == 2:
            mess = "<font color=gray>Şu an çalışmakta olan kod penceresi kapatılmadan aynı kod tekrar çalıştırılamaz!<br/><br/>Çalışmakta olan uygulamalara ait pencereleri kapatıp tekrar deneyiniz..</font>"
            CustomizeMessageBox_Ok(mess, "critical")

    def command(self, command, directory):
        self.isRun = True
        if os.path.isfile(directory):
            try:
                if not self.is_file_in_use(directory):
                    os.remove(directory)
                else:
                    self.isRun = False

            except Exception as err:
                pass
        if self.isRun:
            os.system(command)

    def is_file_in_use(self, file_path):
        path = Path(file_path)
        try:
            path.rename(path)
        except PermissionError:
            return True
        else:
            return False

    def showMessage(self, textpad, directory):
        file = textpad.filename
        if os.path.isfile(directory):
            if os.path.getsize(directory) != 0:
                try:
                    with open(directory, "r", encoding='utf-8') as f:
                        errorMessage = f.read()
                    os.remove(directory)
                    if errorMessage[-2:] != "^C":
                        self.errorToDb.writeNewLog(file, errorMessage)
                        if self.logAndInd.cmdControl == 2:
                            message = self.logAndInd.showCmdMessage(errorMessage, textpad)
                            # Runtime hatası loglama
                            # Loglama fonksiyonuna gönderim için bilgilerin json formatına dönüştürülmesi gerekli, ve bunun parse ile aynı formatta olması lazım.
                            # Öncelikle satir bilgisinin başladığı ve bittiği yerleri bulup buradan bu bilgiyi al
                            if message != None:
                                line_start = errorMessage.find("line ") + 5
                                line_end = errorMessage[line_start:].find(",") + line_start
                                satir_bilgisi = errorMessage[line_start:line_end]
                                # Sonra json yapısını oluştur
                                hata_listesi_diagnostic = {}
                                # Diğer fonksiyon ile uyumlu olacak şekilde json'u yapılandır
                                hata_listesi_diagnostic['file'] = textpad.filename
                                hata_listesi_diagnostic['message'] = str(message)
                                hata_listesi_diagnostic['satir'] = satir_bilgisi
                                hata_listesi = {}
                                hata_listesi['diagnostics'] = []
                                hata_listesi['diagnostics'].append(hata_listesi_diagnostic)
                                # Son halindeki json yapsını log fonksiyonuna gönder
                                self.errorgridlog(hata_listesi)
                            # log end
                        self.timer.stop()
                except:
                    self.timer.start(1)
            else:
                self.timer.start(1)
        else:
            self.timer.start(1)
        if not self.styntaxError:
            self.currentErrorsChange()
        if self.errorConsole.message is not None and self.activeErrorCount > 0 and self.c.getChatbotStatusEnabled() == "True":
            self.chatbotAddErrorMessage(self.errorConsole.message)
            self.timer.stop()
        else:
            if self.chatbotview.answerButton is None:
                self.chatbotErrorButtonsClear()
    def currentErrorsChange(self):
        self.previousErrorCount = self.activeErrorCount
        self.activeErrorCount = self.errorConsole.tableWidget.rowCount()

    def onSearch(self):
        if not self.textPad:
            return
        dialog = FindReplaceDialog(self, self.textPad)
        dialog.exec_()

    def refresh(self, textPad=None):
        if not textPad:
            return

        self.textPad = textPad

        if not self.textPad.filename:
            self.setWindowTitle('PyNar Kod Editörü')
            return

        dir = os.path.dirname(self.textPad.filename)

        try:
            os.chdir(dir)
            self.setWindowTitle(self.textPad.filename)

        except Exception as e:
            self.statusBar.showMessage(str(e), 3000)

        # self.fileBrowser.refresh(dir)
        self.codeView.refresh()

    def centerOnScreen(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)

    def help(self):
        self.helpdialog = HelpDialog(self)
        self.helpdialog.show()

    def log_messenger(self, some_info):
        logfunc(some_info, parent=self)

    # Errorgridden bilgileri al ve ana loglama fonksiyonuna gönder
    def errorgridlog(self, hata_listesi_0):
        import copy
        # Hata indisini belirlemek için sayı tanımla
        i = 0
        # Hata listesini oluştur
        hata_listesi = {}
        # hata_listesi_0 içindeki gerekli bilgileri hata_listesine at
        for hata in hata_listesi_0["diagnostics"]:
            i = i + 1
            hata_indisi = "hata_" + str(i)
            # hata_listesi_0 içerisindeki mesaj kısmındaki " ve ' karakterlerini temizledikten sonra hata_listesine aktar
            mesaj = hata['message'].replace('"', "")
            mesaj = mesaj.replace("'", "")
            hata_satiri = {}
            hata_satiri['mesaj'] = mesaj
            hata_satiri['dosya'] = hata['file']
            if ('satir' in hata):
                hata_satiri['satir'] = hata['satir']
            else:
                hata_satiri['satir'] = hata['range']['start']['line']
            hata_listesi[hata_indisi] = hata_satiri
        logfunc("Hata", "", hata_listesi, parent=self)

    def chatbotAddErrorMessage(self, errorMessages):
        self.chatbotview.textEdit_message.append("\n")
        isVisible = self.chatbotview.RunErrorMessage(errorMessages, self.textPad.text().split("\n"))
        if isVisible:
            self.label_robot.setVisible(False)
        self.chatbotview.textEdit_message.append("\n")

    def chatbotErrorButtonsClear(self):
        self.chatbotview.ErrorButtonsClear()

    def control(self):
        if self.token is None:
            mess = "Sınavlarınızı görebilmek için <b>giriş</b> yapmanız gerekmektedir. Giriş yapmak istermisiniz?"
            CustomizeMessageBox_Yes_No(mess, clickAccept=self.UserLoginClick)

    def exams(self):
        self.setExamImage()
        self.control()
        if self.exCount > 0:
            self.examWindow = QDialog()
            self.examWindow.setWindowFlags(Qt.FramelessWindowHint | Qt.Popup)
            self.examWindow.setMinimumSize(QSize(315, 260))
            self.examWindow.setMaximumSize(QSize(315, 260))

            self.examLayout = QtWidgets.QHBoxLayout()
            self.scrollArea = QtWidgets.QScrollArea()

            self.scrollArea.setWidgetResizable(True)
            self.scrollAreaWidgetContents = QtWidgets.QWidget()
            self.gridLayoutExam = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
            self.scrollArea.setWidget(self.scrollAreaWidgetContents)
            self.examLayout.addWidget(self.scrollArea)

            self.font_exam_menu = QFont()
            self.font_exam_menu.setFamily(self.c.getEditorFont())
            self.font_exam_menu.setPointSize(self.c.getHistoryMenuFontSize() + 6)
            self.font_exam_menu.setWeight(75)

            self.lbl_title_exam = QtWidgets.QLabel()
            self.lbl_title_exam.setObjectName("lblTitleRecent")
            self.lbl_title_exam.setText("Sınavlarınız")
            self.lbl_title_exam.setStyleSheet('color:#0070ba;')
            self.lbl_title_exam.setFont(self.font_exam_menu)
            self.lbl_title_exam.setContentsMargins(0, 0, 0, 0)
            self.gridLayoutExam.addWidget(self.lbl_title_exam, 0, 0)

            self.lw_exams = QtWidgets.QListWidget()
            self.lw_exams.setMinimumWidth(200)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.lw_exams.sizePolicy().hasHeightForWidth())
            self.lw_exams.setSizePolicy(sizePolicy)
            self.lw_exams.setFrameShape(QtWidgets.QFrame.NoFrame)
            self.lw_exams.itemClicked.connect(self.onClickExamItem)
            self.lw_exams.setStyleSheet(
                "QListWidget{ background-color: #f0f0f0;}QListWidget::item{}QListWidget::item:hover{background-color:#d0d7da;}; ")
            self.lw_exams.setSelectionMode(QAbstractItemView.NoSelection)
            self.gridLayoutExam.addWidget(self.lw_exams, 0, 0)
            self.lw_exams.horizontalScrollBar().setVisible(False)
            self.loadExams()

            if self.lw_exams.count() == 0:
                pass
            else:
                rightVLayout = QtWidgets.QVBoxLayout(self.examWindow)
                rightVLayout.addWidget(self.lbl_title_exam)
                rightVLayout.addWidget(self.lw_exams)
                rightVLayout.setStretch(1, 2)
                rightVLayout.setSpacing(10)
                self.examWindow.move(self.geometry().x() + self.geometry().width() - 385, self.geometry().y() + 107)
                self.examWindow.exec()

    def loadExams(self):
        self.rm.removeAllItemNotExist()
        try:
            self.lw_exams.clear()

            for k in self.examList:
                if k['started_at'] is None:
                    contDateStart = datetime(*tuple([int(x) for x in k['start_date'][:10].split('-')]) + tuple(
                        [int(x) for x in k['start_date'][11:].split(':')]))
                    contDateStop = datetime(*tuple([int(x) for x in k['due_date'][:10].split('-')]) + tuple(
                        [int(x) for x in k['due_date'][11:].split(':')]))
                    if contDateStart < datetime.now() and contDateStop > datetime.now():
                        p = k['exam_name']
                        examItem = UcSpExamItem(self)
                        examItem.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

                        if len(p) > 28:
                            p = p[:25] + "..."
                        if len(p) > 75:
                            p = p[:75] + "..."
                        dateStart = datetime.fromisoformat(k['start_date']).strftime("%d-%m-%Y, %H:%M:%S")
                        dateStop = datetime.fromisoformat(k['due_date']).strftime("%d-%m-%Y, %H:%M:%S")
                        examItem.setValue(p, 'Sınav Süresi     :'+str(k['exam_time'])+' dk\nBaşlangıç Tarihi:'+dateStart+'\nBitiş Tarih         :'+ dateStop, p)
                        item = QListWidgetItem(self.lw_exams)
                        item.setData(QtCore.Qt.UserRole, p)
                        item.setSizeHint(examItem.sizeHint())
                        self.lw_exams.addItem(item)
                        self.lw_exams.setItemWidget(item, examItem)
        except Exception as err:
            print("error: {0}".format(err))

        self.lw_exams.setCurrentIndex(QModelIndex())

    def onClickExamItem(self, item):
        if self.c.getExamLogEnabled() == "True":
            lesson = item.data(QtCore.Qt.UserRole)
            questionInfo = next(item for item in self.examList if item["exam_name"] == lesson)
            if self.openExam is None:
                self.openExam = lesson
                self.ExamWindow = ExamWindow(self, self.token, questionInfo)
                self.ExamWindow.show()
            else:
                self.examWindow.setVisible(False)
                self.ExamWindow.activateWindow()
                if self.ExamWindow.lesson != lesson:
                    mess = 'Açık bir sınav ekranı varken farklı bir sınav açamazsınız. Sınavınızı değişmek için mevcut olanı kapatıp yeniden seçim yapabilirsiniz'
                    CustomizeMessageBox_Ok(mess, "critical")
        else:
            mess = "Sınava Başlayabilmek için Ayarlar penceresi altındaki \'Sınav verilerini kaydet\' alanını seçmelisiniz'"
            CustomizeMessageBox_Ok(mess, "critical")

    def fetchExams(self):
        serverAdd = self.c.getServerAddress()
        if self.token != None:
            headers = {'Authorization': 'Bearer ' + self.token}
            exams = requests.post(serverAdd + "/api/v1/user/student/exams", headers=headers)
            res_json = exams.json()
            self.examList = res_json['result']['data']

    def closeEvent(self, event):
        for i in range(self.notebook.count()):
            self.notebook.closeTab(0)#Her seferinde bir tab kapandığından sürekli 0. tab alınmalı
            if self.notebook.cancelButton:
                event.ignore()
                self.notebook.cancelButton = False
                break
            if self.notebook.count() == 0:
                break

    def showReleaseInfo(self):
        try:
            from PyQt5.QtCore import QT_VERSION_STR
            from PyQt5.Qt import PYQT_VERSION_STR

            CustomizeMessageBox_Ok("Pynar Editör Sürüm: " + self.c.getReleaseInfo() +
                                   "\nPython version: " + str(platform.python_version()) +
                                   "\nQt version: " + str(QT_VERSION_STR) +
                                   "\nPyQt version: " + str(PYQT_VERSION_STR), "information")
        except Exception as err:
            print("error show releaseInfo: {0}".format(err))
# if __name__ == '__main__':
# app = QApplication(sys.argv)
# # apply_stylesheet(app, theme='white_pynar_theme.xml', light_secondary=True)
# main = MainWindow()
# sys.exit(app.exec_())
