from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QAction, QVBoxLayout, QToolBar, QFrame
from PyQt5.Qt import Qt

# QAction Overwrite
class QAction(QAction):
    def __init__(self, a=None, b=None, parent=None):
        if parent:
            super().__init__(a, b, parent)
        elif b:
            super().__init__(b, parent)
        elif a:
            super().__init__(parent)
        # QAction her çalıştığında logfunction fonksiyonunu çalıştır
        self.triggered.connect(self.log_action)

    # Çalıştırılan QAction'ı log dosyasına kaydet.
    def log_action(self, extra=""):
        if (self.sender().text() == "Aç"):
            return
        message = "Eylem: " + self.sender().text()
        self.parentWidget().parent.log_messenger(message)
## Overwrite End

class ToolBar(QWidget):
    def __init__(self, parent,menu):
        super(QWidget, self).__init__(parent)
        self.parent = parent
        self.tabMenu = menu
        self.CreateToolBar()


    def CreateToolBar(self):
        # Dosya toolbar
        self.toolbarFile = QToolBar()
        self.toolbarFile.setStyleSheet("QToolButton::hover {background-color: #6b899f};")
        self.toolbarFile.setFixedHeight(50)
        self.toolbarFile.setIconSize(QSize(50, 50))
        self.toolbarFile.setObjectName("toolbar")
        self.toolbarFile.setMovable(False)
        self.toolbarFile.setContextMenuPolicy(Qt.PreventContextMenu)
        self.CreateFileActions()

        # Ayarlar toolbar
        self.toolbarSettings = QToolBar()
        self.toolbarSettings.setStyleSheet("QToolButton::hover {background-color: #6b899f};")
        self.toolbarSettings.setFixedHeight(50)
        self.toolbarSettings.setIconSize(QSize(50, 50))
        self.toolbarSettings.setObjectName("toolbarSettings")
        self.toolbarSettings.setMovable(False)
        self.toolbarSettings.setContextMenuPolicy(Qt.PreventContextMenu)
        self.CreateSettingsActions()

        # Bulut toolbar
        self.toolbarCloud = QToolBar()
        self.toolbarCloud.setStyleSheet("QToolButton::hover {background-color: #6b899f};")
        self.toolbarCloud.setFixedHeight(50)
        self.toolbarCloud.setIconSize(QSize(50, 50))
        self.toolbarCloud.setObjectName("toolbarCloud")
        self.toolbarCloud.setMovable(False)
        self.toolbarCloud.setContextMenuPolicy(Qt.PreventContextMenu)
        self.CreateCloudActions()

        # Help toolbar
        self.toolbarHelp = QToolBar()
        self.toolbarHelp.setStyleSheet("QToolButton::hover {background-color: #6b899f};")
        self.toolbarHelp.setFixedHeight(50)
        self.toolbarHelp.setIconSize(QSize(50, 50))
        self.toolbarHelp.setObjectName("toolbarHelp")
        self.toolbarHelp.setMovable(False)
        self.toolbarHelp.setContextMenuPolicy(Qt.PreventContextMenu)
        self.CreateHelpActions()

        self.tabMenu.AddAllToolBar(self.toolbarFile,self.toolbarSettings,self.toolbarCloud,self.toolbarHelp)

    def CreateFileActions(self):
        self.findAction = QAction(QIcon(':/icon/images/search.png'), 'Bul & Değiştir', self)
        # self.terminalAction = QAction(QIcon(':/icon/images/command.png'), 'Terminal Başlat', self)
        self.interpreterAction = QAction(QIcon(':/icon/images/pythonstart.png'), 'Python Yorumlayıcıyı Başlat', self)
        self.flowchartAction = QAction(QIcon(':/icon/images/startflow.png'), 'Akış şeması oluştur', self)
        self.zoomOutAction = QAction(QIcon(':/icon/images/zoom_out.png'), 'Uzaklaştır', self)
        self.zoomInAction = QAction(QIcon(':/icon/images/zoom_in.png'), 'Yakınlaştır', self)
        self.redoAction = QAction(QIcon(':/icon/images/redo_i.png'), 'İleri Al', self)
        self.undoAction = QAction(QIcon(':/icon/images/undo_i.png'), 'Geri Al', self)
        self.printAction = QAction(QIcon(':/icon/images/printicon.png'), 'Yazdır', self)
        self.saveAsAction = QAction(QIcon(':/icon/images/save_as.png'), 'Farklı Kaydet', self)
        self.saveAction = QAction(QIcon(':/icon/images/savefile.png'), 'Kaydet', self)
        self.openAction = QAction(QIcon(':/icon/images/openfile.png'), 'Aç', self)
        self.newAction = QAction(QIcon(':/icon/images/addfile.png'), 'Yeni', self)
        self.closeAction = QAction(QIcon(':/icon/images/addfile.png'), 'Kapat', self)
        self.historyAction = QAction(QIcon(':/icon/images/history.png'), 'Son Kullanılan Dosyalar', self)
        self.debugAction = QAction(QIcon(':/icon/images/debug-icon.png'), 'Debugger', self)

        self.newAction.setShortcut('Ctrl+N')
        self.newAction.triggered.connect(self.parent.new)

        self.closeAction.setShortcut('Ctrl+W')
        self.closeAction.triggered.connect(self.parent.close)

        self.openAction.setShortcut('Ctrl+O')
        self.openAction.triggered.connect(self.parent.openPythonFiles)

        self.saveAction.setShortcut('Ctrl+S')
        self.saveAction.triggered.connect(self.parent.save)

        self.saveAsAction.setShortcut('Ctrl+Shift+S')
        self.saveAsAction.triggered.connect(self.parent.saveAs)

        self.printAction.setShortcut('Ctrl+P')
        self.printAction.triggered.connect(self.parent.onPrint)

        self.undoAction.setShortcut('Ctrl+Z')
        self.undoAction.triggered.connect(self.parent.undo)

        self.redoAction.setShortcut('Ctrl+Shift+Z')
        self.redoAction.triggered.connect(self.parent.redo)

        self.zoomInAction.setShortcut('Ctrl++')
        self.zoomInAction.triggered.connect(self.parent.zoomIn)

        self.zoomOutAction.setShortcut('Ctrl+-')
        self.zoomOutAction.triggered.connect(self.parent.zoomOut)

        self.interpreterAction.setShortcut('F10')
        self.interpreterAction.triggered.connect(self.parent.interpreter)

        self.flowchartAction.triggered.connect(self.parent.flowchart)

        # self.debugAction.setShortcut('')
        self.debugAction.triggered.connect(self.parent.debugger)

        self.historyAction.setShortcut('Ctrl+H')
        self.historyAction.triggered.connect(self.parent.history)

        # self.terminalAction.setShortcut('F11')
        # self.terminalAction.triggered.connect(self.parent.terminal)

        self.findAction.setShortcut('Ctrl+F')
        self.findAction.triggered.connect(self.parent.onSearch)

        self.toolbarFile.addAction(self.newAction)
        self.addAction(self.closeAction)
        self.toolbarFile.addAction(self.openAction)
        self.toolbarFile.addAction(self.historyAction)
        self.toolbarFile.addAction(self.saveAction)
        self.toolbarFile.addAction(self.saveAsAction)
        self.toolbarFile.addAction(self.printAction)
        self.toolbarFile.addAction(self.undoAction)
        self.toolbarFile.addAction(self.redoAction)
        self.toolbarFile.addAction(self.zoomInAction)
        self.toolbarFile.addAction(self.zoomOutAction)
        self.toolbarFile.addAction(self.findAction)
        self.toolbarFile.addAction(self.interpreterAction)
        self.toolbarFile.addAction(self.flowchartAction)
        self.toolbarFile.addAction(self.debugAction)
        # self.toolbarFile.addAction(self.terminalAction)


    def CreateSettingsActions(self):
        self.settingsAction = QAction(QIcon(':/icon/images/settings_i.png'), 'Ayarlar', self)
        self.packageAction = QAction(QIcon(':/icon/images/package.png'), 'Paket Yöneticisi', self)

        self.settingsAction.setShortcut('F9')
        self.settingsAction.triggered.connect(self.parent.showSettings)

        self.packageAction.setShortcut('F8')
        self.packageAction.triggered.connect(self.parent.showPackage)

        self.toolbarSettings.addAction(self.settingsAction)
        self.toolbarSettings.addAction(self.packageAction)

    def CreateCloudActions(self):
        # Daha sonra eklenecek..
        self.sendCloud = QAction(QIcon(':/icon/images/sendCloud.png'), 'Buluta Gönder', self)
        self.installCloud = QAction(QIcon(':/icon/images/installCloud.png'), 'Buluttan İndir', self)
        self.sendTeacher = QAction(QIcon(':/icon/images/sendTeacher.png'), 'Öğretmene Gönder', self)
        self.pynarBox = QAction(QIcon(':/icon/images/pynarBox.png'), 'Pynar Kutu', self)

        self.sendCloud.triggered.connect(self.parent.sendCloud)
        self.installCloud.triggered.connect(self.parent.installCloud)
        self.sendTeacher.triggered.connect(self.parent.sendTeacher)
        self.pynarBox.triggered.connect(self.parent.pynarBox)

        self.toolbarCloud.addAction(self.sendCloud)
        self.toolbarCloud.addAction(self.installCloud)
        self.toolbarCloud.addAction(self.sendTeacher)
        self.toolbarCloud.addAction(self.pynarBox)

    def CreateHelpActions(self):
        self.licenseAction = QAction(QIcon(':/icon/images/license.png'), 'Pynar Hakkında', self)
        self.helpAction = QAction(QIcon(':/icon/images/help.png'), 'Yardım', self)

        self.licenseAction.setShortcut('F2')
        self.licenseAction.triggered.connect(self.parent.showLicense)

        self.helpAction.setShortcut('F1')
        self.helpAction.triggered.connect(self.parent.showHelp)

        self.toolbarHelp.addAction(self.licenseAction)
        self.toolbarHelp.addAction(self.helpAction)

    def changeToolbarButtonActive(self, activeState):
        self.saveAction.setEnabled(activeState)
        self.saveAsAction.setEnabled(activeState)
        self.printAction.setEnabled(activeState)
        self.undoAction.setEnabled(False)
        self.redoAction.setEnabled(False)
        self.zoomInAction.setEnabled(activeState)
        self.zoomOutAction.setEnabled(activeState)
        self.interpreterAction.setEnabled(activeState)
        self.flowchartAction.setEnabled(activeState)
        self.debugAction.setEnabled(activeState)
        # self.terminalAction.setEnabled(activeState)
        self.findAction.setEnabled(activeState)

