from PyQt5.QtWidgets import (QMessageBox, QLabel, QRadioButton,
                             QPushButton, QListWidget, QTabWidget,
                             QTextEdit,QFrame)


class MessageBox(QMessageBox):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName("widgetMessageBox")


class Label(QLabel):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName("widgetLabel")


class WhiteLabel(QLabel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName("widgetWhiteLabel")

class PushButton(QPushButton):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName("widgetPushButton")


class RadioButton(QRadioButton):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName("widgetRadioButton")

class ListWidget(QListWidget):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName("widgetListWidget")
        self.verticalScrollBar().setObjectName("widgetVerticalScrollBar")
        self.horizontalScrollBar().setObjectName("widgetHorizontalScrollBar")


class TabWidget(QTabWidget):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName("widgetTabWidget")
        self.tabBar().setObjectName("widgetTabBar")
            

class TextEdit(QTextEdit):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName("widgetTextEdit")
        self.verticalScrollBar().setObjectName("widgetTextEditScrollBarV")
        self.horizontalScrollBar().setObjectName("widgetTextEditScrollBarH")

