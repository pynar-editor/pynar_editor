import icons_rc
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtGui import *
from PyQt5.Qt import QModelIndex
from PyQt5.Qt import Qt
from PyQt5.QtCore import QSize
import sys
import os
import json
from Components.MessageBox.CustomizeMessageBox import CustomizeMessageBox_Yes_No,  CustomizeMessageBox_Ok
from configuration import Configuration
from PyQt5.QtWidgets import *
from Components.StartPage.uc_sp_recentitem import UcSpRecentItem
from Components.StartPage.uc_sp_menuitem import UcSpMenuItem
from Components.StartPage.recentmanager import RecentManager
from Components.StartPage.startmenumager import StartMenuManager, StartMenuModel
from Components.StartPage.emptyrecent import UcEmptyRecent
from pynar import MainWindow
import webbrowser
import urllib
import requests
import threading
import subprocess
import importlib.util
from PyQt5 import QtCore, QtWidgets


class StartPage(QDialog):
    def __init__(self, parent=None):
        super().__init__()

        self.c = Configuration()
        self.font_editor = QFont()
        self.font_editor.setFamily(self.c.getEditorFont())
        self.font_editor.setPointSize(self.c.getEditorFontSize()+6)
        self.font_editor.setWeight(75)

        self.mainWindow = parent
        self.checkAppJar()
        self.setupUi(self)
        self.show()
        self.center()


        self.loadRightMenu()

        if (len(sys.argv) > 1):
            path = sys.argv[1]
            if os.path.exists(path):
                self.mainWindow.open(starter=1, getPath=path)
                self.mainWindow.show()
                self.hide()
            else:
                CustomizeMessageBox_Ok('Dosya bulunamadı', "warning")

    def setupUi(self, startpage_container):
        startpage_container.setObjectName("StartPage")
        startpage_container.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        startpage_container.setAttribute(Qt.WA_TranslucentBackground, True)
        startpage_container.setModal(False)

        # Main widget
        self.container_widget = QWidget(startpage_container)
        self.container_widget.setObjectName('CustomWidget')
        self.container_widget.resize(1004, 660) #1120, 720

        # Main frame
        self.pnl_content = QtWidgets.QFrame(self.container_widget)
        self.pnl_content.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.pnl_content.setFrameShadow(QtWidgets.QFrame.Raised)
        self.pnl_content.setObjectName("pnlContent")
        self.pnl_content.setStyleSheet("QFrame{background-color: transparent;}")

        # Sol panel ( Menu Butonları)
        self.pnl_left = QtWidgets.QFrame(self.pnl_content)
        self.pnl_left.setStyleSheet("QFrame{background-color: transparent; border-radius: 10px;}")
        self.pnl_left.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.pnl_left.setFrameShadow(QtWidgets.QFrame.Raised)
        self.pnl_left.setObjectName("pnl_left")
        self.leftPanelUI(self.pnl_left)

        # Sağ Panel (Son Kullanılan Dosyalar)
        self.pnl_right = QtWidgets.QFrame(self.pnl_content)
        self.pnl_right.setStyleSheet("QFrame{background-color: white; border-radius: 10px;}")
        self.pnl_right.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.pnl_right.setFrameShadow(QtWidgets.QFrame.Raised)
        self.pnl_right.setObjectName("pnl_right")
        self.rightPanelUI(self.pnl_right)

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.pnl_content)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.addWidget(self.pnl_left)
        self.horizontalLayout.addWidget(self.pnl_right)


        self.gridLayout = QtWidgets.QGridLayout(self.container_widget)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.addWidget(self.pnl_content, 1, 0, 1, 1)

        self.retranslateUi(self.container_widget)
        QtCore.QMetaObject.connectSlotsByName(self.container_widget)

    def leftPanelUI(self,panel):
        # Pynar logosu ve yazısının frame'i
        headFrame = QtWidgets.QFrame()
        headFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        headFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        headFrame.setMaximumSize(QtCore.QSize(380, 150))
        headFrame.setMinimumSize(QtCore.QSize(380, 150))

        # Pynar Logosu
        head_lbl_image = QtWidgets.QLabel(headFrame)
        head_lbl_image.setObjectName("lblImageMenu")
        head_lbl_image.setPixmap(QtGui.QPixmap(":/icon/images/startLogo.png"))
        head_lbl_image.setScaledContents(True)
        head_lbl_image.setAlignment(Qt.AlignLeft)

        # Pynar logosu ve yazısının layoutu
        headHLayout = QtWidgets.QHBoxLayout(headFrame)
        headHLayout.addWidget(head_lbl_image)
        headHLayout.setContentsMargins(20,0,0,0)
        headHLayout.setStretch(1, 1)


        lwFrame = QtWidgets.QFrame()
        lwFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        lwFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        lwFrame.setContentsMargins(25,0,25,0)

        self.lw_menu = QtWidgets.QListWidget(lwFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lw_menu.sizePolicy().hasHeightForWidth())
        self.lw_menu.setSizePolicy(sizePolicy)
        self.lw_menu.itemClicked.connect(self.onClickMenuItem)
        self.lw_menu.setObjectName("lwMenu")
        self.lw_menu.setStyleSheet("QListWidget::item:hover {background-color:rgb(133,158,175);}")
        self.lw_menu.setSelectionMode(QAbstractItemView.NoSelection)
        lwLayout = QtWidgets.QHBoxLayout(lwFrame)
        lwLayout.addWidget(self.lw_menu)

        helpItem = StartMenuModel("Yardım", "PyNar Yardım", ":/icon/images/help.png", "help")
        btnHelp = UcSpMenuItem(panel)
        btnHelp.frame.setStyleSheet("QFrame::hover {background-color:rgb(133,158,175); border-radius : 0px;}")
        btnHelp.setValue(helpItem.MenuName, helpItem.MenuDesc, helpItem.MenuIcon)
        btnHelp.setContentsMargins(260,0,0,0)
        btnHelp.frame.mouseReleaseEvent=lambda event:self.onClickHelp()

        leftVLayout = QtWidgets.QVBoxLayout(panel)
        leftVLayout.setAlignment(Qt.AlignCenter)
        leftVLayout.addWidget(headFrame)
        leftVLayout.addWidget(lwFrame)
        leftVLayout.addWidget(btnHelp)
        leftVLayout.setSpacing(5)
        leftVLayout.setContentsMargins(20,35,20,0)

        if self.c.getSystem() == "windows":
            self.closePushButton = QPushButton(text = "r", parent=panel, clicked=self.accept, objectName='closeButtonStartPage')
        else:
            self.closePushButton = QPushButton(text="X", parent=panel, clicked=self.accept, objectName='closeButtonStartPage')
        self.closePushButton.setMaximumSize(30, 30)
        self.closePushButton.setMinimumSize(30, 30)

    def rightPanelUI(self, panel):

        self.lbl_title_recent = QtWidgets.QLabel()
        self.lbl_title_recent.setObjectName("lblTitleRecent")
        self.lbl_title_recent.setFont(self.font_editor)
        self.lbl_title_recent.setContentsMargins(10,10,10,10)

        self.lw_recent = QtWidgets.QListWidget()
        self.lw_recent.setMinimumWidth(480)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lw_recent.sizePolicy().hasHeightForWidth())
        self.lw_recent.setSizePolicy(sizePolicy)
        self.lw_recent.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lw_recent.setObjectName("lwRecent")
        self.lw_recent.itemClicked.connect(self.onClickRecentItem)
        self.lw_recent.setStyleSheet("QListWidget::item:hover {background-color:rgb(230,238,255);}")
        self.lw_recent.setSelectionMode(QAbstractItemView.NoSelection)

        self.rm = RecentManager()
        self.loadRecents()

        if self.lw_recent.count() == 0:
            self.emptyrecent = UcEmptyRecent(panel)
            rightVLayout = QtWidgets.QVBoxLayout(panel)
            rightVLayout.addWidget(self.emptyrecent)
        else:
            rightVLayout = QtWidgets.QVBoxLayout(panel)
            rightVLayout.addWidget(self.lbl_title_recent)
            rightVLayout.addWidget(self.lw_recent)
            rightVLayout.setStretch(1,2)
            rightVLayout.setSpacing(10)

    def retranslateUi(self, startpage_container):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("StartPage", "PyNar Kod Editörü"))
        self.setWindowIcon(QIcon(':/icon/images/headerLogo1.png'))
        self.lbl_title_recent.setText(_translate("StartPage", "Son Kullanılan Dosyalar"))

    # Recent dosyasındaki listeyi ekranda görüntüler
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
                    recentItem.setValue(p['filename'], p['filepath'], p['opendate'])

                    item = QListWidgetItem(self.lw_recent)
                    item.setData(QtCore.Qt.UserRole, p)
                    item.setSizeHint(recentItem.sizeHint())
                    self.lw_recent.addItem(item)
                    self.lw_recent.setItemWidget(item, recentItem)
        except Exception as err:
            print("error: {0}".format(err))

        self.lw_recent.setCurrentIndex(QModelIndex())

    # Sağ menü listesi ekranda görüntüler
    def loadRightMenu(self):
        sm = StartMenuManager()
        for menuItem in sm.menus:
            btn = UcSpMenuItem(self)
            btn.setValue(menuItem.MenuName, menuItem.MenuDesc, menuItem.MenuIcon)
            item1 = QListWidgetItem(self.lw_menu)
            item1.setData(QtCore.Qt.UserRole, menuItem.MenuCode)
            item1.setSizeHint(btn.sizeHint())
            # item1.setSizeHint(QSize(330, 75))
            self.lw_menu.addItem(item1)
            self.lw_menu.setItemWidget(item1, btn)
        self.lw_menu.setCurrentIndex(QModelIndex())

    #  Recent listesindeki itemlara tıklanma olayı
    def onClickRecentItem(self, item):
        p = item.data(QtCore.Qt.UserRole)
        self.removeItemPath = str(p['filepath'])
        if os.path.exists(self.removeItemPath):
            self.mainWindow.open(starter=1, getPath=self.removeItemPath)
            self.mainWindow.show()
            self.hide()
        else:
            mess = "<b>Dosya bulunamadı </br><b>Son kullanılan dosyalar listesinden çıkarmak ister misiniz ?"
            CustomizeMessageBox_Yes_No(mess, clickAccept=self.removeItemClick)

    def removeItemClick(self):
        if self.rm.removeItem(self.removeItemPath):
            self.loadRecents()

    # sağ menu butonların tıklama olaylarını yönetir.
    def onClickMenuItem(self, item):
        p = item.data(QtCore.Qt.UserRole)
        if p == "example":
            if (self.mainWindow.saveAsExample()):
                self.mainWindow.show()
                self.hide()

        elif p == "new":
            self.mainWindow.new()
            self.mainWindow.show()
            self.hide()

        elif p == "open":
            filePath = self.c.getHomeDir()
            if (self.mainWindow.open(starter=None, getPath=filePath)):
                self.mainWindow.show()
                self.hide()

        elif p == "help":
            self.mainWindow.showHelp()
            # path = self.c.getHomeDir() + self.c.getHtmlHelpPath("html_help_path") + "PyNarKilavuz" + os.sep + "index.html"
            # newTabOnWeb = 1
            # webbrowser.open(path, new=newTabOnWeb)

        elif p == "skip":
            self.mainWindow.show()
            self.hide()

    def onClickHelp(self):
        self.mainWindow.showHelp()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)

    def checkAppJar(self):
        try:
            self.result_install = None
            self.package_name = 'appJar'
            c = Configuration()
            system = c.getSystem()
            python_exe = c.getSelectedPythonExe()
            spec = subprocess.run([python_exe, '-c', "import appJar"], capture_output=True, text=True, encoding='utf-8', shell = self.c.getShell())
            #spec = importlib.util.find_spec(self.package_name)
            self.appjarIns = False
            if spec.stderr:
                mess = "Kullandığınız Python sürümünde appJar paketi bulunmuyor, PyNar Editörde Görsel programlama yapabilmeniz için appJar paketi gereklidir. Bu paketin otomatik olarak kurulmasını ister misiniz? Eğer \"Hayır\" cevabı verirseniz Pynar Editör Açıldıktan sonra Paket yöneticisini kullanarak appJar paketini kurabilirsiniz."
                CustomizeMessageBox_Yes_No(message=mess, clickAccept=self.yesAppjarInstall, icon="warning")

                self.appjarIns = True
        except Exception as err:
            CustomizeMessageBox_Ok("Bir Hata ile karşılaşıldı", "critical")

    def yesAppjarInstall(self):
        msgBox = LoadingMessageBox()
        font = QFont()
        font.setFamily(self.c.getEditorFont())
        font.setPointSize(self.c.getHistoryMenuFontSize() + 6)
        msgBox.setFont(font)
        csstxt = 'QMessageBox{\n  background-color: #e8f2c6;\n  border-left:1px solid #acd33b;\n  border-right:1px solid #acd33b;\n  border-bottom:1px solid #acd33b;\n  border-top: 8px solid #00ccff;\n}\n\nQLabel{background-color:transparent;height: 110px; min-height: 110px; max-height: 110px; width: 155px; min-width: 155px; max-width: 155px;}'
        msgBox.setStyleSheet(csstxt)

        msgBox.setWindowFlags(msgBox.windowFlags() | Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)
        msgBox.setStandardButtons(QtWidgets.QMessageBox.NoButton)
        msgBox.execute(consuming_work)


    def appjarInstall(self):
        text = 'appJar'
        version = "==" + self.version
        process = subprocess.Popen(
            [os.path.basename(sys.executable), '-m', 'pip', 'install', text + version,
             "--disable-pip-version-check"],
            stdout=subprocess.PIPE, shell=self.c.getShell())
        while True:
            # output = process.stdout.readline()
            rc = process.poll()
            if rc == 1:  # Hata
                return False
            elif rc == 0:  # Başarılı
                return True
            elif rc is not None:
                # TODO:Loglama eklenince burayada log eklenmeli
                return False

    def setAppjarVersion(self):
        baseUrl = 'https://pypi.org/pypi/'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0'}
        jsonDataUrl = baseUrl + urllib.parse.quote(self.package_name) + "/json"
        req = requests.get(jsonDataUrl, headers=headers)
        jsonData = req.json()
        self.version = jsonData['info']['version']

    def connectedToInternet(self):
        try:
            if requests.get('https://google.com').ok:
                return True
        except Exception as err:
            return False


def consuming_work():
    pass



class LoadingMessageBox(QtWidgets.QMessageBox):
    started = QtCore.pyqtSignal()
    finished = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.finished.connect(self.accept)
        movie = QMovie(':/icon/images/loading.gif')
        label_gif = QtWidgets.QLabel(self)
        label_gif.setMovie(movie)
        label_gif.setAlignment(Qt.AlignCenter)
        label_gif.setGeometry(QtCore.QRect(18, 0, 205, 20))
        movie.start()
        label_text = QtWidgets.QLineEdit(self)
        label_text.setReadOnly(True)
        label_text.setStyleSheet("border:none; background-color:transparent")
        label_text.setGeometry(QtCore.QRect(0, 105, 203, 25))
        label_text.setAlignment(Qt.AlignCenter)
        label_text.setText("Kurulum yapılıyor")

        label_text2 = QtWidgets.QLineEdit(self)
        label_text2.setReadOnly(True)
        label_text2.setStyleSheet("border:none; background-color:transparent")
        label_text2.setGeometry(QtCore.QRect(0, 130, 203, 25))
        label_text2.setAlignment(Qt.AlignCenter)
        label_text2.setText("Lütfen bekleyiniz...")

    def execute(self, func):
        threading.Thread(target=self._execute, args=(func,), daemon=True).start()
        return self.exec_()

    def _execute(self, func):
        self.started.emit()
        res = self.connectedToInternet()
        if res:
            self.setAppjarVersion()
            self.result_install = self.appjarInstall()
        else:
            path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
            os.system('pip install ' + path + '/Data/packages/appJar-0.94.0.tar.gz')
        self.finished.emit()

    def appjarInstall(self):
        text = 'appJar'
        c = Configuration()
        version = "==" + self.version
        process = subprocess.Popen(
            [os.path.basename(sys.executable), '-m', 'pip', 'install', text + version,
             "--disable-pip-version-check"],
            stdout=subprocess.PIPE, shell=c.getShell())
        while True:
            # output = process.stdout.readline()
            rc = process.poll()
            if rc == 1:  # Hata
                return False
            elif rc == 0:  # Başarılı
                return True
            elif rc is not None:
                # TODO:Loglama eklenince burayada log eklenmeli
                return False

    def setAppjarVersion(self):
        package_name = 'appJar'
        baseUrl = 'https://pypi.org/pypi/'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0'}
        jsonDataUrl = baseUrl + urllib.parse.quote(package_name) + "/json"
        req = requests.get(jsonDataUrl, headers=headers)
        jsonData = req.json()
        self.version = jsonData['info']['version']

    def connectedToInternet(self):
        try:
            if requests.get('https://google.com').ok:
                return True
        except Exception as err:
            return False

