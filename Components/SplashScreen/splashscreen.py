# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from configuration import Configuration
from PyQt5.Qt import Qt
class UcSplashScreen(QDialog):
    def __init__(self):
        super().__init__()
        self.c = Configuration()
        self.setupUi(self)
        self.center()

    def setupUi(self, Form):
        Form.setObjectName("SplashScreen")
        Form.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        Form.setAttribute(Qt.WA_TranslucentBackground, True)
        Form.setModal(False)
        # Main widget
        self.container_widget = QWidget(Form)
        self.container_widget.setObjectName('CustomWidget')
        self.container_widget.resize(609, 249)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QtCore.QSize(610, 250))
        Form.setMaximumSize(QtCore.QSize(610, 250))
        Form.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)

        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("SplashScreenGrid")
        self.gridLayout.setContentsMargins(15,15,15,15)
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setObjectName("SplashFrame")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        # self.horizontalLayout.setSpacing(15)
        self.horizontalLayout.setContentsMargins(40, 10, 40, 10)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setPixmap(QtGui.QPixmap(":/icon/images/startLogo.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.horizontalLayout.setStretch(1, 3)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)

        self.retranslateUi(self.container_widget)
        QtCore.QMetaObject.connectSlotsByName(self.container_widget)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("SplashScreen", "SplashScreen"))

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)

    def closeScreen(self):
        self.close()
        return True