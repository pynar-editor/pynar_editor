from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import icons_rc
import os
from configuration import Configuration

class UcSpExamItem(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.mainWindow = parent
        self.c = Configuration()
        self.setStyleSheet("border: 0px solid black;")
        self.setupUi(self)

    def setupUi(self, uc_sp_recentitem):
        uc_sp_recentitem.setObjectName("ucSpExamItem")
        uc_sp_recentitem.resize(430, 110)
        self.gridLayout_2 = QtWidgets.QGridLayout(uc_sp_recentitem)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.frame = QtWidgets.QFrame(uc_sp_recentitem)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setObjectName("gridLayout")
        self.lbl_icon = QtWidgets.QLabel(self.frame)
        self.lbl_icon.setMaximumSize(QtCore.QSize(60, 65))
        self.lbl_icon.setPixmap(QtGui.QPixmap(":/icon/images/quiz.png"))
        self.lbl_icon.setScaledContents(True)
        self.lbl_icon.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.lbl_icon.setObjectName("lblIcon")
        self.gridLayout.addWidget(self.lbl_icon, 0, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()

        self.verticalLayout.setObjectName("verticalLayout")
        self.lbl_title = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setFamily(self.c.getEditorFont())
        font.setPointSize(self.c.getHistoryMenuFontSize()+5)
        font.setBold(True)
        # font.setWeight(55)
        self.lbl_title.setFont(font)
        self.lbl_title.setObjectName("lblTitleExam")
        self.lbl_title.setStyleSheet('color:#0070ba;')
        self.verticalLayout.addWidget(self.lbl_title)
        self.lbl_description = QtWidgets.QLabel(self.frame)
        self.lbl_description.setFixedWidth(205)
        self.lbl_description.setWordWrap(True)
        font = QtGui.QFont()
        font.setFamily(self.c.getEditorFont())
        font.setPointSize(self.c.getHistoryMenuFontSize()+3)
        self.lbl_description.setFont(font)
        self.lbl_description.setStyleSheet('color:#394b58;')
        self.lbl_description.setWhatsThis("")
        self.lbl_description.setObjectName("lblDescriptionExam")
        self.verticalLayout.addWidget(self.lbl_description)
        self.gridLayout.addLayout(self.verticalLayout, 0, 1, 1, 1)
        self.gridLayout_2.addWidget(self.frame, 0, 0, 1, 1)

        self.retranslateUi(uc_sp_recentitem)
        QtCore.QMetaObject.connectSlotsByName(uc_sp_recentitem)

    def retranslateUi(self, uc_sp_recentitem):
        _translate = QtCore.QCoreApplication.translate
        uc_sp_recentitem.setWindowTitle(_translate("UcSpExamItem", "Form"))
        self.lbl_title.setText(_translate("UcSpExamItem", "Title"))
        self.lbl_description.setText(_translate("UcSpExamItem", "Desc"))

    def setValue(self,filename,filepath,opendate):
        self.lbl_title.setText(filename)
        self.lbl_description.setText(filepath)
        self.lbl_description.setToolTip(filepath)