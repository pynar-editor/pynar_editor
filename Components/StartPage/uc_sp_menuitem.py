from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import icons_rc
import os
from configuration import Configuration


class UcSpMenuItem(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.c = Configuration()
        self.mainWindow = parent
        self.setStyleSheet("border: 0px solid black;")
        self.setupUi(self)

    def setupUi(self, uc_sp_menuitem):
        uc_sp_menuitem.setObjectName("ucSpMenuItem")
        uc_sp_menuitem.resize(400, 100)

        self.horizontalLayout = QtWidgets.QHBoxLayout(uc_sp_menuitem)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame = QtWidgets.QFrame(uc_sp_menuitem)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.setHorizontalSpacing(12)
        self.lbl_icon = QtWidgets.QLabel(self.frame)
        self.lbl_icon.setMaximumSize(QtCore.QSize(45, 45))
        self.lbl_icon.setObjectName("lblIcon")
        self.gridLayout.addWidget(self.lbl_icon, 0, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.lbl_title = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setFamily(self.c.getEditorFont())
        font.setPointSize(self.c.getEditorFontSize()+4)
        font.setBold(True)
        font.setWeight(75)

        self.lbl_title.setFont(font)
        self.lbl_title.setObjectName("lblTitleMenu")
        self.verticalLayout.addWidget(self.lbl_title)
        self.lbl_description = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setFamily(self.c.getEditorFont())
        font.setPointSize(self.c.getEditorFontSize())

        self.lbl_description.setFont(font)
        self.lbl_description.setWhatsThis("")
        self.lbl_description.setObjectName("lblDescriptionMenu")
        self.verticalLayout.addWidget(self.lbl_description)
        self.gridLayout.addLayout(self.verticalLayout, 0, 1, 1, 1)
        self.horizontalLayout.addWidget(self.frame)

        self.retranslateUi(uc_sp_menuitem)
        QtCore.QMetaObject.connectSlotsByName(uc_sp_menuitem)

    def retranslateUi(self, uc_sp_menuitem):
        _translate = QtCore.QCoreApplication.translate
        uc_sp_menuitem.setWindowTitle(_translate("UcSpMenuItem", "Form"))
        self.lbl_icon.setText(_translate("UcSpMenuItem", "icon"))
        self.lbl_title.setText(_translate("UcSpMenuItem", "Title"))
        self.lbl_description.setText(_translate("UcSpMenuItem", "Desc"))

    def setValue(self,menuName,description,icon):
        self.lbl_icon.setPixmap(QtGui.QPixmap(icon))
        self.lbl_icon.setScaledContents(True)
        self.lbl_title.setText(menuName)
        self.lbl_description.setText(description)