import os
from datetime import datetime

from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtWebChannel
from PyQt5 import QtWidgets, QtGui
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSizeGrip

from Components.MessageBox.CustomizeMessageBox import CustomizeMessageBox_Yes_No, CustomizeMessageBox_Ok
from configuration import Configuration
import base64
import requests
import uuid
import locale
import platform
from pathlib import Path


class Backend(QtCore.QObject):
    valueChanged = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._value = ""

    @QtCore.pyqtProperty(str)
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        self._value = v
        self.valueChanged.emit(v)


class UI_Exam(object):
    QtCore.qInstallMessageHandler(lambda x, y, z: None)
    def setupUi(self, Exam):
        self.openImage = []
        Exam.setObjectName("Exam")
        Exam.resize(850, 850)
        self.Exam = Exam
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Exam.sizePolicy().hasHeightForWidth())
        Exam.setSizePolicy(sizePolicy)

        Exam.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.verticalLayout = QtWidgets.QVBoxLayout(Exam)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(13, 13, 13, 13)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.titleBar = QtWidgets.QWidget(Exam)
        self.titleBar.setMinimumSize(QtCore.QSize(0, 30))
        self.titleBar.setMaximumSize(QtCore.QSize(16777215, 30))
        self.titleBar.setMouseTracking(True)
        self.titleBar.setObjectName("titleBar")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.titleBar)
        self.horizontalLayout.setContentsMargins(0, 0, 20, 0)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.title_label = QtWidgets.QLabel(self.titleBar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.title_label.sizePolicy().hasHeightForWidth())
        self.title_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(17)
        font.setBold(False)
        font.setWeight(50)
        self.title_label.setFont(font)
        self.title_label.setMouseTracking(True)
        self.title_label.setLayoutDirection(QtCore.Qt.LeftToRight)

        self.title_label.setScaledContents(False)
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.title_label.setWordWrap(False)
        self.title_label.setObjectName("title_label")
        self.horizontalLayout.addWidget(self.title_label, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

        self.maxBtn = QtWidgets.QPushButton(self.titleBar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.maxBtn.sizePolicy().hasHeightForWidth())
        self.maxBtn.setSizePolicy(sizePolicy)
        self.maxBtn.setFixedSize(QtCore.QSize(18, 18))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setKerning(True)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setKerning(True)
        self.maxBtn.setFont(font)
        self.maxBtn.setIcon(QIcon(':/icon/images/restore.png'))
        self.maxBtn.setIconSize(QtCore.QSize(10, 10))
        self.maxBtn.setObjectName("maxBtn")
        self.horizontalLayout.addWidget(self.maxBtn, 0, QtCore.Qt.AlignVCenter)

        self.closeBtn = QtWidgets.QPushButton(self.titleBar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.closeBtn.sizePolicy().hasHeightForWidth())
        self.closeBtn.setFixedSize(QtCore.QSize(18, 18))
        self.closeBtn.setSizePolicy(sizePolicy)
        self.closeBtn.setIcon(QIcon(':/icon/images/close-white.png'))
        self.closeBtn.setIconSize(QtCore.QSize(10, 10))
        self.closeBtn.setObjectName("closeBtn")
        self.horizontalLayout.addWidget(self.closeBtn, 0, QtCore.Qt.AlignVCenter)
        self.horizontalLayout.setStretch(0, 1)
        self.verticalLayout.addWidget(self.titleBar)
        self.centerStackedWidget = QtWidgets.QStackedWidget(Exam)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centerStackedWidget.sizePolicy().hasHeightForWidth())
        self.centerStackedWidget.setSizePolicy(sizePolicy)
        self.centerStackedWidget.setMinimumSize(QtCore.QSize(0, 0))
        self.centerStackedWidget.setStyleSheet("")
        self.centerStackedWidget.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.centerStackedWidget.setObjectName("centerStackedWidget")
        self.examPage = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.examPage.sizePolicy().hasHeightForWidth())
        self.examPage.setSizePolicy(sizePolicy)
        self.examPage.setStyleSheet("""QWidget#examPage{background-color:#202020;background-image: url(:/icon/images/exam-background.png);background-repeat: no-repeat;background-position: center;}""")

        self.examPage.setObjectName("examPage")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.examPage)
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout_2.setContentsMargins(20, 20, 20, 50)
        self.verticalLayout_2.setSpacing(20)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.textQuestionHtmlView = QWebEngineView(self.examPage)
        self.textQuestionHtmlView.page().setBackgroundColor(Qt.transparent)
        self.textQuestionHtmlView.setHtml('')
        self.startExamBtn = QtWidgets.QPushButton(self.examPage)
        self.startExamBtn.setGeometry(QtCore.QRect(5, 5, 50, 50))
        self.startExamBtn.setStyleSheet("QPushButton{background-color:transparent;color: #fff}")
        self.startExamBtn.setObjectName("startExamBtn")
        self.startExamBtn.setIcon(QIcon(':/icon/images/start.png'))
        self.startExamBtn.setIconSize(QtCore.QSize(45, 45))
        self.startExamBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.startExamBtn.setToolTip('Sınavı Başlat')

        self.sendExamBtn = QtWidgets.QPushButton(self.examPage)
        self.sendExamBtn.setMinimumSize(QtCore.QSize(50, 50))
        self.sendExamBtn.setGeometry(QtCore.QRect(56, 5, 50, 50))
        self.sendExamBtn.setStyleSheet("QPushButton{background-color:transparent;color: #fff}")
        self.sendExamBtn.setObjectName("sendExamBtn")
        self.sendExamBtn.setIcon(QIcon(':/icon/images/sendexam.png'))
        self.sendExamBtn.setIconSize(QtCore.QSize(45, 45))
        self.sendExamBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.sendExamBtn.setEnabled(False)
        self.sendExamBtn.setToolTip('Sınavı Gönder')

        self.timerLabel = QLabel(self.examPage)
        self.timerLabel.setStyleSheet("font: 36pt \"MS Shell Dlg 2\";color: #ff1f3d;")
        self.timerLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

        self.time_left_int = self.DURATION_INT
        self.timer = QtCore.QTimer(self)
        self.update_gui()

        self.verticalLayout_2.setStretch(0, 1)
        self.centerStackedWidget.addWidget(self.examPage)


        self.verticalLayout.addWidget(self.centerStackedWidget)
        self.statusBarExam = QtWidgets.QWidget(Exam)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statusBarExam.sizePolicy().hasHeightForWidth())
        self.statusBarExam.setSizePolicy(sizePolicy)
        self.statusBarExam.setMinimumSize(QtCore.QSize(0, 30))
        self.statusBarExam.setMaximumSize(QtCore.QSize(16777215, 30))

        self.statusBarExam.setObjectName("statusBarExam")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.statusBarExam)
        self.horizontalLayout_3.setContentsMargins(20, 0, 20, 0)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.ipInfo = QtWidgets.QLabel(self.statusBarExam)

        self.ipInfo.setStyleSheet(".QLabel{color:white;background:#202020}")
        self.ipInfo.setObjectName("ipInfo")
        self.horizontalLayout_3.addWidget(self.ipInfo, 0, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        self.verticalLayout.addWidget(self.statusBarExam)

        self.retranslateUi(Exam)
        self.centerStackedWidget.setCurrentIndex(0)
        self.closeBtn.clicked.connect(self.examClose)
        self.maxBtn.clicked.connect(self.maxAndNormal)

        backend = Backend(self)
        backend.valueChanged.connect(self.foo_function)

        self.channel = QtWebChannel.QWebChannel()
        self.channel.registerObject("backend", backend)
        self.textQuestionHtmlView.page().setWebChannel(self.channel)
        self.c = Configuration()

    @QtCore.pyqtSlot(str)
    def foo_function(self, value):
        if value[0:1] not in self.openImage:
            self.openImage.append(value[0:1])
            self.box = Frame(val=value[0:1], imgs=self.openImage, les=self.lesson)
            l = QtWidgets.QVBoxLayout(self.box.contentWidget())
            l.setContentsMargins(0, 0, 0, 0)
            img_widget = ImageWidget(value[1:].replace('data:image/png;base64,', ''))
            img_widget.setMinimumWidth(300)
            img_widget.setMinimumHeight(300)
            l.addWidget(img_widget)
            self.box.show()

    def retranslateUi(self, Exam):
        _translate = QtCore.QCoreApplication.translate
        Exam.setWindowTitle(_translate("Exam", "Sınav Pencereniz"))
        self.ipInfo.setText(_translate("Start",
                                       "Sınavı başlattığınızda işlemi geri alamazsınız. Süre bitimine kadar göndermediyseniz cevaplarınız otomatik gönderilir."))

    def maxAndNormal(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def examClose(self):
        if self.IsExamStarted:
            self.sendExam = SendWindow(self, self.startExamBtn, self.time_left_int, self.timer, self.timerTimeout)
        else:
            self.parent.openExam = None
            self.close()

    def resizeEvent(self, event):
        self.timerLabel.setGeometry(QtCore.QRect(self.width() - 300, 3, 260, 70))
        self.textQuestionHtmlView.setGeometry(QtCore.QRect(27, 150, self.geometry().width() - 80, 80))
        self.textQuestionHtmlView.setFixedHeight(self.height() - 220)

    def initHtmlExamPath(self):
        return self.c.getHomeDir() + self.c.getHtmlExamPath("html_exam")


class ShadowWindow(QWidget):

    def __init__(self):
        super(ShadowWindow, self).__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.SHADOW_WIDTH = 15


class ExamWindow(UI_Exam, ShadowWindow):

    def __init__(self, parent, token, questionInfo):
        super(ExamWindow, self).__init__()
        self.setWindowIcon(QIcon(':/icon/images/start.png'))
        self.DURATION_INT = int(questionInfo['exam_time']) * 60
        self.lesson = questionInfo['exam_name']
        self.parent = parent
        self.images = []
        self.token = token
        self.isStarted = False
        self.questionInfo = questionInfo
        self.setupUi(self)
        self.inicializao()
        self.__leftButtonPress = False
        self.__movePoint = QPoint()
        self.IsExamStarted = False
        self.title_label.setText(self.lesson)
        self.sendExam = None
        self.c = Configuration()
        self.serverAddress = self.c.getServerAddress()

    def inicializao(self):
        self.startExamBtn.clicked.connect(self.startExamClick)
        self.sendExamBtn.clicked.connect(self.sendExamClick)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.titleBar.rect().contains(event.pos()):
                self.__leftButtonPress = True
                self.__movePoint = event.pos()

    def mouseMoveEvent(self, event):
        if self.__leftButtonPress:
            globalPos = event.globalPos()
            self.move(globalPos - self.__movePoint)

    def mouseReleaseEvent(self, event):
        self.__leftButtonPress = False

    def startExamClick(self):
        mess = "<b>" + self.lesson + "</b> adlı sınavınızı başlatmak istediğinize emin misiniz?<br/>Bu işlem <b>geri alınamaz.</b>"
        CustomizeMessageBox_Yes_No(mess, clickAccept=self.startButton)


    def setExamLogFileName(self):
        timestamp = datetime.now().strftime('%Y_%m_%d-%H_%M_%S.%f')[:-3]
        data_folder = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
        data_folder = Path(data_folder)
        data_folder = data_folder / self.c.getExamLogFolder()
        self.file_to_write = data_folder / (str(self.lesson) + "-" + str(timestamp) + ".json")
        self.checkerExamLog=False

        if (not os.path.exists(self.file_to_write)):
            with open(self.file_to_write, 'w', encoding='utf-8') as file:
                file.write('[\n]')

    def startButton(self):
        if self.parent.notebook.currentIndex() == -1:
            CustomizeMessageBox_Ok('Sınava başlamadan önce sadece 1 adet boş kod editörü açmış olmanız ve sınavınız bitene kadar kapatmamanız gerekmektedir.', "critical")
        elif self.parent.notebook.currentIndex() > 0:
            CustomizeMessageBox_Ok('Sadece 1 adet boş kod editörü açmış olmanız ve sınavınız bitene kadar kapatmamanız gerekmektedir.', "critical")
        elif self.parent.textPad.text() != '':
            CustomizeMessageBox_Ok('Kod editörünüz boş olmalıdır ve sınavınız bitene kadar kapatmamanız gerekmektedir.', "critical")
        else:  # Birden fazla açık varmı diye bakılmalı
            self.setExamLogFileName()
            self.isStarted = True
            self.startExamBtn.setEnabled(False)
            self.sendExamBtn.setEnabled(True)
            self.time_left_int = self.DURATION_INT
            self.timer.timeout.connect(self.timerTimeout)
            self.timerLabel.setStyleSheet("font: 36pt \"MS Shell Dlg 2\";color: #202020; border:none;")
            self.timerWindow = TimerWindow(self.time_left_int, parent=self)
            self.timerWindow.timerWidget.timer.start(1000)
            self.timer.start(1000)
            self.IsExamStarted = True
            self.loadQuestion()

    def loadQuestion(self):
        exam = self.fetchExam()
        if exam != 0:
            self.lesson = exam['exam']['exam_name']
            if exam != 0:
                img_names = exam['question']['medias']
                if len(img_names) > 0:
                    for i in img_names:
                        if i['file_name'] is not None:
                            img = self.fetchImage(exam['question']['id'], i['file_name'])
                            self.images.append(img)

            # Alınan Bilgilerin Html'e basılması
            path = self.initHtmlExamPath() + "classicTemplate.html"
            with open(path, 'r', encoding='utf8') as f:
                html = f.read()
                if len(self.images) > 0:
                    img_str = ""
                    for index, image in enumerate(self.images):
                        i = str(index)
                        img_str = img_str + "<img id=\"img" + i + "\" src=\"" + str(
                            image.decode("utf-8")) + "\" onclick='func_img" + i + "()'/>"

                    self.html = html.replace('images', img_str)
                else:
                    self.html = html.replace('images', '')
                self.html = self.html.replace('metin', str("<b style=\"color:red\">Soru: </b>" + exam['question']['question']))
                self.examPage.setStyleSheet("QWidget#examPage{background-color:#202020;background-image: none;}")
                self.textQuestionHtmlView.setHtml(self.html)

    def timerTimeout(self):
        self.time_left_int -= 1
        if self.time_left_int == 0:
            self.timerWindow.close()
            self.close()
        self.update_gui()

    def update_gui(self):
        minsec = self.secs_to_minsec(self.time_left_int)
        self.timerLabel.setText(minsec)

    def secs_to_minsec(self, secs: int):
        hours = secs // (60 * 60)
        mins = (secs - hours * 60 * 60) // 60
        secs = secs - (hours * 60 * 60) - (mins * 60)
        minsec = f'{hours:02}:{mins:02}:{secs:02}'
        return minsec

    def sendExamClick(self):
        self.timer.stop()
        self.sendExam = SendWindow(self, self.startExamBtn, self.time_left_int, self.timer, self.timerTimeout)

    def showTime(self):
        time = QDateTime.currentDateTime()
        timeDisplay = time.toString('hh:mm:ss')
        self.timerLabel.setText(timeDisplay)

    def fetchExam(self):
        id = self.questionInfo["exam_id"]
        myobj = {'start_exam_id': id}
        headers = {'Authorization': 'Bearer ' + self.token}
        exams = requests.post(self.serverAddress + "/api/v1/user/student/exams", headers=headers, data=myobj)
        res_json = exams.json()
        if res_json['ok']:
            return res_json['result']['data']
        else:
            return 0

    def fetchImage(self, questionId, media):
        examId = self.questionInfo["exam_id"]
        myobj = {'exam_id': examId, 'question_id': questionId}
        headers = {'Authorization': 'Bearer ' + self.token}
        exams = requests.post(self.serverAddress + "/api/v1/user/student/media/" + media, headers=headers, data=myobj)
        return exams.content

    def closeEvent(self, event):
        if self.sendExam is None:
            self.examClose()
        self.parent.ExamWindow = None

class SendWindow(QMainWindow):
    def __init__(self, parent, startExamBtn, time_left_int, timer, timerTimeout):
        super().__init__()

        self.startExamBtn = startExamBtn
        self.time_left_int = time_left_int
        self.timer = timer
        self.timerTimeout = timerTimeout
        self.parent = parent
        self.c = Configuration()
        self.serverAddress = self.c.getServerAddress()

        if time_left_int > 0:
            mess = "Sınavınızı tamamlamak istediğinize emin misiniz?<br/>Bu işlem <b>geri alınamaz.</b> <br/>Şuan <b>sınav sürenizin</b> gittiğini unutmayınız"
            CustomizeMessageBox_Yes_No(mess, clickAccept=self.stopExam1, clickCancel=self.stopExam2)
        else:
            self.stopExam1()

    def stopExam1(self):
        res = self.finishExam()
        self.parent.parent.openExam = None
        if self.parent.sendExam is None:
            self.parent.sendExam = self
        self.parent.close()
        self.parent.timerWindow.close()
        if res:
            self.parent.parent.setExamImage()
            CustomizeMessageBox_Ok('Sınavınız başarıyla tamamlanmıştır.', "information")
        else:
            CustomizeMessageBox_Ok('Bir Hata ile karşılaşıldı. Öğretmeniniz ile iletişime geçiniz', "critical")

    def stopExam2(self):
            self.startExamBtn.setEnabled(False)
            self.time_left_int = self.parent.DURATION_INT
            self.timer.timeout.connect(self.timerTimeout)
            self.timer.start(1000)

    def finishExam(self):
        self.textPad = self.parent.parent.textPad
        if self.textPad.filename == None:
            filename = self.parent.lesson.split(".")

            if len(filename) == 1:
                filename.append(".py")
            else:
                if filename[1] != ".py":
                    filename[1] = ".py"

            filename = filename[0] + '_' + str(str(datetime.now()).split('.')[0]) + filename[1]
            filename = filename.replace(':', '-')
            plt = platform.system()
            if plt == "Windows":
                self.directoryPath = self.c.checkPath(os.environ['USERPROFILE']) + "/Documents/PynarKutu/"
                if not os.path.exists(self.directoryPath):
                    os.mkdir(self.directoryPath)
                self.directoryPath = os.path.join(self.directoryPath)

            elif plt == "Linux":
                locale.setlocale(locale.LC_ALL, "")
                message_language = locale.getlocale(locale.LC_MESSAGES)[0]
                self.directoryPath = os.path.join(os.environ['HOME'])
                if message_language == 'tr_TR':
                    self.directoryPath += '/Belgeler/PynarKutu/'
                else:
                    self.directoryPath += '/Documents/PynarKutu/'
                if not os.path.exists(self.directoryPath):
                    os.mkdir(self.directoryPath)

            with open(self.directoryPath + filename, "w", encoding='utf8') as f:
                f.write(self.textPad.text())

            self.textPad.filename = self.directoryPath + filename

        else:
            text = self.textPad.text()
            try:
                with open(self.textPad.filename, 'w', newline='', encoding='utf8') as file:
                    file.write(text)

            except Exception as e:
                CustomizeMessageBox_Ok(str(e), "critical")


        id = self.parent.questionInfo["exam_id"]
        server_update_url = self.serverAddress + '/api/v1/user/student/exams'
        headers = {'Authorization': 'Bearer ' + self.parent.token}

        logFile = str(self.parent.file_to_write.as_posix())
        file_dict = {
            'file': (self.textPad.filename.split('/').pop(-1), open(self.textPad.filename, 'r', encoding="utf-8"), 'text/x-python'),
            'logs': (logFile.split('/').pop(-1), open(logFile, 'r',  encoding="utf-8"),
                     'application/json'),
        }

        myobj = {'mac_address': hex(uuid.getnode()),
                 'finish_exam_id': id}

        x = requests.post(server_update_url, files=file_dict, headers=headers, data=myobj, verify=False)
        res_json = x.json()
        if (res_json['ok'] == True):
            return True
        else:
            return res_json['description']


class Label(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        self.p = QPixmap()

    def setPixmap(self, p):
        self.p = p
        self.update()

    def paintEvent(self, event):
        if not self.p.isNull():
            painter = QPainter(self)
            painter.setRenderHint(QPainter.SmoothPixmapTransform)
            painter.drawPixmap(self.rect(), self.p)


class ImageWidget(QWidget):
    def __init__(self, img_base64=None):
        QWidget.__init__(self)
        lay = QVBoxLayout(self)
        lb = Label(self)
        pm = QPixmap()
        pm.loadFromData(base64.b64decode(img_base64))
        lb.setPixmap(pm)
        lay.addWidget(lb)


class TitleBar(QtWidgets.QDialog):
    def __init__(self, parent=None, les=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.parent = parent
        self.setWindowFlags(Qt.FramelessWindowHint)
        css = """
        QWidget{
            Background: black;
            color:white;
            font:12px bold;
            font-weight:bold;
            height: 11px;
        }
        QDialog{
            font-size:12px;
            color: black;
        }
        QToolButton{
            Background:black;
            font-size:11px;
        }
        """
        self.setAutoFillBackground(True)
        self.setBackgroundRole(QtGui.QPalette.Highlight)
        self.setStyleSheet(css)
        self.btnMinimize = QtWidgets.QToolButton(self)
        self.btnMinimize.setIcon(QtGui.QIcon(':/icon/images/minimize2.png'))
        self.btnMaximize = QtWidgets.QToolButton(self)
        self.btnMaximize.setIcon(QtGui.QIcon(':/icon/images/resize2.png'))
        self.btnMaximize.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnMinimize.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        btnClose = QtWidgets.QToolButton(self)
        btnClose.setIcon(QtGui.QIcon(':/icon/images/close2.png'))
        btnClose.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnMinimize.setMinimumHeight(15)
        btnClose.setMinimumHeight(15)
        self.btnMaximize.setMinimumHeight(15)
        label = QtWidgets.QLabel(self)
        label.setText(les + " sınavına ait görüntü")
        hbox = QtWidgets.QHBoxLayout(self)
        hbox.addWidget(label)
        hbox.addWidget(self.btnMinimize)
        hbox.addWidget(self.btnMaximize)
        hbox.addWidget(btnClose)
        self.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.maxNormal = False
        btnClose.clicked.connect(self.close)
        self.btnMinimize.clicked.connect(self.showSmall)
        self.btnMaximize.clicked.connect(self.showMaxRestore)

    def showSmall(self):
        self.parent.showMinimized()

    def showMaxRestore(self):
        if self.maxNormal:
            self.parent.showNormal()
            self.maxNormal = False
        else:
            self.parent.showMaximized()
            self.maxNormal = True

    def close(self):
        if self.parent.val in self.parent.imgs:
            self.parent.imgs.remove(self.parent.val)
        self.parent.close()


class Frame(QtWidgets.QFrame):
    def __init__(self, parent=None, les=None, imgs=None, val=None):
        QtWidgets.QFrame.__init__(self, parent)
        self.imgs = imgs
        self.val = val
        self.setMinimumSize(500, 500)
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setStyleSheet("""QFrame{Background:  black; color:white; font:13px; font-weight:bold; padding:0px; } """)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setMouseTracking(True)
        self.m_titleBar = TitleBar(self, les=les)
        self.m_content = QtWidgets.QWidget(self)
        vbox = QtWidgets.QVBoxLayout(self)
        vbox.addWidget(self.m_titleBar)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(0)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.m_content)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(0)
        vbox.addLayout(layout)

        self.gripSize = 16
        self.grips = []
        for i in range(4):
            grip = QSizeGrip(self)
            grip.resize(self.gripSize, self.gripSize)
            self.grips.append(grip)

    def contentWidget(self):
        return self.m_content

    def resizeEvent(self, event):
        QtWidgets.QFrame.resizeEvent(self, event)
        rect = self.rect()
        self.grips[1].move(rect.right() - self.gripSize, 0)
        self.grips[2].move(
            rect.right() - self.gripSize, rect.bottom() - self.gripSize)
        self.grips[3].move(0, rect.bottom() - self.gripSize)

class TimerLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self, ExamWindow):
        super().__init__()
        self.ExamWindow = ExamWindow


    def mouseReleaseEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton:
            self.clicked.emit()
            self.ExamWindow.activateWindow()

class TimerWidget(QWidget):
    def __init__(self, time_left_int, ExamWindow):
        super().__init__()
        self.ExamWindow = ExamWindow
        grid = QGridLayout()
        grid.setContentsMargins(0,0,0,0)
        self.setLayout(grid)
        grid.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.setCursor(QtGui.QCursor(QtCore.Qt.SizeAllCursor))
        self.timerLabel = TimerLabel(ExamWindow=self.ExamWindow)
        self.timerLabel.setText('00:12:00')
        self.timerLabel.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.timerLabel.setStyleSheet(""" QLabel{font: 36pt \"MS Shell Dlg 2\";color: #ff1f3d; border:none;}
                                          QToolTip { font: 16pt; background-color: white;color: black;border: black solid 1px}""")
        self.timerLabel.setFixedWidth(250)
        self.timerLabel.setFixedHeight(50)
        self.timerLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.timerLabel.setToolTip('Timerın ekrandaki konumunu sürükleyerek değiştirebilirsiniz.')
        self.time_left_int = time_left_int
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.timerTimeout)
        grid.addWidget(self.timerLabel, 0, 0)

    def timerTimeout(self):
        self.time_left_int -= 1
        if self.time_left_int == 0:
            self.close()
        self.update_gui()

    def update_gui(self):
        minsec = self.secs_to_minsec(self.time_left_int)
        self.timerLabel.setText(minsec)

    def secs_to_minsec(self, secs: int):
        hours = secs // (60 * 60)
        mins = (secs - hours * 60 * 60) // 60
        secs = secs - (hours * 60 * 60) - (mins * 60)
        minsec = f'{hours:02}:{mins:02}:{secs:02}'
        return minsec


class TimerWindow(QMainWindow):
    def __init__(self, time_left_int, parent):
        super().__init__()
        self.ExamWindow = parent
        self.setWindowFlags(
            QtCore.Qt.Window | QtCore.Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool)
        self.setFixedHeight(90)
        self.setFixedWidth(260)
        self.setStyleSheet("QWidget{background-color:#202020; border:2px solid red;}")
        screen = QDesktopWidget().screenGeometry()
        self.move((screen.width() - self.width()), 0)

        self.timerWidget = TimerWidget(time_left_int, ExamWindow=self.ExamWindow)
        self.setCentralWidget(self.timerWidget)
        self.show()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.offset = event.pos()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.offset is not None and event.buttons() == QtCore.Qt.LeftButton:
            self.move(self.pos() + event.pos() - self.offset)
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.offset = None
        super().mouseReleaseEvent(event)
