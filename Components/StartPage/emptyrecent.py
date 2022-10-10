# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import icons_rc
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QFont
from configuration import Configuration

class UcEmptyRecent(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.mainWindow = parent

        self.c = Configuration()
        self.font = QtGui.QFont()
        self.font.setFamily(self.c.getEditorFont())
        self.font.setPointSize(self.c.getEditorFontSize())
        self.font.setBold(True)
        self.font.setWeight(75)

        self.setupUi(self)

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(503, 658)
        Form.setLayoutDirection(QtCore.Qt.LeftToRight)
        Form.setStyleSheet("background-color: rgb(245, 245, 245);")
		
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
		
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
		
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        spacerItem = QtWidgets.QSpacerItem(20, 30, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 3, 0, 1, 1)
		
        self.lbl_info = QtWidgets.QLabel(self.frame)
        self.lbl_info.setWordWrap(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_info.sizePolicy().hasHeightForWidth())
        self.lbl_info.setSizePolicy(sizePolicy)
        self.lbl_info.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_info.setObjectName("label_2")
        self.lbl_info.setFont(self.font)
        self.lbl_info.setStyleSheet("color:gray;")
        self.gridLayout_2.addWidget(self.lbl_info, 2, 0, 1, 1)
		
        self.lbl_image = QtWidgets.QLabel(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_image.sizePolicy().hasHeightForWidth())
        self.lbl_image.setSizePolicy(sizePolicy)
        self.lbl_image.setMaximumSize(QtCore.QSize(16777215, 177))
        self.lbl_image.setPixmap(QtGui.QPixmap(":/icon/images/empty_recent.png"))
        self.lbl_image.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_image.setObjectName("label")
        self.gridLayout_2.addWidget(self.lbl_image, 1, 0, 1, 1)
		
        spacerItem1 = QtWidgets.QSpacerItem(20, 30, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem1, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.lbl_info.setText(_translate("Form", "Açık Dosya Bulunamadı! \n"
" Yandaki menüden Yeni Proje oluşturabilir veya mevcut projenizi açabilirsiniz."))

