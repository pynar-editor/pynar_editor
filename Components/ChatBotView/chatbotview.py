import sys
import unicodedata

from PyQt5.QtGui import QMovie
from unidecode import unidecode
import sqlite3

import ast
from PyQt5 import QtWidgets, Qt
from PyQt5.QtWidgets import *
from datetime import datetime
from Components.ChatBotView.chatbot_engine import ChatbotEngine
import logging
from Components.ChatBotView.Messages import LoadMessage
from Components.ChatBotView.replace_emoji import replaceToEmoji
from soundlib import playsound
from threading import Thread
from Components.LeftMenu.Menus.TreeHelpDialog import *
from Components.CheckError.checkError import checkError
import time
import copy

logfilename = os.path.join(sys.path[0], 'Log/chat.log')
logging.basicConfig(filename=logfilename, level=logging.DEBUG)
logger = logging.getLogger("logger")
usermessages = {}

class ChatbotAnswer:
    def __init__(self, word):
        self.current = LoadMessage(word)

    def robotBalloonMessage(self):
        if self.current is not None:
            return self.current.otherMessage
        else:
            return None

    def robotButtonOptions(self):
        if self.current is not None:
            if len(self.current.userOptions) == 1 and self.current.userOptions[0] == '':
                return None
            else:
                dict = {}
                i = 1
                for x in self.current.userOptions:
                    dict[x] = i
                    i = i + 1
                return dict

    def buttonAnswer(self, index):
        if self.current is not None:
            if self.current.messageLinks is None:
                self.current = self.current.messageLinks
            else:
                self.current = self.current.messageLinks[int(index) - 1]

            if self.current is not None:
                return self.current.otherMessage
            else:
                return usermessages['dialogEndMessage']


class UcChatBotView(QWidget):
    chatButtons = {}
    errorButtons = {}
    fixedBtnTxt = 'Düzelt'
    noFixedBtnTxt = 'Düzeltme'

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.c = Configuration()
        self.setupUi(self)


    def setupUi(self, Form):
        self.form = Form
        Form.setObjectName("Form")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        self.frame_sagMenuParent = QtWidgets.QFrame()
        self.frame_sagMenuParent.setObjectName("FrameSagMenuParent")
        self.frame_sagMenuParent.setSizePolicy(sizePolicy)
        self.frame_sagMenuParent.setMinimumSize(QtCore.QSize(335, 0))
        self.frame_sagMenuParent.setMaximumSize(QtCore.QSize(335, 16777215))
        self.frame_sagMenuParent.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_sagMenuParent.setFrameShadow(QtWidgets.QFrame.Raised)
        sizePolicy.setHeightForWidth(self.frame_sagMenuParent.sizePolicy().hasHeightForWidth())

        self.frame_robotImage = QtWidgets.QFrame(self.frame_sagMenuParent)
        self.frame_robotImage.setObjectName("FrameRobotImage")
        self.frame_robotImage.setFixedHeight(70)
        self.frame_robotImage.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_robotImage.setFrameShadow(QtWidgets.QFrame.Raised)
        self.label_robot = QtWidgets.QLabel(self.frame_robotImage)
        self.label_robot.setStyleSheet('image: url(:/icon/images/robot.png);')
        self.answertime = 3
        self.robottimer = QtCore.QTimer(self)
        self.robottimer.timeout.connect(self.timerTimeout)
        self.label_robot.setObjectName("LabelRobot")
        self.label_robot.setGeometry(QtCore.QRect(0, 0, 108, 70))

        self.icon = QtGui.QIcon()
        self.icon.addPixmap(QtGui.QPixmap(":/icon/images/chatnext.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_close = QtWidgets.QPushButton(self.frame_robotImage)
        self.pushButton_close.setObjectName("PushButtonFolding")
        self.pushButton_close.setGeometry(QtCore.QRect(250, 0, 91, 71))
        self.pushButton_close.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_close.setText("")
        self.pushButton_close.setIcon(self.icon)
        self.pushButton_close.setIconSize(QtCore.QSize(60, 45))
        self.pushButton_close.clicked.connect(self.closeForm)

        self.frame_lineEdit = QtWidgets.QFrame(self.frame_sagMenuParent)
        self.frame_lineEdit.setObjectName("FrameLineEdit")
        self.frame_lineEdit.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_lineEdit.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_lineEdit.setMinimumWidth(130)
        self.frame_lineEdit.setMinimumHeight(70)

        self.frame_userButton = QtWidgets.QFrame(self.frame_lineEdit)
        self.frame_userButton.setObjectName("FrameUserButton")
        self.frame_userButton.setContentsMargins(0, 0, 0, 0)
        self.frame_userButton.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_userButton.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_userButton.setVisible(False)


        self.VBoxUserButtons = QtWidgets.QVBoxLayout(self.frame_userButton)
        self.VBoxUserButtons.setContentsMargins(0, 0, 0, 0)

        self.lineEdit_sendMessage = QLineEdit(self.frame_lineEdit)
        self.lineEdit_sendMessage.setObjectName("LineEditSendMessage")
        self.lineEdit_sendMessage.setGeometry(QtCore.QRect(5, 45, 307, 55))
        self.lineEdit_sendMessage.setSizePolicy(sizePolicy)
        self.lineEdit_sendMessage.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.lineEdit_sendMessage.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.lineEdit_sendMessage.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.lineEdit_sendMessage.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)
        self.lineEdit_sendMessage.returnPressed.connect(self.enterSendAndReceive)
        self.lineEdit_sendMessage.setEnabled(True)
        self.lineEdit_sendMessage.setFocus()
        self.lineEdit_sendMessage.setFont(self.getfont())
        self.lineEdit_sendMessage.setPlaceholderText("Bir mesaj giriniz...")

        self.icon = QtGui.QIcon()
        self.icon.addPixmap(QtGui.QPixmap(":/icon/images/happy.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        self.pushButton_smile = QtWidgets.QPushButton(self.frame_lineEdit)
        self.pushButton_smile.setObjectName("PushButtonSmile")
        self.pushButton_smile.setGeometry(QtCore.QRect(0, 3, 60, 60))
        self.pushButton_smile.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_smile.setText("")
        self.pushButton_smile.setIcon(self.icon)
        self.pushButton_smile.setIconSize(QtCore.QSize(45, 45))
        self.pushButton_smile.clicked.connect(self.btnSmileClicked)

        self.frame_pushButton_trush = QtWidgets.QFrame(self.frame_lineEdit)
        self.frame_pushButton_trush.setGeometry(QtCore.QRect(260, 0, 60, 60))
        self.trush_icon = QtGui.QIcon()
        self.trush_icon.addPixmap(QtGui.QPixmap(":/icon/images/trash.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_trush = QtWidgets.QPushButton(self.frame_pushButton_trush)
        self.pushButton_trush.setObjectName("PushButtonTrush")
        self.pushButton_trush.setFixedWidth(37)
        self.pushButton_trush.setFixedHeight(37)
        self.pushButton_trush.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_trush.setText("")
        self.pushButton_trush.setIcon(self.trush_icon)
        self.pushButton_trush.setIconSize(QtCore.QSize(37, 37))
        self.pushButton_trush.clicked.connect(self.btnTrushClicked)

        self.textEdit_message = QtWidgets.QTextBrowser(self.frame_sagMenuParent)
        self.textEdit_message.setObjectName("TextEditMessage")
        self.textEdit_message.setSizePolicy(sizePolicy)
        self.textEdit_message.setMinimumSize(QtCore.QSize(300, 200))
        self.textEdit_message.append(self.robotBalloonMessage())
        log_mesaj_ekle("", self.robot_message)
        self.textEdit_message.setFont(self.getfont())
        self.textEdit_message.setReadOnly(True)
        self.textEdit_message.setOpenLinks(False)
        self.textEdit_message.setOpenExternalLinks(False)
        self.textEdit_message.anchorClicked.connect(self.HelpLinkClicked)

        self.verticalLayout_sagMenu = QtWidgets.QVBoxLayout()
        self.verticalLayout_sagMenu.setObjectName("verticalLayout_sagMenu")
        self.verticalLayout_sagMenu.addWidget(self.frame_robotImage)
        self.verticalLayout_sagMenu.addWidget(self.textEdit_message)
        self.verticalLayout_sagMenu.addWidget(self.frame_lineEdit)

        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.addWidget(self.frame_sagMenuParent, 0, 0, 1, 1)

        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame_sagMenuParent)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout_2.addLayout(self.verticalLayout_sagMenu, 0, 0, 1, 1)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))

    def closeForm(self):
        if self.form.isVisible():
            self.form.setVisible(False)
            pixmap = QtGui.QPixmap(":/icon/images/robot-rotate.png")
            pixmap2 = pixmap.scaled(pixmap.width() // 3, pixmap.height() // 3) #python3.10 da burada float gelirse çöküyor.
            self.parent.label_robot.setPixmap(pixmap2)
            self.parent.label_robot.setAlignment(Qt.AlignTop)
            self.parent.label_robot.setVisible(True)
            return False
        else:
            self.form.setVisible(True)
            return True

    def getfont(self):
        c = Configuration()
        font = QFont()
        font.setFamily(c.getEditorFont())
        font.setPointSize(c.getEditorFontSize())
        return font

    def btnSmileClicked(self):
        self.emojiPopupDialog()

    def HelpLinkClicked(self, event):
        dosyaAdi = event.path()
        helpDialog = TreeHelpDialog(dosyaAdi)
        helpDialog.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        helpDialog.setMinimumSize(QtCore.QSize(800, 500))
        helpDialog.setMaximumSize(QtCore.QSize(16777215, 16777215))
        helpDialog.exec_()

    def btnTrushClicked(self):
        self.trushPopupDialog()

    def get_emoji_codes(self):
        filename = self.initDataPaht() + "emoji.txt"
        emoji_dict = {}
        with open(filename, encoding="utf-8") as f:
            line = f.readline()
            line = line.replace('\n', "")
            while line != "":
                desc = "u'\\U{:08X}'".format(int(line, 16))
                emoji = ast.literal_eval(desc)
                emoji_dict[emoji] = desc
                line = f.readline()

        emojis = list(emoji_dict.keys())
        return emojis

    def emojiPopupDialog(self):
        self.smileWindow = QDialog()
        self.smileWindow.setWindowFlags(Qt.FramelessWindowHint | Qt.Popup)
        self.smileWindow.setMinimumSize(QSize(270, 380))
        self.smileWindow.setMaximumSize(QSize(270, 380))
        self.smileWindow.setWindowTitle("Emojiler")
        self.smileWindow.setWindowIcon(QIcon(':/icon/images/smile.png'))

        self.smileNewLayout = QtWidgets.QHBoxLayout()
        self.scrollArea = QtWidgets.QScrollArea()

        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.gridLayoutEmoji = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.smileNewLayout.addWidget(self.scrollArea)

        self.font = QFont()
        self.font.setPointSize(13)

        emojis = self.get_emoji_codes()
        self.item = 0
        for i in range(0, 24):
            for j in range(0, 5):
                if self.item < len(emojis):
                    self.emojiButton = QPushButton(emojis[self.item])
                    self.emojiButton.setMinimumWidth(30)
                    self.emojiButton.setMinimumHeight(30)
                    self.gridLayoutEmoji.addWidget(self.emojiButton, i, j)
                    self.emojiButton.setFont(self.font)
                    self.emojiButton.clicked.connect(lambda _, emoji=emojis[self.item]: self.clickeEmojiPushButton(emoji))
                    self.item = self.item + 1
                else:
                    break

        self.smileWindow.setLayout(self.smileNewLayout)

        self.smileWindow.move(self.parent.x() + self.parent.width() - self.width() + 10,
                              self.parent.y() + self.parent.height() - self.smileWindow.height() * 2 + self.pushButton_smile.height() * 5)
        if self.smileWindow.exec_():
            self.lineEdit_sendMessage.setText(self.lineEdit_sendMessage.text())

        self.lineEdit_sendMessage.setFocus()

    def clickeEmojiPushButton(self, emoji):
        if self.lineEdit_sendMessage.text() == '':
            self.lineEdit_sendMessage.setText(self.lineEdit_sendMessage.text() + emoji)
        else:
            self.lineEdit_sendMessage.setText(self.lineEdit_sendMessage.text() + " " + emoji)

    def currentTime(self):
        now = datetime.now()
        return now.strftime("%H:%M")

    def initDataPaht(self):
        c = Configuration()
        return c.getHomeDir() + c.getDataDirPath("data_directory")

    def initHtmlChatbotPaht(self):
        c = Configuration()
        return c.getHomeDir() + c.getHtmlChatbotPath("html_chatbot")

    def userBalloonMessage(self, userMessage=None):
        try:
            if userMessage is None:
                self.user_message = self.lineEdit_sendMessage.text()
            else:
                self.user_message = userMessage

            balloon_user_path = self.initHtmlChatbotPaht() + "ballon_user.html"
            file = open(str(balloon_user_path), 'r', errors='ignore')

            if self.user_message != '' and self.user_message != None:
                self.user_message = replaceToEmoji(self.user_message)
                if self.user_message is None:
                    if userMessage is None:
                        self.user_message = self.lineEdit_sendMessage.text()
                    else:
                        self.user_message = userMessage
                self.user_message = self.htmlCharacterControl(self.user_message, isUser=True)
                user_balloon_message = file.read().format(self.user_message, self.currentTime())
                return user_balloon_message

        except Exception as err:
            print("userError: {0}".format(err))

    def robotBalloonMessage(self, errorMessage=None, message=None, ButtonIndex=None, errorButtons=False):
        try:
            self.answerButton = None
            self.helpMessage = False
            balloon_robot_path = self.initHtmlChatbotPaht() + "ballon_robot.html"
            file = open(balloon_robot_path, 'r', errors='ignore')

            self.robot_message = ''
            if message is not None:
                self.robot_message = message
            else:
                user_message = self.lineEdit_sendMessage.text()
                if ButtonIndex is None and (user_message is None or user_message == ''):
                    self.robot_message = usermessages['startMessage']

                elif self.lineEdit_sendMessage.text() != '' and len(user_message) <= 3:
                    self.robot_message = "Öğrenmek istediğiniz konuyu daha detaylı yazabilir misiniz?"

                else:
                    if ButtonIndex is not None:
                        self.robot_message = self.robot_answer.buttonAnswer(ButtonIndex)
                    else:
                        self.robot_answer = ChatbotAnswer(user_message)
                        if self.robot_answer.robotBalloonMessage() is not None:
                            self.answerButton = self.robot_answer.robotButtonOptions()
                        else:
                            self.robot_answer = ChatbotEngine(user_message)
                            self.answerButton = None

                        self.robot_message = self.robot_answer.robotBalloonMessage()
                    self.answerButton = self.robot_answer.robotButtonOptions()
                    self.helpMessage = True
                if errorMessage is not None and errorMessage != '':
                    self.robot_message = errorMessage

            if errorButtons == True:
                self.AddUserHelpButton(['Evet', 'Hayır'], True)
            else:
                self.AddUserHelpButton(self.answerButton)

            self.robot_message = self.htmlCharacterControl(self.robot_message)
            robot_balloon_message = file.read().format(self.robot_message, self.currentTime())

            self.textEdit_message.verticalScrollBar().setValue((self.textEdit_message.verticalScrollBar().maximum()))
            if self.robot_message != "Nasıl yardımcı olabilirim?":
                parentdir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
                a = Thread(target=playsound, args=[parentdir + '/Data/Sounds/notification.mp3'], daemon=True)
                a.start()  # bell
            return robot_balloon_message

        except Exception as err:
            print("UserBallonError: {0}".format(err))

    def htmlCharacterControl(self, words, isUser=False):
        words = words.replace('"<"', '"&lt;"')
        words = words.replace('"<="', '"&lt;="')
        if isUser:
            words = words.replace('<', '&lt;')
        return words

    def enterSendAndReceive(self):
        mes = self.lineEdit_sendMessage.text()
        if self.frame_lineEdit.height() == 139 and self.errorButtons != {} and (mes.lower() == 'evet' or mes.lower() == 'hayır'):
            self.errorButtonClicked(mes)
        else:
            message = self.userBalloonMessage()
            if message != "" and message is not None:
                self.showUserMessage(message)
                time.sleep(0.2)
                # self.textEdit_message.setAlignment(Qt.AlignRight)
                self.textEdit_message.append("\n")
                self.textEdit_message.append(self.robotBalloonMessage())
                self.textEdit_message.append("\n")
        self.textEdit_message.setReadOnly(True)
        self.lineEdit_sendMessage.setText("")
        self.textEdit_message.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.textEdit_message.moveCursor(QtGui.QTextCursor.End)
        log_mesaj_ekle(self.user_message, self.robot_message)
        self.textEdit_message.setOpenExternalLinks(True)

    def AddUserHelpButton(self, answerButton, errorButtons=False):
        if answerButton is not None:
            self.createUserButton(sorted(answerButton, key=len), errorButtons)
            self.frame_userButton.setVisible(True)
        else:
            self.resizeObjects(70)
            self.frame_userButton.setVisible(False)

    def setChatbotEnable(self, boolValue):
        self.lineEdit_sendMessage.setEnabled(boolValue)
        self.pushButton_smile.setEnabled(boolValue)
        self.pushButton_trush.setEnabled(boolValue)

    def showUserMessage(self, message):
        self.textEdit_message.setAlignment(Qt.AlignLeft)
        self.textEdit_message.append(message)

    def createUserButton(self, buttonTextList, errorButtons):
        c = Configuration()
        font = QFont()
        font.setPointSize(c.getEditorFontSize())
        font.setFamily(c.getEditorFont())

        self.clearVerticalBoxLayout()

        self.sagmenuHBox1 = QtWidgets.QHBoxLayout()
        self.sagmenuHBox1.setContentsMargins(0, 0, 0, 0)
        self.VBoxUserButtons.addLayout(self.sagmenuHBox1)
        activeLine = self.sagmenuHBox1
        activeLineButtonCount = 1
        lineLetterCapacity = 37

        totalLineCount = 1
        doubleLineCount = 0

        i = 0
        for buttonText in buttonTextList:
            if (len(buttonText) > lineLetterCapacity or activeLineButtonCount > 3 or buttonText == self.fixedBtnTxt) and (buttonText != self.noFixedBtnTxt and activeLineButtonCount > 1):
                lineLetterCapacity = 37
                activeLineButtonCount = 1
                self.sagmenuHBox = QtWidgets.QHBoxLayout()
                self.sagmenuHBox.setContentsMargins(0, 0, 0, 0)
                activeLine = self.sagmenuHBox
                self.VBoxUserButtons.addLayout(activeLine)
                totalLineCount += 1

            if len(buttonText) > 37:
                if not errorButtons:
                    self.chatButtons[i] = newButton = QPushButton(self)
                else:
                    self.errorButtons[i] = newButton = QPushButton(self)
                newButton.setFixedHeight(52)
                newLabel = QLabel(buttonText, newButton)
                newLabel.setObjectName("chatButtonLabel")
                newLabel.setWordWrap(True)
                newLabel.setFont(font)
                newButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                newButton.move(0, 0)
                newButton.setObjectName("chatButton")
                newButton.setFont(font)
                doubleLineCount += 1
            else:
                if not errorButtons:
                    self.chatButtons[i] = newButton = QPushButton(buttonText, self)
                else:
                    self.errorButtons[i] = newButton = QPushButton(buttonText, self)
                newButton.setFixedHeight(35)
                newButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                newButton.move(0, 0)
                newButton.setObjectName("chatButton")
                newButton.setFont(font)
            lineLetterCapacity = lineLetterCapacity - len(buttonText)
            activeLineButtonCount += 1
            activeLine.addWidget(newButton)
            if not errorButtons:
                self.chatButtons[i].clicked.connect(
                    lambda checked, buttonText=buttonText: self.chatButtonClicked(buttonText))
            else:
                self.errorButtons[i].clicked.connect(
                    lambda checked, buttonText=buttonText: self.errorButtonClicked(buttonText))
            i += 1

        self.resizeObjects((totalLineCount-doubleLineCount+1.5)*34 + (doubleLineCount+1)*54)  #chatbota butonlar eklendikten sonra objeler yeniden yerleştirilmeli
        self.frame_lineEdit.setVisible(False)
        self.frame_lineEdit.setVisible(True)
        self.textEdit_message.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.textEdit_message.moveCursor(QtGui.QTextCursor.End)

    def clearVerticalBoxLayout(self):
        while self.VBoxUserButtons.count():
            child = self.VBoxUserButtons.takeAt(0)
            self.clearHorizontalBoxLayout(child)
            if child.widget():
                child.widget().deleteLater()

    def clearHorizontalBoxLayout(self, hbox):
        while hbox.count():
            child = hbox.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def trushButtonClicked(self, buttonText):
        if buttonText == 'Sohbeti Sil':
            self.textEdit_message.clear()
            self.resizeObjects(70)
            self.frame_userButton.setVisible(False)
        self.trushWindow.close()

    def chatButtonClicked(self, buttonText):
        message = self.userBalloonMessage(buttonText)
        self.showUserMessage(message)
        self.textEdit_message.append("\n")
        self.textEdit_message.append(self.robotBalloonMessage(ButtonIndex=self.answerButton[buttonText]))
        self.textEdit_message.append("\n")
        self.textEdit_message.moveCursor(QtGui.QTextCursor.End)
        log_mesaj_ekle(self.user_message, self.robot_message)

    def errorButtonClicked(self, buttonText):
        self.textEdit_message.append("\n")
        message = self.userBalloonMessage(buttonText)
        self.showUserMessage(message)
        self.textEdit_message.append("\n")
        message = replaceToEmoji('Görüşmek Üzere 😊')
        if buttonText.lower() == self.fixedBtnTxt.lower():
            codeText = copy.copy(self.text)
            temp = codeText[self.line].lstrip()
            if self.message == 'Girintisizlik beklenmiyor':
                codeText[self.line] = codeText[self.line][4:]
            elif self.message == 'Girintili kod bloğu bekleniyor':
                codeText[self.line] = "    "+codeText[self.line]
            else:
                if self.lineControl == True:
                    temp = codeText[self.line-1].lstrip()
                    codeText[self.line-1] = codeText[self.line-1].replace(temp, self.trueData)
                else:
                    codeText[self.line] = codeText[self.line].replace(temp, self.trueData)
            self.parent.textPad.SendScintilla(self.parent.textPad.SCI_SETTEXT, bytes('\n'.join(codeText), 'utf-8'))
            message = replaceToEmoji('Hatalı satır düzeltildi kodları tekrar çalıştırmayı deneyebilirsin 😊')
        if len(self.runErrors) > 0 and (buttonText.lower() == 'Evet'.lower()):
                self.errorButtons[0].setEnabled(False)
                self.errorButtons[1].setEnabled(False)
                QtCore.QTimer.singleShot(1, self.robotProcess)

        else:
            self.textEdit_message.append(self.robotBalloonMessage(message=message))
            self.textEdit_message.append("\n")
        self.textEdit_message.moveCursor(QtGui.QTextCursor.End)
        log_mesaj_ekle(self.user_message, self.robot_message)


    def resizeObjects(self, parentHeight):
        if parentHeight is None or parentHeight == 70:
            self.errorButtons = {}
        self.parentHeight = parentHeight
        self.frame_userButton.setGeometry(QtCore.QRect(0, 0, 317, int(parentHeight) - 70))

        if self.parentHeight is None:
            self.frame_lineEdit.setFixedHeight(70)
            self.parentHeight = self.frame_lineEdit.geometry().height()

        else:
            self.frame_lineEdit.setFixedHeight(int(self.parentHeight))

        self.lineEdit_sendMessage.setGeometry(5, int(self.parentHeight - 65), 307, 55)
        self.pushButton_smile.setGeometry(QtCore.QRect(0, int(self.parentHeight) - 67, 60, 60))
        self.frame_pushButton_trush.setGeometry(QtCore.QRect(260, int(self.parentHeight) - 56, 60, 60))


    def resizeEvent(self, event):
        self.textEdit_message.setMinimumSize(QtCore.QSize(300, 200))
        self.textEdit_message.setMaximumSize(QtCore.QSize(320, 16777215))
        self.textEdit_message.moveCursor(QtGui.QTextCursor.End)

    def RunErrorMessage(self, runErrors, text):
        if(len(runErrors)>0 and self.c.getChatbotStatusEnabled() == "True"):
            self.runErrors = runErrors.copy()
            self.text = text
            self.line = runErrors[0]['range']['start']['line']
                       
            try:
                self.rule = runErrors[len(runErrors)-1]["rule"]
            except:
                self.rule = "None"       
            try:
                self.message = runErrors[len(runErrors)-1]["message"]
            except:
                self.message = "None"
                
            if len(runErrors) < 5:  
                for i in range(len(runErrors)): 
                    if (runErrors[i]["message"] == "Girintisizlik beklenmiyor") or (runErrors[i]["message"] == "Girintili kod bloğu bekleniyor") :  
                        self.message =runErrors[i]["message"]    
            self.errorNo=1
            message = 'Yazdığınız kodlarda hata bulunmuştur. Hatanızı öğrenmek ve yardım almak ister misiniz?'.format(len(runErrors))


            isVisible = False
            if not self.form.isVisible():
                isVisible = self.closeForm()

            if message != "" and message is not None:
                time.sleep(0.2)
                self.textEdit_message.append(self.robotBalloonMessage(message=message, errorButtons=True))
                self.textEdit_message.setReadOnly(True)
                self.lineEdit_sendMessage.setText("")
                log_mesaj_ekle("", self.robot_message)

            self.textEdit_message.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            self.textEdit_message.moveCursor(QtGui.QTextCursor.End)
            return isVisible

    def trushPopupDialog(self):
        self.trushWindow = QDialog()
        self.trushWindow.setWindowFlags(Qt.FramelessWindowHint | Qt.Popup)
        self.trushWindow.setMinimumSize(QSize(300, 100))
        self.trushWindow.setMaximumSize(QSize(270, 240))

        self.trushNewLayout = QtWidgets.QHBoxLayout()
        self.scrollArea = QtWidgets.QScrollArea()

        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.gridLayoutTrush = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.trushNewLayout.addWidget(self.scrollArea)

        self.font = QFont()
        self.font.setPointSize(13)

        trushButton = ['Sohbeti Sil', 'Vazgeç']
        item = 0
        for buttonText in trushButton:
            self.trushButton = QPushButton(buttonText)
            self.trushButton.setObjectName("chatButton")
            self.trushButton.setMinimumWidth(80)
            self.trushButton.setMinimumHeight(40)
            self.gridLayoutTrush.addWidget(self.trushButton, 0, item)
            self.trushButton.setFont(self.font)
            self.trushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            self.trushButton.clicked.connect(lambda checked, buttonText=buttonText: self.trushButtonClicked(buttonText))
            item = item + 1

        self.trushWindow.setLayout(self.trushNewLayout)

        self.trushWindow.move(self.parent.x() + self.parent.width() - self.width() + 10,
                              self.parent.y() + self.parent.height() - self.trushWindow.height() * 2 + self.pushButton_smile.height() * 5)
        if self.trushWindow.exec_():
            self.lineEdit_sendMessage.setText(self.lineEdit_sendMessage.text())

        self.lineEdit_sendMessage.setFocus()

    def showRunErrorMessage(self):
        
        def SeeAddUserHelpButton(message):
            self.textEdit_message.append(self.robotBalloonMessage(message=message))
            if controlData:
                self.AddUserHelpButton([self.fixedBtnTxt, self.noFixedBtnTxt], True)  

        if self.text[self.line][-1] == ':' and self.text[self.line][-2] == ' ':
            tmp = self.text[self.line].split(' ')
            tmp = [x for x in tmp if x]
            tmp2 = ' '.join(tmp[0:-1]) + tmp[-1]
            self.text[self.line] = tmp2

        check = checkError()
        checkData = check.run(self.text, self.line , self.rule, self.message, self.runErrors)

        self.lineControl = False
        if checkData[0] == '#':
            check.returnData = []
            checkData = None
            self.lineControl = True
            checkData = check.run(self.text, self.line-1, self.rule, self.message, self.runErrors)

        self.trueData = checkData[0]
        descErrorMessage = self.runErrors[0]['message']
        controlData = self.control(self.trueData)
        self.runErrors.pop(0)

        tmp = descErrorMessage.split('\n')
        descErrorMessage = [x for x in tmp if x]
        descErrorMessage = descErrorMessage[-1]

        if self.trueData[0] == "#":
            message = '{0}. Hata <br /><br />{1}.<br/><p style="color:red"> Bu hataya çözüm bulamadım :( Dilerseniz bu satırın başına yorum işareti koyarak hata oluşmasını engelleyebilirim.:</p>&#9989;&nbsp; {2} <br/><br/> Bu şekilde değiştirmek ister misiniz?'.format(
            self.errorNo, descErrorMessage, controlData)
            SeeAddUserHelpButton(message)       
        elif self.trueData[-2:] == "..":
            message = '{0}. Hata <br /><br />{1}.<br/><p style="color:green">Bu hatayı düzeltmek için önerimiz şöyle:</p>&#9989;&nbsp; {2} <br/><br/> Bu hatayı düzeltmek istermisiniz?'.format(
                self.errorNo, descErrorMessage, controlData)
            self.textEdit_message.append(self.robotBalloonMessage(message=message)) 
        elif self.trueData[0:13]  == "girintihatasi":

            message = '{0}. Hata <br /><br />{1}.<br/><p style="color:green">Girinti Hatası Tespit Edildi. Düzeltmek İçin Tıklayabilirsiniz...</p>  <br/><br/> Bu hatayı düzeltmek istermisiniz?'.format(
                self.errorNo, descErrorMessage)
            SeeAddUserHelpButton(message)  
               
        else:    
            message = '{0}. Hata <br /><br />{1}.<br/><p style="color:green">Bu hatayı düzeltmek için önerimiz şöyle:</p>&#9989;&nbsp; {2} <br/><br/> Bu hatayı düzeltmek istermisiniz?'.format(
                self.errorNo, descErrorMessage, controlData)
            SeeAddUserHelpButton(message) 

        log_mesaj_ekle("", self.robot_message)
        self.errorNo += 1


    def timerTimeout(self):
        self.answertime -= 1
        if self.answertime == 0:
            self.showRunErrorMessage()
            self.label_robot.clear()
            self.label_robot.setStyleSheet('image: url(:/icon/images/robot.png);')

    def robotProcess(self):
        self.movie = QMovie(':/icon/images/robot_typing.gif')
        self.label_robot.setMovie(self.movie)
        self.movie.start()
        QtWidgets.qApp.processEvents(QtCore.QEventLoop.AllEvents, 50)
        self.answertime=3
        self.robottimer.start(1000)

    def ErrorButtonsClear(self, chatClear=False):
        self.resizeObjects(70)
        self.setChatbotEnable(True)
        if chatClear == True:
            self.textEdit_message.clear()

    def control(self,text):
        newText = ""
        charList = ["<",">","&",'"',"'",]
        charDict = {"<" : "&lt;",">" : "&gt;","&" : "&amp;",'"' : "&quot;","'" : "&apos;"}
        for i in text:
            if i in charList:
                i = charDict[i]
            newText += i
        return newText
        
def log_mesaj_ekle(mesaj, el_cevap):
    mesaj = deEmojify(mesaj)
    el_cevap = deEmojify(el_cevap)
    time = datetime.now()
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S:f')[:-3]
    if mesaj is not None and mesaj != '':
        logging.debug(' {0} -> Kullanici: {1}.'.format(timestamp, mesaj))
    logging.debug(' {0} -> Ro-Bot   : {1}'.format(timestamp, el_cevap))


def deEmojify(inputString):
    returnString = ""

    for character in inputString:
        try:
            character.encode("ascii")
            returnString += character
        except UnicodeEncodeError:
            replaced = unidecode(str(character))
            if replaced != '':
                returnString += replaced
            else:
                try:
                     returnString += "[" + unicodedata.name(character) + "]"

                except ValueError:
                     returnString += "[x]"

    return returnString

def LoadUserMessages():
    parentdir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    conn = sqlite3.connect(parentdir + '/Config/' + 'chatbot-database.db')
    c = conn.cursor()

    c.execute("SELECT MessageName, MessageValue from StaticMessages")
    messages = c.fetchall()

    for message in messages:
        usermessages[message[0]] = message[1]
