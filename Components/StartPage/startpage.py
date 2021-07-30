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
from configuration import Configuration
from PyQt5.QtWidgets import *
from Components.StartPage.uc_sp_recentitem import UcSpRecentItem
from Components.StartPage.uc_sp_menuitem import UcSpMenuItem
from widgets import MessageBox
from Components.StartPage.recentmanager import RecentManager
from Components.StartPage.startmenumager import StartMenuManager, StartMenuModel
from Components.StartPage.emptyrecent import UcEmptyRecent
from pynar import MainWindow

import webbrowser


class StartPage(QDialog):
    def __init__(self, parent=None):
        super().__init__()

        self.c = Configuration()
        self.font_editor = QFont()
        self.font_editor.setFamily(self.c.getEditorFont())
        self.font_editor.setPointSize(self.c.getEditorFontSize()+6)
        self.font_editor.setWeight(75)

        self.mainWindow = parent
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
                q = MessageBox(QMessageBox.Warning, 'Uyarı', 'Dosya bulunamadı', QMessageBox.Ok)
                q.exec_() == QMessageBox.Yes

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
        path = str(p['filepath'])
        if os.path.exists(path):
            self.mainWindow.open(starter=1, getPath=path)
            self.mainWindow.show()
            self.hide()
        else:
            q = MessageBox(QMessageBox.Warning, 'Uyarı',
                           'Dosya bulunamadı\n\nSon kullanılan dosyalar listesinden çıkarmak ister misiniz ?',
                           QMessageBox.Yes | QMessageBox.No)

            if (q.exec_() == QMessageBox.Yes):
                if self.rm.removeItem(path):
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

