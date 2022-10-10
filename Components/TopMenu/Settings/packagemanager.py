import sys, stat
import os
from PyQt5 import Qt
from PyQt5.QtCore import QSize, QRect, pyqtSignal
from PyQt5.QtWidgets import (QApplication, QWidget, QDialog, QHBoxLayout,
                             QVBoxLayout, QGridLayout, QLabel, QLineEdit,
                             QPushButton, QMainWindow, QCheckBox, QDesktopWidget,
                             QGroupBox, QSpinBox, QTextEdit, QTabWidget,
                             QDialogButtonBox, QMessageBox, QListWidget,
                             QListWidgetItem, QComboBox, QFontDialog)
from PyQt5.QtGui import (QFont, QPalette, QIcon)
from PyQt5.Qt import Qt

from Components.MessageBox.CustomizeMessageBox import CustomizeMessageBox_Ok
from configuration import Configuration
from widgets import (MessageBox, Label, RadioButton, PushButton,
                     ListWidget, WhiteLabel, TabWidget, TextEdit)
from deadcodechecker import DeadCodeChecker
from pycodechecker import PyCodeChecker
from natsort import natsorted
import urllib
from urllib import parse
import requests
import subprocess,json
from threading import Thread
import re
import configparser
from dialog import Dialog

class PMDialog(Dialog):
    outSignal = pyqtSignal(str)
    okSignal = pyqtSignal(str, bool)
    _messagesSignal = pyqtSignal(int, str)
    _updateSignal = pyqtSignal()

    def __init__(self, parent=None, textPad=None):
        super().__init__(parent, textPad)
        self.c = Configuration()
        try:
            subprocess.check_output(["conda", "-V"], shell=self.c.getShell(), stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            CustomizeMessageBox_Ok("\nBilgisayarınızda Anaconda dağıtımından gelen bir python sürümü bulunmaktadır. Anaconda kendi paket yöneticisini kullanmaktadır. PyNar Paket Yöneticisi Anaconda dağıtımıyla uyumlu değildir, eğer PyNar paket yöneticisini kullanmak istiyorsanız Anaconda yazılımını bilgisayarınızdan kaldırınız.", "critical")
        except:
            self.parent = parent
            self.textPad = textPad
            self.setWindowTitle('Paket Yöneticisi')
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
            self.setWindowIcon(QIcon(':/icon/images/package.png'))
            self.setStyleSheet("background-color: #CAD7E0;")
            self.setMinimumSize(QSize(620, 393))
            self.setMaximumSize(QSize(620, 393))
            self.baseUrl = 'https://pypi.org/pypi/'
            self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0'}
            self.initUI()
            self.exec_()

    def initUI(self):
        font = QFont()
        font.setFamily(self.c.getEditorFont())
        font.setPointSize(self.c.getEditorFontSize())

        Package_manager = QWidget()
        Package_manager.setFont(font)
        Package_manager.setStyleSheet(" background-color: rgb(255, 255, 255);")

        self.Description_line = QTextEdit(Package_manager)
        self.Description_line.setReadOnly(True)
        self.Description_line.setGeometry(QRect(300, 70, 271, 231))
        self.Description_line.setFont(font)
        self.Description_line.setStyleSheet("background-color: rgb(255, 203, 201);")
        self.Description_line.setText("Paketler pypi.org siyesinden indirilmektedir. "
                                      "Aradığınız paket pypi.org sitesinde bulunduktan "
                                      "sonra paket bilgisi kısmında paketin bilgileri görüntülenir. "
                                      "Aradığınız pakete ait son sürümü yerine farklı bir sürümünü "
                                      "indirmek istiyorsanız sürüm numarası seç bölümünden paketinize "
                                      "ait tüm sürüm numaraları arasından seçiminizi yapabilirsiniz.")
        self.Description_line.setObjectName("settingsTextEdit")

        self.Search_line = QLineEdit(Package_manager)
        self.Search_line.setGeometry(QRect(10, 10, 390, 31))
        self.Search_line.setFont(font)
        self.Search_line.setPlaceholderText("Aradığınız paketin tam adını yazınız.")
        self.Search_line.setObjectName("settingsLine")

        self.Search_button = QPushButton(Package_manager)
        self.Search_button.setGeometry(QRect(410, 5, 170, 41))
        self.Search_button.setText("PyPI\'dan Paket Bul")
        self.Search_button.setFont(font)
        self.Search_button.setStyleSheet(
            "QPushButton { color: white;padding: 5px;margin: 4px 2px;border-radius: 4px; background-color: rgb(0, 170, 255);} " \
            "QPushButton::hover{background-color:rgb(4, 124, 184)}")
        self.Search_button.setObjectName("settingsMenu")

        self.Download_button = QPushButton(Package_manager)
        self.Download_button.setGeometry(QRect(440, 307, 141, 41))
        self.Download_button.setText("Kur")
        self.Download_button.setEnabled(False)
        self.Download_button.setFont(font)
        self.Download_button.setStyleSheet(
            "QPushButton { color: white;padding: 5px;margin: 4px 2px;border-radius: 4px; background-color: rgb(0, 170, 255);} " \
            "QPushButton::hover{background-color:rgb(4, 124, 184)}")
        self.Download_button.setObjectName("settingsMenu")

        self.Version_list = QComboBox(Package_manager)
        self.Version_list.setStyleSheet("QComboBox { border : 1px solid gray; selection-background-color: blue;}")
        self.Version_list.setGeometry(QRect(176, 316, 115, 22))
        self.Version_list.setFont(font)
        self.Version_list.setObjectName("settigsComboBox")

        self.Update_button = QPushButton(Package_manager)
        self.Update_button.setGeometry(QRect(299, 307, 141, 41))
        self.Update_button.setText("Güncelle")
        self.Update_button.setEnabled(False)
        self.Update_button.setFont(font)
        self.Update_button.setStyleSheet(
            "QPushButton { color: white;padding: 5px;margin: 4px 2px;border-radius: 4px; background-color: rgb(0, 170, 255);} " \
            "QPushButton::hover{background-color:rgb(4, 124, 184)}")
        self.Update_button.setObjectName("settingsMenu")

        self.List_line = QListWidget(Package_manager)
        self.List_line.setGeometry(QRect(10, 70, 281, 231))
        self.List_line.setFont(font)
        self.List_line.setObjectName("settingsList")

        Label_vers = QLabel(Package_manager)
        Label_vers.setGeometry(QRect(10, 315, 165, 20))
        Label_vers.setText("Sürüm Numarası Seç")
        Label_vers.setFont(font)
        Label_vers.setObjectName("settingsMenu")

        Label_desp = QLabel(Package_manager)
        Label_desp.setGeometry(QRect(300, 48, 261, 20))
        Label_desp.setText("Paket Bilgisi")
        Label_desp.setFont(font)
        Label_desp.setObjectName("settingsMenu")

        Label_list = QLabel(Package_manager)
        Label_list.setGeometry(QRect(10, 48, 261, 20))
        Label_list.setText("Paket Listesi")
        Label_list.setFont(font)
        Label_list.setObjectName("settingsMenu")

        self.Update_button.hide()

        self.dPackageDict = {}
        firstThread = Thread(target=self._setInstructıonPage, args=[True])
        firstThread.start()

        self.List_line.itemClicked.connect(lambda: self._listItemClicked())
        self.Search_line.returnPressed.connect(lambda: self._searchQuery(self.Search_line))
        self.Search_line.textChanged.connect(lambda: self._searcLineChange())
        self.Search_button.clicked.connect(lambda: self._searchQuery(self.Search_line))
        self.Download_button.clicked.connect(lambda: self._btnClicked())
        self.Version_list.currentIndexChanged.connect(lambda: self._btnVersion())
        self.Update_button.clicked.connect(lambda: self._updatePackage())
        self.outSignal.connect(self._setDescText)
        self.okSignal.connect(self._updateList)
        self._messagesSignal.connect(self._messages)
        self._updateSignal.connect(self._listItemClicked)

        self.btnIsUninstall = False
        self.dwnVersion = ""

        layout = QVBoxLayout()
        layout.addWidget(Package_manager)
        self.setLayout(layout)
        self.center()

    def _searcLineChange(self):
        if self.List_line.selectedIndexes() == None:
            self.Update_button.hide()

    def _btnVersion(self):
        if self.btnIsUninstall:
            if self.dwnVersion == self.Version_list.currentText():
                self.Update_button.setEnabled(False)
            else:
                self.Update_button.setEnabled(True)

    def _btnClicked(self):
        if self.btnIsUninstall:
            self._uninstallPackage()
        else:
            self._downloadPackage()

    def _btnChanged(self):
        self.Download_button.setEnabled(False)
        self.btnIsUninstall = False
        self.Download_button.setText("Kur")
        self.Update_button.hide()

    def _setInstructıonPage(self,first=False):
        c = Configuration()
        python_exe = c.getSelectedPythonExe()
        data = subprocess.check_output([python_exe, '-m', 'pip', "list", "--format", "json",  "--disable-pip-version-check"], shell = self.c.getShell())
        parsed_results = json.loads(data)
        dPackageDict = {}
        self.List_line.clear()
        for element in parsed_results:
            self.List_line.addItem(element['name'].lower())
            dPackageDict[element["name"].lower()] = element["version"]
        self.List_line.sortItems()
        dPackageDict['isInstalled'] = True
        if first:
            self.dPackageDict = dPackageDict
        else:
            return dPackageDict

    def _listItemClicked(self):
        self.Description_line.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.Update_button.show()
        try:
            packageName = self.List_line.currentItem().text()
            jsonDataUrl = self.baseUrl + urllib.parse.quote(
                packageName) + "/json"
            packageURL = "https://pypi.org/project/" + packageName + "/"
            self.dPackageDict['Json page'] = jsonDataUrl
            self.dPackageDict['PyPI page'] = packageURL
            self.dPackageDict['isInstalled'] = True
            self._fetchPackageData()
        except Exception as e:
            print(e)
            pass

    def _fetchPackageData(self):
        try:
            req = requests.get(self.dPackageDict['Json page'], headers=self.headers)
            jsonData = req.json()
            self.Version_list.clear()
            for i in natsorted(list(jsonData['releases'].keys()))[::-1]:
                self.Version_list.addItem(i)
        except Exception as e:
            print(e)
            self._packageNotFound()
            return False
        else:
            self.dPackageDict['Author'] = jsonData['info']['author']
            self.dPackageDict['name'] = jsonData['info']['name']
            self.dPackageDict['version'] = jsonData['info']['version']
            self.dPackageDict['details'] = jsonData['info']['summary']
            self.dPackageDict['Homepage'] = jsonData['info']['home_page']
            self.dPackageDict['Requirements'] = jsonData['info']['requires_dist']
            for data in self.dPackageDict:
                if self.dPackageDict[data] == None:
                    self.dPackageDict[data] = ""
            self._writeData(self.dPackageDict['isInstalled'])
            return True

    def _writeData(self, isInstalled):
        if isInstalled == True:
            pName = self.dPackageDict['name']
            try:
                tempList = pName.split("_")
            except Exception as e:
                print(e)
            else:
                pName = "-".join(tempList)
                self.Description_line.setText(f"{str(self.dPackageDict['name']).upper()}")
                self.Description_line.append("\n")
                self.Description_line.append(f"İndirilen versiyon : {self.dPackageDict[pName.lower()]}")
                self.Description_line.append("\n")
                self.Description_line.append(f"Güncel versiyon : {self.dPackageDict['version']} ")
                self.Description_line.append(f"Açıklama :{self.dPackageDict['details']} ")
                self.Description_line.append(f"Anasayfa : {self.dPackageDict['Homepage']}  ")
                self.Description_line.append(f"PyPI sayfası :{self.dPackageDict['PyPI page']} ")
                self.Description_line.append(f"Yazar : {self.dPackageDict['Author']} ")
                self.Description_line.append(f"Gerekli olanlar : {str(self.dPackageDict['Requirements'])}")
                try:
                    cursor = self.Description_line.textCursor()
                    cursor.movePosition(0)
                    self.Description_line.setTextCursor(cursor)
                except Exception as e:
                    print(e)
                    pass
                self.dwnVersion = self.dPackageDict[pName.lower()]
                self.btnIsUninstall = True
                self.Version_list.setCurrentIndex(self.Version_list.findText(self.dPackageDict[pName.lower()]))
                self._btnVersion()
                self.Download_button.setEnabled(True)
                self.Download_button.setText("Kaldır")
                self.Description_line.setStyleSheet("background-color: rgb(255, 255, 255);")
        else:
            self.Description_line.setText(f"{str(self.dPackageDict['name']).upper()}")
            self.Description_line.append("\n")
            self.Description_line.append(f"Güncel versiyon : {self.dPackageDict['version']} ")
            self.Description_line.append(f"Açıklama :{self.dPackageDict['details']} ")
            self.Description_line.append(f"Anasayfa : {self.dPackageDict['Homepage']}  ")
            self.Description_line.append(f"PyPI sayfası :{self.dPackageDict['PyPI page']} ")
            self.Description_line.append(f"Yazar : {self.dPackageDict['Author']} ")
            self.Description_line.append(f"Gerekli olanlar : {str(self.dPackageDict['Requirements'])}")
            try:
                cursor = self.Description_line.textCursor()
                cursor.movePosition(0)
                self.Description_line.setTextCursor(cursor)
            except Exception as e:
                print(e)
                pass
            self.btnIsUninstall = False
            self.Download_button.setEnabled(True)
            self.Update_button.setEnabled(False)
            self.Download_button.setText("Kur")
            self.Description_line.setStyleSheet("background-color: rgb(255, 255, 255);")
        return

    def _searchQuery(self, query):
        self.Update_button.hide()
        if query.text().strip() == "":
            return
        packageName = query.text().strip().lower()
        findList = self.List_line.findItems(packageName, Qt.MatchExactly)

        packageURL = "https://pypi.org/project/" + packageName + "/"
        jsonDataUrl = self.baseUrl + urllib.parse.quote(packageName) + "/json"
        self.dPackageDict['PyPI page'] = packageURL
        self.dPackageDict['Json page'] = jsonDataUrl

        if findList:
            self.dPackageDict['isInstalled'] = True
        else:
            self.dPackageDict['isInstalled'] = False

        isFind = self._fetchPackageData()
        if isFind:
            if findList:
                self.Update_button.show()
                self.List_line.setCurrentItem(findList[0])
            else:
                self.List_line.setCurrentRow(-1)
                self.Version_list.setCurrentIndex(0)
        else:
            pass

    def _downloadPackage(self):
        self.block()
        self.List_line.setCurrentRow(0)
        self.Description_line.clear()
        runs = Thread(target=self.download_command)
        runs.start()

    def download_command(self, update=False):
        text = (self.Search_line.text() if not update else self.List_line.currentItem().text())
        version = "==" + self.Version_list.currentText()
        c = Configuration()
        python_exe = c.getSelectedPythonExe()
        process = subprocess.Popen([python_exe, '-m', 'pip', 'install', text + version,  "--disable-pip-version-check"], stdout=subprocess.PIPE, shell = self.c.getShell())
        while True:
            output = process.stdout.readline()
            if output:
                self.outSignal[str].emit(output.strip().decode() + "\n")
            rc = process.poll()
            if rc == 1:
                if not update:
                    self._messagesSignal[int, str].emit(1, "Kurulum yapılırken bir hata oluştu.")
                else:
                    self._messagesSignal[int, str].emit(1, "Güncelleme yapılırken bir hata oluştu.")
                return rc
            elif rc == 0:
                self.okSignal[str, bool].emit(text, True)
                self._updateSignal.emit()
                if not update:
                    self._messagesSignal[int, str].emit(0, "Kurulum Başarı ile Tamamlandı.")
                else:
                    self._messagesSignal[int, str].emit(0, "Güncelleme Başarı ile Tamamlandı.")
                return rc
            elif rc != None:
                print(rc)
                return

    def _setDescText(self, text):
        self.Description_line.insertPlainText(text)
        try:
            cursor = self.Description_line.textCursor()
            cursor.movePosition(len(self.Description_line.toPlainText()) - 1)
            self.Description_line.setTextCursor(cursor)
        except Exception as e:
            print(e)
            pass

    def _updateList(self, text, isDwn):
        self.prev_dPackageDict = self.dPackageDict
        self.dPackageDict = self._setInstructıonPage()
        if isDwn:
            try:
                self.List_line.setCurrentItem(self.List_line.findItems(text, Qt.MatchExactly)[0])
            except Exception as e:
                text = list(self.dPackageDict.keys() - self.prev_dPackageDict.keys())[0]
                self.List_line.setCurrentItem(self.List_line.findItems(text, Qt.MatchExactly)[0])
                print(e)
                pass

    def _uninstallPackage(self):
        self.block()

        self.Description_line.clear()
        runs = Thread(target=self.uninstall_command)
        runs.start()

    def uninstall_command(self):
        c = Configuration()
        python_exe = c.getSelectedPythonExe()
        process = subprocess.Popen(
            [python_exe, '-m', 'pip', 'uninstall', '-y', self.List_line.currentItem().text(), "--disable-pip-version-check"],
            stdout=subprocess.PIPE, shell = self.c.getShell())
        while True:
            output = process.stdout.readline()

            if output:
                self.outSignal[str].emit(output.strip().decode() + "\n")
            rc = process.poll()
            if rc == 1:
                self._messagesSignal[int, str].emit(1, "Kaldırma işlemi gerçekleştirilirken bir hata oluştu.")
                break
            elif rc == 0:
                self.okSignal[str, bool].emit("", False)
                self.Version_list.clear()
                self._messagesSignal[int, str].emit(0, "Paket Başarılı Bir Şekilde Kaldırıldı.")
                break
            elif rc != None:
                print(rc)
                break
        self._btnChanged()

    def _updatePackage(self):
        self.block()

        self.Description_line.clear()
        runs = Thread(target=self.download_command, args=[True])
        runs.start()

    def block(self):
        self.Search_button.setEnabled(False)
        self.Search_line.setEnabled(False)
        self.List_line.setEnabled(False)
        self.Download_button.setEnabled(False)
        self.Update_button.setEnabled(False)

    def noneBlock(self):
        self.Search_button.setEnabled(True)
        self.Search_line.setEnabled(True)
        self.List_line.setEnabled(True)

    def _messages(self, err, text):
        ms_Btn = "information"
        if err == 1:
            ms_Btn = "critical"
        CustomizeMessageBox_Ok(text, ms_Btn)
        self.noneBlock()
        return
    def _packageNotFound(self):
        CustomizeMessageBox_Ok('Paket Bulunamadı!', "critical")
        self.noneBlock()
        return

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)

    def close(self):
        self.done(1)
