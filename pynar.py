import sys
import os
import platform
import uuid
import subprocess

from PyQt5 import QtWidgets, QtCore
from PyQt5.uic.properties import QtGui

from Components.StartPage.emptyrecent import UcEmptyRecent
from Components.TopMenu.uc_sp_recentitem import UcSpRecentItem
from widgets import MessageBox

plt = platform.system()
from PyQt5.QtCore import QSize, QModelIndex
from Components.LoginProcesses.login import UserLabel
import icons_rc
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout, QToolBar, QAction, QSplitter, QFileDialog,
                             QStatusBar, QDialog, QSizePolicy, QPushButton, QLineEdit, QDesktopWidget, QShortcut,
                             QVBoxLayout,
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

activePage = None

#########MSTF
# Log icin su anki zaman gerekli
from datetime import datetime
import json
from PyQt5.QtGui import QKeySequence
import tempfile

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
    def __init__(self, parent=None, logAndInd=None):
        super().__init__(parent)
        self.logAndInd = logAndInd

    def paste(self):
        super().paste()
        logfunc("Yapıştır: " + QApplication.clipboard().text())

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
        # Tus kombinasyonlarinda modifier tusu logda gozukmesin
        if (key_pressed == "Ctrl+V"):
            logfunc("Yapıştır: " + QApplication.clipboard().text())
            return
        if (
                event.key() != Qt.Key_Shift and event.key() != Qt.Key_Alt and event.key() != Qt.Key_Control and event.key() != Qt.Key_Meta):
            logfunc("Basılan Tuş: " + key_pressed)

    # Sürükleme log
    def dropEvent(self, event):
        super().dropEvent(event)
        message = "Sürükle: " + event.mimeData().text()
        logfunc(message)
        
    def messenger(self, string):
        logfunc(string)


# Solmenü override
class UcLMMenus(UcLMMenus):
    def __init__(self, parent=None):
        super().__init__(parent)

    def MenuActionClick(self, jsonFile, index):
        super().MenuActionClick(jsonFile, index)
        message = self.toolButtons[index].text()
        message = "Solmenü_Tıkla: " + message.replace("\n", "")
        logfunc(message)


# QAction Overwrite
class QAction(QAction):
    def __init__(self, a=None, b=None, parent=None):
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
        logfunc(message)

# Loga yazma fonksiyonu
def logfunc(input_message, filestr="", error_grid_info=""):
    if (main_pointer.notebook.textPad == None):
        return
    c = Configuration()
    if (c.getLogEnabled() != "True"):
        return
    text_size = len(main_pointer.notebook.textPad.text())
    line_count = main_pointer.notebook.textPad.lines()
    time = datetime.now()
    timestamp = time.strftime('%Y_%m_%d %H-%M-%S.%f')[:-3]
    message = {'MachineId': str(generate_system_id()), 'time': timestamp, 'action': input_message,
               'totalchars': text_size, 'totallines': line_count}
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


#######################

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
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

        # MSTF: LOG baslat, mainwindow pointeri ata
        self.log = initialize_log()
        global main_pointer
        main_pointer = self
        #
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

    def UserLoginClick(self):
        if self.loginWindow is None:
            self.loginWindow = LoginWindow(self,self.lbl_img_user)

        self.loginWindow.move(self.x() + (
                    self.lbl_img_user.width() * (self.width() / self.lbl_img_user.width())) - self.loginWindow.width(),
                              self.y() + self.lbl_img_user.height() * 2)
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

        self.lbl_img_user = UserLabel(self.header)
        self.lbl_img_user.setMaximumSize(QtCore.QSize(55, 55))
        self.lbl_img_user.setMinimumSize(QtCore.QSize(55, 55))
        self.lbl_img_user.setPixmap(QPixmap(':/icon/images/user.png'))
        self.lbl_img_user.setScaledContents(True)
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

        MainWindow.resize(1600, 900)
        MainWindow.setMinimumSize(QtCore.QSize(1200, 700))

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
        self.menus = UcLMMenus(self.notebook)
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
        pixmap2 = pixmap.scaled(pixmap.width() / 3, pixmap.height() / 3)
        self.label_robot.setPixmap(pixmap2)
        self.label_robot.setAlignment(Qt.AlignTop)
        self.label_robot.setVisible(True)


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
        self.logAndInd = writeLog(os.path.dirname(os.path.realpath(__file__)), self.errorConsole, self.splitterV)
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

        self.errorToDb = error_outputs_to_db()


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
        editor = CodeEditor(parent=self, logAndInd=self.logAndInd)
        editor.filename = None

        self.notebook.newTab(editor)

        x = self.notebook.count()
        index = x - 1

        self.notebook.setCurrentIndex(index)
        self.textPad = editor
        self.notebook.textPad = editor
        self.mainWindow = self.textPad.mainWindow
        self.changeToolbarButtonActive(True)

    def open(self, starter=None, getPath=None):
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

    def openFile(self, filePath):
        filePath = filePath
        try:
            with open(filePath, 'r', encoding='utf-8') as f:
                text = f.read()

            editor = CodeEditor(self, logAndInd=self.logAndInd)
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

            # MSTF: Log open action
            logfunc("Eylem: Aç", str(filePath))
            #

        except Exception as e:
            self.statusBar.showMessage(str(e), 3000)

        self.changeToolbarButtonActive(True)
        return True

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

                editor = CodeEditor(self, logAndInd=self.logAndInd)
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

    def redo(self):
        self.textPad.redo()

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
        path = str(p['filepath'])
        if os.path.exists(path):
            self.openFile(path)
            self.historyWindow.close()
        else:
            q = MessageBox(QMessageBox.Warning, 'Uyarı',
                           'Dosya bulunamadı\n\nSon kullanılan dosyalar listesinden çıkarmak ister misiniz ?',
                           QMessageBox.Yes | QMessageBox.No)

            if (q.exec_() == QMessageBox.Yes):
                if self.rm.removeItem(path):
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
            dialog = PMDialog(self, self.textPad)
            dialog.exec_()
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

            dialog = HelpDialog(self, view)
            dialog.exec_()

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
        command = c.getInterpreter(system)

        thread = RunThread(command)
        thread.start()

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
        command = c.getRun(system).format(self.textPad.filename)

        if not self.textPad.filename:
            self.statusBar.showMessage("Dosya adı olmadan çalıştırılamaz!", 3000)
            return
        self.logAndInd.clearIndıcator(self.textPad)
        logfunc("Eylem: Çalıştır", self.textPad.filename)

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
            self.styntaxError=False

        if self.activeErrorCount == 0 and self.previousErrorCount > 0:
            self.chatbotview.ErrorButtonsClear(chatClear=True)

    def command(self, command, directory):
        if os.path.isfile(directory):
            os.remove(directory)
        os.system(command)

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
        if self.errorConsole.message is not None and self.activeErrorCount > 0:
            self.chatbotAddErrorMessage(self.errorConsole.message)
            self.timer.stop()
        else:
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
        helpdialog = HelpDialog(self)
        helpdialog.exec_()

    def log_messenger(self, some_info):
        logfunc(some_info)

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
        logfunc("Hata", "", hata_listesi)

    def chatbotAddErrorMessage(self, errorMessages):
        isVisible = self.chatbotview.RunErrorMessage(errorMessages)
        if isVisible:
            self.label_robot.setVisible(False)

    def chatbotErrorButtonsClear(self):
        self.chatbotview.ErrorButtonsClear()

# if __name__ == '__main__':
# app = QApplication(sys.argv)
# # apply_stylesheet(app, theme='white_pynar_theme.xml', light_secondary=True)
# main = MainWindow()
# sys.exit(app.exec_())
