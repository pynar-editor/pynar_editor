import json
import sys
import platform
from os import listdir
from pathlib import Path
from PyQt5.QtCore import QMimeData
from PyQt5 import QtWidgets, Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QFont, QColor
from Components.LeftMenu.Menus.TreeHelpDialog import *
from PyQt5.QtWidgets import QAbstractItemView, QLayout, QHeaderView
from configuration import Configuration

childNodes = []

class StandardItem(QStandardItem):
    def __init__(self, image_path=''):
        super().__init__()
        if image_path:
            image = QIcon(image_path)
            self.setData(image, Qt.DecorationRole)

class SceneTreeModel(QStandardItemModel):

    def mimeData(self, indexes):
        name = indexes[0].data()
        mimedata = QMimeData()
        if name in childNodes:
            mimedata.setText(name)
        return mimedata

    def supportedDropActions(self):
        return QtCore.Qt.CopyAction

    def canDropMimeData(self, data, action, row, column, parent):
        return True



class MenuButton(QtWidgets.QPushButton):
    moveSignal = QtCore.pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(MenuButton, self).__init__(*args, **kwargs)
        self.setFixedHeight(50)


class UcLMMenus(QWidget):
    jsonFiles = []
    leftToolMenuWidth = 115
    # descriptions = []
    isTreeOpen = True
    def __init__(self, parent=None):
        super().__init__(parent)

        self.c = Configuration()
        self.font = QFont()
        self.font.setFamily(self.c.getEditorFont())
        self.font.setPointSize(self.c.getEditorFontSize())
        self.parent = parent
        self.setupUi(self)
        self.upButton.setVisible(False)

    # Slide Menu hide -show method
    def hideTreeView(self, control=False):
        if not self.treeView.isVisible() or control:
            self.treeView.hide()
            self.treeView.setVisible(True)
            self.solmenu.setFixedWidth(427)
            return False
        else:
            self.treeView.show()
            self.treeView.setVisible(False)
            self.solmenu.setFixedWidth(115)
            return True

    def solGenislik(self, solmenu=None):
        if solmenu is not None:
            self.solmenu = solmenu


    def expanded(self, index):

        if index.column():
            dosyaAdi = self.treeView.model().item(index.row(), 0).text()
            if dosyaAdi in self.descriptions.values():
                self.helpDialog = TreeHelpDialog(dosyaAdi)
                self.helpDialog.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
                self.helpDialog.setMinimumSize(QtCore.QSize(1200, 800))
                self.helpDialog.setMaximumSize(QtCore.QSize(16777215, 16777215))
                self.helpDialog.show()

    def ReadFromFile(self, dosya):
        dosyaPath = self.c.getHomeDir() + self.c.getTreeMenuPath("tree_menu_path") + dosya
        with open(dosyaPath, encoding='utf-8') as f:
            data = json.load(f)
        model = SceneTreeModel()
        model.setColumnCount(2)
        model.setHeaderData(1, Qt.Horizontal, "")
        self.TreeViewFill(model, data)
        self.treeView.setModel(model)
        self.treeView.setAutoScroll(False)
        self.treeView.setColumnWidth(0, 260)

    def TreeViewFill(self, model, data):
        for root, children in data.items():
            self.treeViewRootData.append(root[root.find(" ") + 1:])
            parent = QStandardItem(root)
            self.treeViewParent = parent
            self.AddChild(children, parent)
            parent.setText(root[root.find(" ") + 1:])
            parent.setToolTip(root[root.find(" ") + 1:])

            if Path(self.c.getHomeDir() + self.c.getHtmlHelpPath("html_help_path") +root.split('#')[0]).exists():

                model.appendRow([parent, StandardItem(':/icon/images/treeview-help.png')])
            else:
                model.appendRow([parent])


    def AddChild(self, children, parent):
        if isinstance(children, dict):
            for item, items in children.items():
                child = QStandardItem(item)
                child.setToolTip(item)
                parent.appendRow(child)
                self.treeViewWayBuffer.append(child)
                self.AddChild(items, child)

        elif children != None:  # if there is one node
            node = QStandardItem(children)
            node.setFont(self.font)
            node.setToolTip("Bu kodu editöre sürükle-bırak şeklinde taşıyabilirsiniz")
            self.treeViewChildData.append(children)
            childNodes.append(children)
            parent.appendRow(node)
            self.treeViewWayBuffer = [self.treeViewParent] + self.treeViewWayBuffer
            self.treeViewWay.append(self.treeViewWayBuffer)
            self.treeViewWayBuffer = []

    # endregion

    @QtCore.pyqtSlot()
    def moveUp(self):
        ix = self.listWidget.moveCursor(QtWidgets.QAbstractItemView.MoveUp, QtCore.Qt.NoModifier)
        self.listWidget.setCurrentIndex(ix)
        if 1 < self.activeMenu:
            self.toolButtons[self.activeMenu].setStyleSheet(
                "background-color: #394b58; color: white; font: 10pt; padding-top:10px;")
            self.previousActiveMenu = self.activeMenu
            self.activeMenu = self.activeMenu - 1
            self.toolButtons[self.activeMenu].setStyleSheet(
                "background-color: #6b899f; color: white; font: 10pt; padding-top:10px;")
            self.MenuActionClick(self.jsonFiles[self.activeMenu - 1][0], self.activeMenu, self.jsonFiles[self.activeMenu - 1][1])
            self.hideTreeView(True)
            self.downButton.setVisible(True)
        if self.activeMenu <= 1:
            self.upButton.setVisible(False)

    @QtCore.pyqtSlot()
    def moveDown(self):
        if self.menuItemCount > self.activeMenu:
            self.toolButtons[self.activeMenu].setStyleSheet(
                "background-color: #394b58; color: white; font: 10pt; padding-top:10px;")
            self.previousActiveMenu = self.activeMenu
            self.activeMenu = self.activeMenu + 1
            self.toolButtons[self.activeMenu].setStyleSheet(
                "background-color: #6b899f; color: white; font: 10pt; padding-top:10px;")
            self.listWidget.setCurrentRow(self.activeMenu - 1)
            self.MenuActionClick(self.jsonFiles[self.activeMenu - 1][0], self.activeMenu,self.jsonFiles[self.activeMenu - 1][1])
            self.hideTreeView(True)
            self.upButton.setVisible(True)
        if self.menuItemCount <= self.activeMenu:
            self.downButton.setVisible(False)

    def FillMenuCategories(self):
        dosya = 'menus.json'
        dosyaPath = self.c.getHomeDir() + self.c.getTreeMenuPath("tree_menu_path") + dosya

        with open(dosyaPath, encoding='utf-8') as f:
            leftMenuJson = json.load(f)
        i = 1
        self.menuItemCount = len(leftMenuJson.items())
        for root, children in leftMenuJson.items():
            item = QtWidgets.QListWidgetItem()
            widget = QWidget()
            jsonfile = children['jsonfile']
            forceNewPage = True if 'forceNewPage' in children else False
            arr = [children['jsonfile'], forceNewPage]
            self.jsonFiles.append(arr)
            self.toolButtons[i] = toolButton = QtWidgets.QToolButton()
            toolButton.setStyleSheet(
                "QToolButton {background-color: #394b58; color: white; font: "+str(self.c.getEditorFontSize())+"pt; padding-top:10px;}\n"
                "QToolButton:hover {background-color: #6b899f; color: white; font: "+str(self.c.getEditorFontSize())+"pt; padding-top:10px;}\n")
            toolButton.setFixedWidth(115)
            toolButton.setFixedHeight(115)
            self.toolButtons[1].setStyleSheet("background-color: #6b899f; color: white; font: "+str(self.c.getEditorFontSize())+"pt; padding-top:10px;")
            self.previousActiveMenu = 1
            self.activeMenu = 1
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(children['icon']), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            toolButton.setIconSize(QtCore.QSize(self.c.getEditorFontSize()*4, self.c.getEditorFontSize()*4))
            toolButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
            toolButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            toolButton.setIcon(icon)
            toolButton.setText(root)
            toolButton.setFont(self.font)
            self.toolButtons[i].clicked.connect(
                lambda checked, index=i, jsonfile=jsonfile, forceNewPage=forceNewPage: self.MenuActionClick(jsonfile, index, forceNewPage))
            toolButton.setObjectName("toolButton")
            toolButton.raise_()
            widgetLayout = QHBoxLayout()
            widgetLayout.addWidget(toolButton)
            widgetLayout.addStretch()
            widgetLayout.setSizeConstraint(QLayout.SetFixedSize)
            widgetLayout.setContentsMargins(0, 0, 0, 0)
            widget.setLayout(widgetLayout)
            item.setSizeHint(widget.sizeHint())
            self.listWidget.addItem(item)
            self.listWidget.setItemWidget(item, widget)
            i = i + 1

    def MenuActionClick(self, jsonFile, index, forceNewPage):
        self.forceNewPage = forceNewPage
        if self.activeMenu != 0:
            self.toolButtons[self.activeMenu].setStyleSheet(
                "background-color: #394b58; color: white; font: "+str(self.c.getEditorFontSize())+"pt; padding-top:10px;")
        self.toolButtons[index].setStyleSheet("background-color: #6b899f; color: white; font: "+str(self.c.getEditorFontSize())+"pt; padding-top:10px;")
        self.treeViewWay = []
        self.ReadFromFile(jsonFile)
        self.previousActiveMenu = self.activeMenu
        self.activeMenu = index

        if self.activeMenu == self.previousActiveMenu:
            self.hideTreeView()
        else:
            self.hideTreeView(True)


    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))

    def setupUi(self, Form):
        self.treeView = QtWidgets.QTreeView(self.parent)
        font = QFont()
        font.setFamily(self.c.getEditorFont())
        font.setPointSize(self.c.getEditorFontSize())
        self.treeView.setFont(font)
        # slide  show - hide
        self.treeView.hide()
        self.treeView.setVisible(False)

        self.downButton = MenuButton(icon=QIcon(':/icon/images/down.png'))
        self.upButton = MenuButton(icon=QIcon(':/icon/images/up.png'))
        self.toolButtons = {}

        Form.setObjectName("Form")
        self.frame_solmenu = QtWidgets.QFrame(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.frame_solmenu.setSizePolicy(sizePolicy)
        self.frame_solmenu.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_solmenu.setObjectName("frame_solmenu")



        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.addWidget(self.frame_solmenu, 0, 0, 1, 1)
        self.gridLayout.setSpacing(0)

        self.leftMenuLayout = QtWidgets.QVBoxLayout(self.frame_solmenu)
        self.leftMenuLayout.setObjectName("leftMenuLayout")
        self.leftMenuLayout.setContentsMargins(0, 0, 0, 0)

        self.upButton.setIconSize(QSize(50, 50))
        self.upButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.upButton.moveSignal.connect(self.moveUp)
        self.upButton.setFixedWidth(self.leftToolMenuWidth)
        self.upButton.setFixedHeight(32)
        self.upButton.setStyleSheet("QPushButton {background-color: #394b58; border:none}"
                                    "QPushButton:hover {background-color: #6b899f; border:none}")
        self.downButton.setIconSize(QSize(50, 50))
        self.downButton.setFixedWidth(self.leftToolMenuWidth)
        self.downButton.setFixedHeight(32)
        self.downButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.downButton.moveSignal.connect(self.moveDown)
        self.downButton.setStyleSheet("QPushButton {background-color: #394b58; border:none;}"
                                      "QPushButton:hover {background-color: #6b899f; border:none} ")

        self.listWidget = QtWidgets.QListWidget(self.frame_solmenu)
        self.listWidget.setStyleSheet("background-color: #394b58; border:none; ")
        self.listWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.listWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.listWidget.setFixedWidth(self.leftToolMenuWidth)

        self.FillMenuCategories()

        self.listWidget.setCurrentRow(self.activeMenu)

        self.leftMenuLayout.addWidget(self.upButton)
        self.leftMenuLayout.addWidget(self.listWidget)
        self.leftMenuLayout.addWidget(self.downButton)
        self.leftMenuLayout.setSpacing(0)

        self.downButton.clicked.connect(self.moveDown)
        self.upButton.clicked.connect(self.moveUp)

        self.treeView.setObjectName("treeView")
        self.treeView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.treeView.setMinimumSize(QtCore.QSize(310, 410))
        self.treeView.setMaximumSize(QtCore.QSize(310, 16777215))
        self.gridLayout.addWidget(self.treeView, 0, 1, 1, 1)
        self.treeView.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.treeView.setIndentation(32)
        self.treeView.setStyleSheet("QTreeView {\n"
                                    "    background-color: #6b899f;\n"
                                    "    padding: 8px;\n"
                                    "    outline: 0px;\n"
                                    "    selection-background-color: transparent;\n"
                                    "    font: "+str(self.c.getEditorFontSize())+"pt;\n"
                                    "}\n"
                                    "\n"
                                    "QTreeView::item {\n"
                                    "         padding-left: 10px;                      \n"
                                    "         margin-bottom:8px;       \n"
                                    "         background-color:  rgb(0, 172, 234);\n"
                                    "         color: white;      \n"
                                    "         selection-background-color: transparent;\n"
                                    "    }\n"
                                    "\n"
                                    "QTreeView::branch:has-siblings:!adjoins-item {\n"
                                    "    border-image: url(:/icon/images/vline.png) 0;\n"
                                    "    background-color: transparent;\n"
                                    "}\n"
                                    "\n"
                                    "QTreeView::branch:has-siblings:adjoins-item {\n"
                                    "    border-image: url(:/icon/images/branch-more.png) 0;\n"
                                    "    background-color: transparent;\n"
                                    "}\n"
                                    "\n"
                                    "QTreeView::branch:!has-children:!has-siblings:adjoins-item {\n"
                                    "    border-image: url(:/icon/images/branch-end.png) 0;\n"
                                    "    background-color: transparent;\n"
                                    "}\n"
                                    "\n"
                                    "QTreeView::branch:has-children:!has-siblings:closed,\n"
                                    "QTreeView::branch:closed:has-children:has-siblings {\n"
                                    "        border-image: none;\n"
                                    "        image: url(:/icon/images/branch-closed.png);\n"
                                    "        background-color: transparent;\n"
                                    "        padding-right:8px;\n"
                                    "        padding-bottom:10px;\n"
                                    "}\n"
                                    "\n"
                                    "QTreeView::branch:open:has-children:!has-siblings,\n"
                                    "QTreeView::branch:open:has-children:has-siblings  {\n"
                                    "        border-image: none;\n"
                                    "        image: url(:/icon/images/branch-open.png);\n"
                                    "        background-color: transparent;\n"
                                    "        padding-right:8px;\n"
                                    "        padding-bottom:10px;\n"
                                    "}\n"
                                    "\n"
                                    "QTreeView::item:!has-children{\n"
                                    "\n"
                                    "      border-radius: 0px 0px 0px 0px;\n"
                                    "      border: 3px solid #fff933;\n"
                                    "      padding-left: 20px;                      \n"
                                    "      margin:10px;                      \n"
                                    "      background-color: #fff933;        \n"
                                    "      color: black;\n"
                                    "\n"
                                    "}\n"
                                    "QTreeView::item:!has-children::hover {\n"
                                    "      border-radius: 0px 0px 0px 0px;\n"
                                    "      border: 3px solid #fff933;\n"
                                    "      padding-left: 20px;                      \n"
                                    "      margin:10px;                      \n"
                                    "      background-color: #ffeaf4; \n"
                                    "      color: black; \n"
                                    "}\n"
                                    "QTreeView::item:open {\n"
                                    "      background-color: #00bcdd; \n"
                                    "}\n"
                                    "\n"
                                    "\n"
                                    "")

        self.treeView.setItemsExpandable(True)
        self.treeView.setDragDropMode(QAbstractItemView.DragOnly)
        self.treeView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.treeView.setHeaderHidden(True)
        self.treeView.clicked.connect(self.expanded)
        self.treeView.expanded.connect(self.expandTreeView)
        self.treeView.collapsed.connect(self.collapseTreeView)
        dosyaPath = self.c.getHomeDir() + self.c.getHtmlHelpPath("html_help_path")
        self.descriptions = {}
        self.expandedData = []
        self.expandedChildData = []
        self.treeViewRootData = []
        self.treeViewChildData = []
        self.treeViewWayBuffer = []
        self.treeViewWay = []
        self.pathDescriptions = [f for f in listdir(dosyaPath) if not os.path.isdir(f)]
        self.show()
        self.FillHelpDialogWords()

    def FillHelpDialogWords(self): #Help Dialog için Treeview öğeleri ile doldurulur.
        for dosya in self.jsonFiles:
            dosyaPath = self.c.getHomeDir() + self.c.getTreeMenuPath("tree_menu_path") + dosya[0]
            with open(dosyaPath, encoding='utf-8') as f:
                data = json.load(f)
            for root, children in data.items():
                self.descriptions[root[:root.find(" ")]] = root[root.find(" ") + 1:]
        TreeViewItemFill(self.descriptions)

    def expandTreeView(self,index):
        if index.data() in self.treeViewRootData:
            for i in self.expandedData:
                self.treeView.collapse(i)
            for i in self.expandedChildData:
                self.treeView.collapse(i)
            self.expandedChildData.clear()
            self.expandedData.append(index)
            self.expandedChildData.append(index)
        else:
            self.expandedChildData.append(index)
            reset = False
            finish = True
            for i in self.treeViewWay:
                collapsed = []
                for k in range(len(self.expandedChildData)):
                    try:
                        if self.expandedChildData[k].data() == i[k].text():
                            pass
                        else:
                            finish = False
                    except:
                        collapsed = []
                        for i in self.treeViewWay:
                            for k in i:
                                if k.text() == self.expandedChildData[-1].data():
                                    reset = True
                                    break
                            if reset:
                                set = 0
                                for j in self.expandedChildData:
                                    if i[set].text() == j.data():
                                        set += 1
                                    else:
                                        self.treeView.collapse(j)
                                        collapsed.append(j)
                                finish = True
                                break
                for j in collapsed:
                    try:
                        self.expandedChildData.remove(j)
                    except:
                        pass
                if finish:
                    break


    def collapseTreeView(self,index):
        if index in self.expandedData:
            self.expandedData.remove(index)
        if index in self.expandedChildData:
            self.expandedChildData.remove(index)

