from PyQt5.QtCore import QSize, QRect, QCoreApplication
from PyQt5.QtWidgets import (QWidget, QDialog, QDesktopWidget,
                             QVBoxLayout, QLineEdit,
                             QCheckBox, QTabWidget,
                             QPushButton, QRadioButton,
                             QLabel, QMessageBox)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.Qt import Qt

from Components.MessageBox.CustomizeMessageBox import CustomizeMessageBox_Ok
from configuration import Configuration

class FindReplaceDialog(QDialog):

    def __init__(self, parent,textPad):
        super().__init__()

        self.mainWindow = parent
        self.textPad = textPad
        self.c = Configuration()

        self.mainWindow.setObjectName("findAndReplaceWidget")
        self.setFixedSize(577, 360)
        self.setWindowTitle('Bul ve Değiştir')
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setStyleSheet("background-color: #CAD7E0;")
        self.setWindowIcon(QIcon(':/icon/images/headerLogo1.png'))
        self.initUI()

    def initUI(self):
        self.centralwidget = QWidget()
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QRect(0, 0, 551, 331))


        font = QFont()
        font.setFamily(self.c.getEditorFont())
        font.setPointSize(self.c.getEditorFontSize())

        self.tabWidget.setFont(font)
        self.tabWidget.setFocusPolicy(Qt.TabFocus)
        self.tabWidget.setContextMenuPolicy(Qt.NoContextMenu)

        self.tabWidget.setStyleSheet(" background-color: rgb(255, 255, 255);")
        self.tabWidget.setTabShape(QTabWidget.Rounded)
        self.tabWidget.setIconSize(QSize(20, 20))
        self.tabWidget.setElideMode(Qt.ElideNone)
        self.tabWidget.setUsesScrollButtons(False)
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setMovable(False)
        self.tabWidget.setTabBarAutoHide(False)
        self.tabWidget.setObjectName("tabWidget")

        self.findDialog = QWidget()
        self.findDialog.setObjectName("findDialog")

        self.find_findText = QLineEdit(self.findDialog)
        self.find_findText.setGeometry(QRect(190, 30, 341, 31))
        self.find_findText.setObjectName("find_findText")

        self.find_findButton = QPushButton(self.findDialog)
        self.find_findButton.setGeometry(QRect(10, 250, 141, 41))
        self.find_findButton.setFont(font)
        self.find_findButton.setStyleSheet("QPushButton { color: white;padding: 5px;font-size: 14px;margin: 4px 2px;border-radius: 4px; background-color: rgb(0, 170, 255);} " \
                      "QPushButton::hover{background-color:rgb(4, 124, 184)}")



        self.find_findButton.setObjectName("find_findButton")
        self.find_downButton = QRadioButton(self.findDialog)
        self.find_downButton.setGeometry(QRect(240, 145, 105, 30))
        self.find_downButton.setStyleSheet("color:rgb(82, 95, 99)")

        self.find_downButton.setFont(font)
        self.find_downButton.setObjectName("find_downButton")
        self.find_upButton = QRadioButton(self.findDialog)
        self.find_upButton.setGeometry(QRect(140, 145, 95, 30))

        self.find_upButton.setFont(font)
        self.find_upButton.setObjectName("find_upButton")
        self.find_upButton.setStyleSheet("color:rgb(82, 95, 99)")
        self.find_matchCase = QCheckBox(self.findDialog)
        self.find_matchCase.setGeometry(QRect(140, 195, 246, 30))
        self.find_matchCase.setStyleSheet("color:rgb(82, 95, 99)")

        self.find_matchCase.setFont(font)
        self.find_matchCase.setObjectName("find_matchCase")
        self.find_labelSearch = QLabel(self.findDialog)
        self.find_labelSearch.setGeometry(QRect(20, 30, 161, 31))
        self.find_labelSearch.setStyleSheet("color:rgb(82, 95, 99)")
        self.find_labelSearch.setFont(font)

        self.find_labelSearch.setObjectName("find_labelSearch")
        self.find_labelDirect = QLabel(self.findDialog)
        self.find_labelDirect.setGeometry(QRect(20, 150, 101, 16))
        self.find_labelDirect.setStyleSheet("color:rgb(82, 95, 99)")

        self.find_labelDirect.setFont(font)
        self.find_labelDirect.setObjectName("find_labelDirect")
        self.find_labelDirect.setStyleSheet("color:rgb(82, 95, 99)")
        self.tabWidget.addTab(self.findDialog, "")
        self.replaceDialog = QWidget()
        self.replaceDialog.setObjectName("replaceDialog")
        self.replace_findButton = QPushButton(self.replaceDialog)
        self.replace_findButton.setGeometry(QRect(10, 250, 141, 41))
        self.replace_findButton.setStyleSheet("color:rgb(82, 95, 99)")

        self.replace_findButton.setFont(font)
        self.replace_findButton.setStyleSheet("QPushButton { color: white;padding: 5px;font-size: 14px;margin: 4px 2px;border-radius: 4px; background-color: rgb(146, 212, 161);} " \
                      "QPushButton::hover{background-color:rgb(97, 140, 107)}")
        self.replace_findButton.setObjectName("replace_findButton")
        self.replace_labelDirect = QLabel(self.replaceDialog)
        self.replace_labelDirect.setGeometry(QRect(20, 150, 101, 16))
        self.replace_labelDirect.setStyleSheet("color:rgb(82, 95, 99)")

        self.replace_labelDirect.setFont(font)
        self.replace_labelDirect.setObjectName("replace_labelDirect")
        self.replace_labelSearch = QLabel(self.replaceDialog)
        self.replace_labelSearch.setStyleSheet("color:rgb(82, 95, 99)")
        self.replace_labelSearch.setGeometry(QRect(20, 30, 161, 31))

        self.replace_labelSearch.setFont(font)
        self.replace_labelSearch.setObjectName("replace_labelSearch")
        self.replace_findText = QLineEdit(self.replaceDialog)
        self.replace_findText.setGeometry(QRect(190, 30, 341, 31))
        self.replace_findText.setObjectName("replace_findText")
        self.replace_upButton = QRadioButton(self.replaceDialog)
        self.replace_upButton.setGeometry(QRect(140, 145, 95, 30))
        self.replace_upButton.setStyleSheet("color:rgb(82, 95, 99)")

        self.replace_upButton.setFont(font)
        self.replace_upButton.setObjectName("replace_upButton")
        self.replace_downButton = QRadioButton(self.replaceDialog)
        self.replace_downButton.setGeometry(QRect(240, 145, 105, 30))
        self.replace_downButton.setStyleSheet("color:rgb(82, 95, 99)")

        self.replace_downButton.setFont(font)
        self.replace_downButton.setObjectName("replace_downButton")
        self.replace_matchCase = QCheckBox(self.replaceDialog)
        self.replace_matchCase.setGeometry(QRect(140, 195, 246, 30))
        self.replace_matchCase.setStyleSheet("color:rgb(82, 95, 99)")

        self.replace_matchCase.setFont(font)
        self.replace_matchCase.setObjectName("replace_matchCase")
        self.replace_replaceText = QLineEdit(self.replaceDialog)
        self.replace_replaceText.setGeometry(QRect(190, 90, 341, 31))
        self.replace_replaceText.setObjectName("replace_replaceText")
        self.replace_labelReplace = QLabel(self.replaceDialog)
        self.replace_labelReplace.setStyleSheet("color:rgb(82, 95, 99)")
        self.replace_labelReplace.setGeometry(QRect(20, 90, 161, 31))

        self.replace_labelReplace.setFont(font)
        self.replace_labelReplace.setObjectName("replace_labelReplace")
        self.replaceButton = QPushButton(self.replaceDialog)
        self.replaceButton.setGeometry(QRect(180, 250, 141, 41))

        self.replaceButton.setFont(font)
        self.replaceButton.setStyleSheet("QPushButton { color: white;padding: 5px;font-size: 14px;margin: 4px 2px;border-radius: 4px; background-color: rgb(227, 183, 154);} " \
                      "QPushButton::hover{background-color:rgb(171, 121, 89)}")
        self.replaceButton.setObjectName("replaceButton")
        self.replaceAllButton = QPushButton(self.replaceDialog)
        self.replaceAllButton.setGeometry(QRect(340, 250, 141, 41))
        font = QFont()
        font.setFamily(self.c.getEditorFont())
        font.setPointSize(self.c.getEditorFontSize())
        self.replaceAllButton.setFont(font)
        self.replaceAllButton.setStyleSheet("QPushButton { color: white;padding: 5px;font-size: 14px;margin: 4px 2px;border-radius: 4px; background-color: rgb(197, 210, 250);} " \
                      "QPushButton::hover{background-color:rgb(116, 140, 212)}")
        self.replaceAllButton.setObjectName("replaceAllButton")
        self.tabWidget.addTab(self.replaceDialog, "")
        layout = QVBoxLayout()
        layout.addWidget(self.tabWidget)

        self.tabWidget.setCurrentIndex(0)
        self.find_downButton.setChecked(1)
        self.replace_downButton.setChecked(1)
        self.find_matchCase.setCheckState(1)
        self.find_matchCase.setTristate(0)
        self.replace_matchCase.setCheckState(1)
        self.replace_matchCase.setTristate(0)

        self.tabWidget.currentChanged.connect(self.tabWidgetChanged)


        self.find_downButton.toggled.connect(lambda: self.btnstate(self.find_downButton))
        self.find_upButton.toggled.connect(lambda: self.btnstate(self.find_upButton))
        self.replace_downButton.toggled.connect(lambda: self.btnstate(self.replace_downButton))
        self.replace_upButton.toggled.connect(lambda: self.btnstate(self.replace_upButton))
        self.find_findButton.clicked.connect(self.find_btnClick)
        self.replace_findButton.clicked.connect(self.replace_findbtnClick)
        self.replaceButton.clicked.connect(self.replace_btnClick)
        self.replaceAllButton.clicked.connect(self.replaceAll_btnClick)
        self.replace_findText.textChanged.connect(self.findTextChange)
        self.find_findText.textChanged.connect(self.findTextChange)
        self.textPad.cursorPositionChanged.connect(self.textPadClicked)
        self.find_matchCase.stateChanged.connect(self.replace_matchCase.setCheckState)
        self.replace_matchCase.stateChanged.connect(self.find_matchCase.setCheckState)
        self.find_matchCase.stateChanged.connect(self.findTextChange)
        self.replace_matchCase.stateChanged.connect(self.findTextChange)

        self.retranslateUi(self.centralwidget)

        self.isFind = False
        self.firstSearch = True

        self.line = -1
        self.index = -1

        if self.textPad.hasSelectedText():
            self.find_findText.setText(self.textPad.selectedText())

        self.setLayout(layout)
        self.center()
        self.show()


    def retranslateUi(self, Find_Replace_Dialog):
        _translate = QCoreApplication.translate
        Find_Replace_Dialog.setWindowTitle(_translate("Find_Replace_Dialog", "Bul/Değiştir"))
        self.find_findButton.setText(_translate("Find_Replace_Dialog", "Bul"))
        self.find_downButton.setText(_translate("Find_Replace_Dialog", "Aşağı"))
        self.find_upButton.setText(_translate("Find_Replace_Dialog", "Yukarı"))
        self.find_matchCase.setText(_translate("Find_Replace_Dialog", "Büyük-Küçük Harf Duyarlılığı"))
        self.find_labelSearch.setText(_translate("Find_Replace_Dialog", "Aranacak Kelime"))
        self.find_labelDirect.setText(_translate("Find_Replace_Dialog", "Arama Yönü"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.findDialog), _translate("Find_Replace_Dialog", "Bul"))
        self.replace_findButton.setText(_translate("Find_Replace_Dialog", "Bul"))
        self.replace_labelDirect.setText(_translate("Find_Replace_Dialog", "Arama Yönü"))
        self.replace_labelSearch.setText(_translate("Find_Replace_Dialog", "Aranacak Kelime"))
        self.replace_upButton.setText(_translate("Find_Replace_Dialog", "Yukarı"))
        self.replace_downButton.setText(_translate("Find_Replace_Dialog", "Aşağı"))
        self.replace_matchCase.setText(_translate("Find_Replace_Dialog", "Büyük-Küçük Harf Duyarlılığı"))
        self.replace_labelReplace.setText(_translate("Find_Replace_Dialog", "Yeni Kelime"))
        self.replaceButton.setText(_translate("Find_Replace_Dialog", "Değiştir"))
        self.replaceAllButton.setText(_translate("Find_Replace_Dialog", "Tümünü Değiştir"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.replaceDialog),
                                  _translate("Find_Replace_Dialog", "Değiştir"))

    def keyPressEvent(self,event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            if self.tabWidget.currentIndex() == 0:
                self.find_btnClick()
            elif self.tabWidget.currentIndex() == 1:
                self.replace_findbtnClick()

    def textPadClicked(self):
        self.line, self.index = self.textPad.getSelection()[:2]

    def findTextChange(self):
        forward = self.find_downButton.isChecked()
        if self.line == -1 and self.index == -1:
            self.line, self.index = 0,0
        cs = self.find_matchCase.checkState()
        if self.tabWidget.currentIndex() == 0:
            find_text = self.find_findText.text()
        elif self.tabWidget.currentIndex() == 1:
            find_text = self.replace_findText.text()
        else:
            find_text = ""

        state_ = (
                  find_text,
                  False,
                  cs,
                  False,
                  True,
                  forward,
                  self.line,
                  self.index
                )
        x = self.textPad.findFirst(*state_)
        if not x:
            self.textPad.setSelection(self.line, self.index, self.line, self.index)

        if not x and find_text != "":
            self.find_findText.setStyleSheet("background-color: rgb(255, 203, 201);")
            self.replace_findText.setStyleSheet("background-color: rgb(255, 203, 201);")
            self.find_findButton.setText("Bulunamadı")
            self.replace_findButton.setText("Bulunamadı")
        else:
            self.find_findText.setStyleSheet("background-color: rgb(255, 255, 255);")
            self.replace_findText.setStyleSheet("background-color: rgb(255, 255, 255);")
            self.firstSearch = True
            self.find_findButton.setText("Bul")
            self.replace_findButton.setText("Bul")


    def btnstate(self,btn):
        if (btn == self.replace_downButton or btn == self.find_downButton) and btn.isChecked() == True:
            self.replace_downButton.setChecked(1)
            self.find_downButton.setChecked(1)
            self.replace_upButton.setChecked(0)
            self.find_upButton.setChecked(0)
        elif (btn == self.replace_upButton or btn == self.find_upButton) and btn.isChecked() == True:
            self.replace_downButton.setChecked(0)
            self.find_downButton.setChecked(0)
            self.replace_upButton.setChecked(1)
            self.find_upButton.setChecked(1)

    def tabWidgetChanged(self,index):
        if index == 0:
            self.find_findText.setText(self.replace_findText.text())
        elif index == 1:
            self.replace_findText.setText(self.find_findText.text())

    def find_btnClick(self):
        if self.firstSearch:
            self.firstSearch = False
            self.find_findButton.setText("Sonrakini Bul")
            self.replace_findButton.setText("Sonrakini Bul")

        forward = self.find_upButton.isChecked()
        cs = self.find_matchCase.checkState()
        find_text = self.find_findText.text()

        if forward:
            line, index = self.textPad.getSelection()[:2]
        else:
            line, index = self.textPad.getSelection()[2:]

        state_ = (
                  find_text,
                  False,
                  cs,
                  False,
                  True,
                  not forward,
                  line,
                  index
                )
        self.textPad.findFirst(*state_)

    def replace_findbtnClick(self):
        if self.firstSearch:
            self.firstSearch = False
            self.find_findButton.setText("Sonrakini Bul")
            self.replace_findButton.setText("Sonrakini Bul")

        forward = self.replace_upButton.isChecked()
        cs = self.replace_matchCase.checkState()
        find_text = self.replace_findText.text()
        if forward:
            line, index = self.textPad.getSelection()[:2]
        else:
            line, index = self.textPad.getSelection()[2:]

        state_ = (
                  find_text,
                  False,
                  cs,
                  False,
                  True,
                  not forward,
                  line,
                  index
                )
        self.textPad.findFirst(*state_)

    def replace_btnClick(self):
        forward = self.replace_upButton.isChecked()
        cs = self.find_matchCase.checkState()
        find_text = self.replace_findText.text()
        replace_text = self.replace_replaceText.text()

        self.textPad.replace(replace_text)

        if forward:
            line, index = self.textPad.getSelection()[:2]
        else:
            line, index = self.textPad.getSelection()[2:]

        state_ = (
                    find_text,
                    False,
                    cs,
                    False,
                    True,
                    not forward,
                    line,
                    index
                )

        self.isFind = self.textPad.findFirst(*state_)

        if not self.isFind:
            if forward:
                line, index = self.textPad.getSelection()[:2]
            else:
                line, index = self.textPad.getSelection()[2:]
            self.textPad.setSelection(line,index,line,index)

    def replaceAll_btnClick(self):
        i = 0
        return_begin = False
        line, index = self.textPad.getSelection()[2:]
        cs = self.replace_matchCase.checkState()
        find_text = self.replace_findText.text()
        replace_text = self.replace_replaceText.text()
        stateFirst_ = (
                  find_text,
                  False,
                  cs,
                  False,
                  False,
                  True,
                )
        state_ = (
            find_text,
            False,
            cs,
            False,
            False,
            True,
            0,
            0
        )
        x = self.textPad.findFirst(*stateFirst_)
        if not x:
            x = self.textPad.findFirst(*state_)
        while x:
            if x:
                self.textPad.replace(replace_text)
                i += 1
            x = self.textPad.findFirst(*stateFirst_)
            line_first, index_first, line_end, index_end = self.textPad.getSelection()[:]
            if not x and not return_begin:
                return_begin = True
                x = self.textPad.findFirst(*state_)
            elif x and return_begin:
                #self.textPad.setSelection(line_end, index_end, line_end, index_end)
                self.findTextChange()
                break
            elif return_begin and line_first >= line and index_first >= index:
                #self.textPad.setSelection(line_end, index_end, line_end, index_end)
                self.findTextChange()
                break

        self.messageBoxShow(i,find_text,replace_text)

    def messageBoxShow(self,i,find_text,replace_text):
        if i > 0:
            CustomizeMessageBox_Ok("""{} Adet "{}" İfadesi "{}" ile Değiştirildi.""".format(i, find_text, replace_text), "information")
        else:
            CustomizeMessageBox_Ok("Değiştirilecek kelime bulunamadı.", "critical")

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)

    def onClose(self):
        self.destroy()
