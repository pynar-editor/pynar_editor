from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtCore import QSize
from PyQt5.Qt import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QPushButton, QLabel, QVBoxLayout, QWidget, QDialog, QLineEdit, QMessageBox, QDesktopWidget, QListWidget, QHBoxLayout, QFileDialog
from PyQt5.uic.properties import QtGui
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QSize, QRect
import sys, os
import icons_rc
import requests
import uuid
import json
import urllib
import locale
import platform

from PyQt5 import QtCore, QtGui

parentdir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
# sys.path.append(parentdir) # Bu satır Nuitka'da problem çıkarıyor, silinmesi bir sorun oluşturmadı.
from configuration import Configuration

class fileUploadWindow(QDialog):
    def __init__(self,textpad=None,token=None, log=None, cloud=False):
        super(fileUploadWindow, self).__init__()

        self.returnValue = 0
        self.fileName = ""

        self.textpad = textpad
        self.token = token
        self.log = log

        self.setWindowTitle('Bulut Yöneticisi')
        self.setWindowIcon(QIcon(':/icon/images/headerLogo1.png'))
        self.setStyleSheet("background-color: #CAD7E0;")
        self.setMinimumSize(QSize(360, 160))
        self.setMaximumSize(QSize(360, 160))

        self.c = Configuration()

        font = QFont()
        font.setFamily(self.c.getEditorFont())
        font.setPointSize(self.c.getEditorFontSize())

        groupBox = QWidget()
        groupBox.setFont(font)
        groupBox.setStyleSheet(" background-color: rgb(255, 255, 255);")
        groupBox.setObjectName("settingsTab")

        self.name = QLabel(groupBox)
        self.name.move(30, 30)
        self.name.resize(170, 25)
        self.name.setText("Dosya İsmi: ")
        self.name.setFont(font)

        self.inputName = QLineEdit(groupBox)
        self.inputName.move(125, 30)
        self.inputName.resize(170, 25)
        self.inputName.setFont(font)

        self.button = QPushButton(groupBox)
        self.button.move(120, 70)
        self.button.resize(100, 40)
        self.button.setText("Tamam")
        if cloud:
            self.button.clicked.connect(self.uploadCloud)
        else:
            self.button.clicked.connect(self.uploadTeacher)
        self.button.setFont(font)
        self.button.setStyleSheet("QPushButton { color: white;padding: 5px;margin: 4px 2px;border-radius: 4px; background-color: rgb(0, 170, 255);} " \
                      "QPushButton::hover{background-color:rgb(4, 124, 184)}")

        layout = QVBoxLayout()
        layout.addWidget(groupBox)
        self.setLayout(layout)

        self.center()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)

    def message(self,title,text,inf=False):
        mesajKutusu = QMessageBox()
        mesajKutusu.setWindowIcon(QtGui.QIcon(":/icon/images/headerLogo1.png"))
        mesajKutusu.setWindowTitle(title)
        mesajKutusu.setText(text)
        if inf:
            mesajKutusu.setIcon(QMessageBox.Information)
        else:
            mesajKutusu.setIcon(QMessageBox.Warning)
        mesajKutusu.setStandardButtons(QMessageBox.Ok)
        mesajKutusu.exec()

    def uploadTeacher(self):
        if self.textpad.filename == None:
            message = "Dosyanız {} olarak Belgelerim\PynarKutu klasörüne kaydedildi ve öğretmene gönderildi."

            filename = self.inputName.text()
            filename = filename.split(".")

            if len(filename) == 0:
                self.message("Hata!", "Lütfen bir dosya adı giriniz.")
                return
            elif len(filename) == 1:
                filename.append(".py")
            else:
                if filename[1] != ".py":
                    filename[1] = ".py"

            filename = filename[0] + filename[1]

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


            if os.path.exists(self.directoryPath + filename):
                self.message("Hata !!","Belgelerim\PynarKutu klasörü altında " + "'" + filename + "'" + "Adında bir dosya zaten bulunuyor. Lüften isim değişikliği yapıp tekrar kaydetmeyi deneyiniz.")
                return 1

            with open(self.directoryPath + filename,"w",encoding='utf8') as f:
                f.write(self.textpad.text())

            self.textpad.filename = self.directoryPath + filename
            self.returnValue = 1

        else:
            message = "{} adlı dosya öğretmene gönderildi."
            text = self.textpad.text()
            try:
                with open(self.textpad.filename, 'w', newline='', encoding='utf8') as file:
                    file.write(text)

            except Exception as e:
                self.message("Hata !", str(e))

        info_url = 'http://pynar.org/api/user/institution/student/info'
        headers = {'Authorization': 'Bearer ' + self.token}
        x = requests.post(info_url, headers=headers)
        res_json = x.json()
        if (res_json['ok'] != True):
            self.message("Hata!", res_json['description'])
            return -1
        else:
            data = res_json['result'].get('data')
            if data.get('institution_id') == None or data.get('teacher_id') == None:
                self.message("Hata!", 'Lütfen portal üzerinden okul ve öğretmen adı seçiniz.')
                self.done(1)
                return -1

        server_update_url = 'http://pynar.org/api/user/student/assignments'

        with open(self.textpad.filename, "rb") as a_file:
            file_dict = {
                'file': (self.textpad.filename, a_file, 'text/x-python'),
            }

            headers = {'Authorization': 'Bearer ' + self.token}
            myobj = {'mac_address': hex(uuid.getnode()), 'teacher_id': data.get('teacher_id')}
            x = requests.post(server_update_url, files=file_dict, headers=headers, data=myobj, verify=False)
            res_json = x.json()
            if (res_json['ok'] == True):
                self.message("Başarılı!", message.format(self.textpad.filename.split("/")[-1]), True)
            else:
                self.message("Hata!", res_json['description'])
                self.returnValue = 2
                return -1
        self.done(1)

    def uploadCloud(self):
        if self.textpad.filename == None:
            message = "Dosyanız {} olarak Belgelerim\PynarKutu klasörüne kaydedildi ve Buluta yüklendi"

            filename = self.inputName.text()
            filename = filename.split(".")

            if len(filename) == 0:
                self.message("Hata!", "Lütfen bir dosya adı giriniz.")
                return
            elif len(filename) == 1:
                filename.append(".py")
            else:
                if filename[1] != ".py":
                    filename[1] = ".py"

            filename = filename[0] + filename[1]

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


            if os.path.exists(self.directoryPath + filename):
                self.message("Hata !!","Belgelerim\PynarKutu klasörü altında " + "'" + filename + "'" + "Adında bir dosya zaten bulunuyor. Lüften isim değişikliği yapıp tekrar kaydetmeyi deneyiniz.")
                return 1

            with open(self.directoryPath + filename,"w",encoding='utf8') as f:
                f.write(self.textpad.text())

            self.textpad.filename = self.directoryPath + filename
            self.returnValue = 1

        else:
            message = "{} adlı dosya Buluta yüklendi"
            text = self.textpad.text()
            try:
                with open(self.textpad.filename, 'w', newline='', encoding='utf8') as file:
                    file.write(text)

            except Exception as e:
                self.message("Hata !", str(e))

        server_update_url = 'http://pynar.org/api/user/file/upload'

        with open(self.textpad.filename, "rb") as a_file:
            if os.path.exists(self.log):
                file_dict = {
                    'file': (self.textpad.filename, a_file, 'text/x-python'),
                    'logs': open(os.path.join('Log', self.log), 'rb'),
                }
            else:
                file_dict = {
                    'file': (self.textpad.filename, a_file, 'text/x-python'),
                }

            headers = {'Authorization': 'Bearer ' + self.token}
            myobj = {'mac_address': hex(uuid.getnode())}
            x = requests.post(server_update_url, files=file_dict, headers=headers, data=myobj, verify=False)
            res_json = x.json()
            if (res_json['ok'] == True):
                self.message("Başarılı!", message.format(self.textpad.filename.split("/")[-1]), True)
            else:
                self.message("Hata!", res_json['description'])
                self.returnValue = 2
                return -1

        self.done(1)

class FilesWindow(QDialog):
    def __init__(self, name, files=None, token=None):
        super(FilesWindow, self).__init__()

        self.name = name
        self.directoryPath = None
        self.authToken = token
        self.fullpath = None

        self.setWindowTitle('Bulut Yöneticisi')
        self.setWindowIcon(QIcon(':/icon/images/headerLogo1.png'))
        self.setStyleSheet("background-color: #CAD7E0;")
        self.setMinimumSize(QSize(460, 250))
        self.setMaximumSize(QSize(460, 250))

        self.c = Configuration()

        font = QFont()
        font.setFamily(self.c.getEditorFont())
        font.setPointSize(self.c.getEditorFontSize())

        groupBox = QWidget()
        groupBox.setFont(font)
        groupBox.setStyleSheet(" background-color: rgb(255, 255, 255);")
        groupBox.setObjectName("settingsTab")

        self.list = QListWidget(groupBox)
        self.list.move(10,10)
        self.list.resize(300,200)
        self.list.setFont(font)

        if files is not None:
            self.list.addItems(files)
            self.list.setCurrentRow(0)

        buttonOpen = QPushButton(groupBox)
        buttonOpen.move(320, 30)
        buttonOpen.resize(100, 40)
        buttonOpen.setText("Dosyayı Aç")
        buttonOpen.setFont(font)
        buttonOpen.setStyleSheet("QPushButton { color: white;padding: 5px;margin: 4px 2px;border-radius: 4px; background-color: rgb(0, 170, 255);} " \
                      "QPushButton::hover{background-color:rgb(4, 124, 184)}")
        buttonOpen.clicked.connect(self.open)

        buttonDel = QPushButton(groupBox)
        buttonDel.move(320, 90)
        buttonDel.resize(100, 40)
        buttonDel.setText("Dosyayı Sil")
        buttonDel.setFont(font)
        buttonDel.setStyleSheet("QPushButton { color: white;padding: 5px;margin: 4px 2px;border-radius: 4px; background-color: rgb(0, 170, 255);} " \
                      "QPushButton::hover{background-color:rgb(4, 124, 184)}")
        buttonDel.clicked.connect(self.delete)

        buttonClose = QPushButton(groupBox)
        buttonClose.move(320, 150)
        buttonClose.resize(100, 40)
        buttonClose.setText("Çıkış")
        buttonClose.setFont(font)
        buttonClose.setStyleSheet("QPushButton { color: white;padding: 5px;margin: 4px 2px;border-radius: 4px; background-color: rgb(0, 170, 255);} " \
                      "QPushButton::hover{background-color:rgb(4, 124, 184)}")
        buttonClose.clicked.connect(self.close)


        hbox = QHBoxLayout()
        hbox.addWidget(groupBox)

        self.setLayout(hbox)

        self.setWindowIcon(QtGui.QIcon(":/icon/images/headerLogo1.png"))


    def delete(self):
        dialog_result = self.dialog_Question("Dosyayı silmek istediğinize emin misiniz ?.")
        if dialog_result == QMessageBox.No:
            return 0
        row = self.list.currentRow()
        filename = self.list.item(row).text()
        headers = {'Authorization': 'Bearer ' + self.authToken}
        myobj = {'mac_address': hex(uuid.getnode())}
        url = "http://pynar.org/api/user/file/remove/" + urllib.parse.quote_plus(filename)
        res = requests.post(url, headers=headers, data=myobj)
        res_json = res.json()
        if res_json['ok'] == True:
            listItems = self.list.selectedItems()
            if listItems:
                for item in listItems:
                    self.list.takeItem(self.list.row(item))
            self.message("Başarılı!", res_json['result'].get('message'), True)
            if (self.list.count() < 1):
                self.accept()
        else:
            self.message("Hata!", res_json['description'], True)

    def open(self):
        try:
            row = self.list.currentRow()
            filename = self.list.item(row).text()
            headers = {'Authorization': 'Bearer ' + self.authToken}
            myobj = {'mac_address': hex(uuid.getnode())}
            url = "http://pynar.org/api/user/file/download/" + urllib.parse.quote_plus(filename)
            res = requests.post(url, data=myobj, headers=headers)

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

            if os.path.exists(self.directoryPath + filename):
                if self.dialog_Question("Pynarkutunuzda {} adlı bir dosya zaten var. Buluttan indirebilmeniz için PynarKutunuzdaki dosyayı silmeniz veya farklı adlandırmanız gerekir.  Devam ederseniz PynarKutunuzdaki dosya silinecek ve buluttan indirilen dosya PynarKutunuza kaydedilecektir. Devam etmek istiyormusunuz?".format(filename)) == QMessageBox.Yes:
                    try:
                        open(self.directoryPath + filename, 'wb').write(res.content)
                        self.message("İndirme Başarılı",
                                     "Buluttan indirilen {} dosyası Pynarkutunuza kaydedildi".format(filename), True)
                        self.fullpath = self.directoryPath + filename
                        self.close()
                        return 1
                    except:
                        self.message("Hata", "İşlem başarısız oldu lütfen daha sonra  tekrar deneyiniz.")
                        return -1
                else:
                    self.message("Dikkat","İndirme iptal edildi.".format(filename))
                    return -1
            try:
                open(self.directoryPath + filename, 'wb').write(res.content)
                self.message("İndirme Başarılı","Buluttan indirilen {} dosyası Pynarkutunuza kaydedildi".format(filename), True)
                self.fullpath = self.directoryPath + filename
                self.close()
            except:
                self.message("Hata", "İşlem başarısız oldu lütfen daha sonra  tekrar deneyiniz.")
                return -1
            return 1

        except Exception as e:
            self.message("Hata", "İşlem başarısız oldu lütfen daha sonra  tekrar deneyiniz.")
            return -1

    def close(self):
        self.accept()

    def message(self,title,text,inf=False):
        mesajKutusu = QMessageBox()
        mesajKutusu.setWindowIcon(QtGui.QIcon(":/icon/images/headerLogo1.png"))
        mesajKutusu.setWindowTitle(title)
        mesajKutusu.setText(text)
        if inf:
            mesajKutusu.setIcon(QMessageBox.Information)
        else:
            mesajKutusu.setIcon(QMessageBox.Warning)
        mesajKutusu.setStandardButtons(QMessageBox.Ok)
        mesajKutusu.exec()

    def dialog_Question(self, text):
        mesajKutusu = QMessageBox()
        mesajKutusu.setWindowIcon(QtGui.QIcon(":/icon/images/headerLogo1.png"))
        mesajKutusu.setWindowTitle("Dikkat !!!")
        mesajKutusu.setText(text)
        mesajKutusu.setIcon(QMessageBox.Warning)
        mesajKutusu.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        mesajKutusu.setDefaultButton(QMessageBox.Yes)
        return mesajKutusu.exec()

class Login(QDialog):
    def __init__(self):
        super(Login, self).__init__()

        self.c = Configuration()
        self.setWindowTitle('Giriş Yap')
        self.setWindowIcon(QIcon(':/icon/images/headerLogo1.png'))
        self.setStyleSheet("background-color: #CAD7E0;")
        self.setMinimumSize(QSize(330, 200))
        self.setMaximumSize(QSize(330, 200))
        self.setUI()

    def setUI(self):
        font = QFont()
        font.setFamily(self.c.getEditorFont())
        font.setPointSize(self.c.getEditorFontSize())

        groupBox = QWidget()
        groupBox.setFont(font)
        groupBox.setStyleSheet(" background-color: rgb(255, 255, 255);")
        groupBox.setObjectName("settingsTab")

        self.email = QLabel(groupBox)
        self.email.move(30, 30)
        self.email.setText("E-mail: ")
        self.email.setFont(font)

        self.input_email = QLineEdit(groupBox)
        self.input_email.move(95, 30)
        self.input_email.resize(170, 25)
        self.input_email.setFont(font)

        self.sifre = QLabel(groupBox)
        self.sifre.move(30, 60)
        self.sifre.setText("Şifre: ")
        self.sifre.setFont(font)

        self.input_sifre = QLineEdit(groupBox)
        self.input_sifre.move(95, 60)
        self.input_sifre.resize(170, 25)
        self.input_sifre.setEchoMode(QLineEdit.Password)
        self.input_sifre.setFont(font)

        self.button = QPushButton(groupBox)
        self.button.move(90, 100)
        self.button.resize(100, 40)
        self.button.setText("Giriş Yap")
        self.button.clicked.connect(self.login)
        self.button.setFont(font)
        self.button.setStyleSheet("QPushButton { color: white;padding: 5px;margin: 4px 2px;border-radius: 4px; background-color: rgb(0, 170, 255);} " \
                      "QPushButton::hover{background-color:rgb(4, 124, 184)}")
        layout = QVBoxLayout()
        layout.addWidget(groupBox)
        self.setLayout(layout)

        self.center()

    def storeToken(self, token):
        basename = self.c.checkPath(os.path.dirname(parentdir))
        filename = basename + '/Config/token'
        newTokenLine = "token: {0}\n".format(token)
        if os.path.exists(filename):
            with open(filename, "r+") as f:
                d = f.readlines()
                f.seek(0)
                for i in d:
                    if i.split(':')[0] != "token":
                        f.write(i)
                    else:
                        f.write(newTokenLine)
                f.truncate()
        else:
            with open(filename, "w+") as f:
                f.write(newTokenLine)

    def login(self):
        try:
            log_email = str(self.input_email.text())
            log_sifre = str(self.input_sifre.text())
            login_url = 'http://pynar.org/api/user/login'
            if (len(log_email and log_sifre) != 0):
                myobj = {}
                myobj['email'] = log_email
                myobj['password'] = log_sifre
                myobj['mac_address'] = hex(uuid.getnode())
                myobj['network_name'] = platform.node()
                myobj['os_name'] = platform.system()
                myobj['os_version'] = platform.version()
                myobj['group'] = 'student'
                x = requests.post(login_url, data=myobj)
                res_json = x.json()
                if res_json['ok'] == True:

                    result = res_json['result']

                    self.token = result.get('token')
                    self.kullanici = result.get('user_fullname')

                    self.storeToken(result.get('token'))

                    self.accept()
                else:
                    self.message("Hata!", res_json['description'])

        except Exception as e:
            self.message("Hata!",str(e))

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)

    def message(self,title,text,inf=False):
        mesajKutusu = QMessageBox()
        mesajKutusu.setWindowIcon(QtGui.QIcon(":/icon/images/headerLogo1.png"))
        mesajKutusu.setWindowTitle(title)
        mesajKutusu.setText(text)
        if inf:
            mesajKutusu.setIcon(QMessageBox.Information)
        else:
            mesajKutusu.setIcon(QMessageBox.Warning)
        mesajKutusu.setStandardButtons(QMessageBox.Ok)
        mesajKutusu.exec()
class Register(QDialog):
    def __init__(self):
        super(Register, self).__init__()
        self.c = Configuration()
        self.setWindowTitle("Kayıt Ol")
        self.setWindowIcon(QIcon(':/icon/images/headerLogo1.png'))
        self.setStyleSheet("background-color: #CAD7E0;")
        self.setMinimumSize(QSize(330, 290))
        self.setMaximumSize(QSize(330, 290))
        self.setUI()

    def setUI(self):
        font = QFont()
        font.setFamily(self.c.getEditorFont())
        font.setPointSize(self.c.getEditorFontSize())

        groupBox = QWidget()
        groupBox.setFont(font)
        groupBox.setStyleSheet(" background-color: rgb(255, 255, 255);")
        groupBox.setObjectName("settingsTab")

        self.ad = QLabel(groupBox)
        self.ad.move(30, 30)
        self.ad.setText("Ad: ")
        self.ad.setFont(font)


        self.input_ad = QLineEdit(groupBox)
        self.input_ad.move(100, 30)
        self.input_ad.resize(170, 25)
        self.input_ad.setFont(font)
        self.input_ad.setPlaceholderText("Adı")

        self.soyad = QLabel(groupBox)
        self.soyad.move(30, 60)
        self.soyad.setText("Soyad: ")
        self.soyad.setFont(font)

        self.input_soyad = QLineEdit(groupBox)
        self.input_soyad.move(100, 60)
        self.input_soyad.resize(170, 25)
        self.input_soyad.setFont(font)
        self.input_soyad.setPlaceholderText("Soyadı")

        self.email = QLabel(groupBox)
        self.email.move(30, 90)
        self.email.setText("E-mail: ")
        self.email.setFont(font)

        self.input_email = QLineEdit(groupBox)
        self.input_email.move(100, 90)
        self.input_email.resize(170, 25)
        self.input_email.setFont(font)
        self.input_email.setPlaceholderText("E-mail")

        self.sifre = QLabel(groupBox)
        self.sifre.move(30, 120)
        self.sifre.setText("Şifre: ")
        self.sifre.setFont(font)

        self.input_sifre = QLineEdit(groupBox)
        self.input_sifre.move(100, 120)
        self.input_sifre.resize(170, 25)
        self.input_sifre.setEchoMode(QLineEdit.Password)
        self.input_sifre.setFont(font)
        self.input_sifre.setPlaceholderText("Şifre")

        self.sifre_r = QLabel(groupBox)
        self.sifre_r.move(30, 150)
        self.sifre_r.setText("Şifre: ")
        self.sifre_r.setFont(font)

        self.input_sifre_r = QLineEdit(groupBox)
        self.input_sifre_r.move(100, 150)
        self.input_sifre_r.resize(170, 25)
        self.input_sifre_r.setEchoMode(QLineEdit.Password)
        self.input_sifre_r.setFont(font)
        self.input_sifre_r.setPlaceholderText("Şifre Tekrar")

        self.button = QPushButton(groupBox)
        self.button.move(90, 200)
        self.button.resize(100, 40)
        self.button.setText("Kayıt Ol")
        self.button.clicked.connect(self.register)
        self.button.setFont(font)
        self.button.setStyleSheet(
            "QPushButton { color: white;padding: 5px;margin: 4px 2px;border-radius: 4px; background-color: rgb(0, 170, 255);} " \
            "QPushButton::hover{background-color:rgb(4, 124, 184)}")

        layout = QVBoxLayout()
        layout.addWidget(groupBox)
        self.setLayout(layout)

        self.center()

    def register(self):
        try:
            reg_ad = str(self.input_ad.text())
            reg_soyad = str(self.input_soyad.text())
            reg_email = str(self.input_email.text())
            reg_sifre = str(self.input_sifre.text())
            reg_sifre_r = str(self.input_sifre_r.text())
            register_url = 'http://pynar.org/api/user/signup'
            if (len(reg_ad and reg_soyad and reg_email and reg_sifre and reg_sifre_r) != 0):
                if (reg_sifre != reg_sifre_r):
                    raise Exception("Şifreler birbirinin aynısı değil.")

                myobj = {}
                myobj['group'] = 'student'
                myobj['user_fullname'] = reg_ad + " " + reg_soyad
                myobj['email'] = reg_email
                myobj['password'] = reg_sifre

                res = requests.post(register_url, data=myobj)
                res_json = res.json()
                if res_json['ok'] == True:
                    self.message("Tebrikler!", res_json['result'].get('message'), True)
                    self.accept()
                else:
                    self.message("Hata!", res_json['description'], True)

            else:
                self.message("Hata!", "Metin kutuları boş geçilemez", True)

        except Exception as e:
            self.message("Hata!",str(e),True)


    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)

    def message(self,title,text,inf=False):
        mesajKutusu = QMessageBox()
        mesajKutusu.setWindowIcon(QtGui.QIcon(":/icon/images/headerLogo1.png"))
        mesajKutusu.setWindowTitle(title)
        mesajKutusu.setText(text)
        if inf:
            mesajKutusu.setIcon(QMessageBox.Information)
        else:
            mesajKutusu.setIcon(QMessageBox.Warning)
        mesajKutusu.setStandardButtons(QMessageBox.Ok)
        mesajKutusu.exec()

class UserLabel(QLabel):
    clicked = pyqtSignal()

    def mouseReleaseEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton:
            self.clicked.emit()

class LoginWindow(QDialog):
    def __init__(self, parent=None, parentImage=None):
        self.parent = parent
        super().__init__()

        self.userColor = {
    "A": "#f44336",
    "B": "#E91E63",
    "C": "#9C27B0",
    "Ç": "#673AB7",
    "D": "#3F51B5",
    "E": "#2196F3",
    "F": "#03A9F4",
    "G": "#00BCD4",
    "H": "#009688",
    "I": "#4CAF50",
    "İ": "#8BC34A",
    "J": "#CDDC39",
    "K": "#FFEB3B",
    "L": "#FFC107",
    "M": "#FF9800",
    "N": "#FF5722",
    "O": "#795548",
    "Ö": "#9E9E9E",
    "P": "#37474F",
    "R": "#f44380",
    "S": "#E91EFF",
    "Ş": "#9C2760",
    "T": "#219613",
    "U": "#7955F1",
    "Ü": "#FF57F2",
    "V": "#FFEB43",
    "Y": "#CDDC16",
    "Z": "#10a167"
}


        self.parentImage = parentImage
        self.c = Configuration()
        
        self.returnValue = False
        self.loginOk = False
        self.btn_signIn = QPushButton("Oturum Aç")
        self.btn_register = QPushButton("Kayıt Ol")
        self.lbl_img_user = QLabel()
        self.lbl_user_name_surname = QLabel(self.lbl_img_user)

        self.lbl_user_account = QLabel("Oturum açılmadı")
        self.retranslateUi(LoginWindow)
        self.setupUi(self)

        # geo = self.geometry()
        # geo.moveTopRight(self.parent.geometry().topRight() + QtCore.QPoint(0, 80))
        # self.setGeometry(geo)

        self.btn_signIn.clicked.connect(self.UserSignInClick)
        self.btn_register.clicked.connect(self.UserRegisterClick)

    def UserSignInClick(self):
        if self.loginOk:
            self.lbl_user_account.setText("Oturum açılmadı")
            self.lbl_user_account.adjustSize()
            self.lbl_user_name_surname.setText("")
            self.lbl_img_user.setPixmap(QPixmap(':/icon/images/user1.png'))
            self.lbl_img_user.setStyleSheet(
                "background-color:transparent; font-size: 14px; color:#a6a6a6;font-weight: bold;")

            self.parentImage.setPixmap(QPixmap(':/icon/images/user1.png'))
            self.parentImage.setStyleSheet(
                "background-color:transparent; font-size: 14px; color:#a6a6a6;font-weight: bold;")

            self.btn_signIn.setText("Oturum Aç")
            self.loginOk = False
            self.btn_register.show()

            basename = self.c.checkPath(os.path.dirname(parentdir))
            filename = basename + '/Config/token'
            if os.path.exists(filename):
                os.remove(filename)
        else:
            self.SW = Login()
            if self.SW.exec_():
                self.lbl_user_account.setText("Hoşgeldin " + self.SW.kullanici)
                self.lbl_user_account.adjustSize()
                name = self.SW.kullanici.split(" ")
                self.lbl_user_name_surname.setText("")

                self.lbl_img_user.setText(name[0][0].upper() + name[1][0].upper())
                self.lbl_img_user.setFont(QFont('Arial', 40))
                self.lbl_img_user.setAlignment(QtCore.Qt.AlignCenter)
                self.lbl_img_user.setStyleSheet(
                    "color : #dddddd; background-color: {}; border: 3px; border-radius: 50px;".format(self.userColor[name[0][0].upper()]))
                self.parentImage.setText(name[0][0].upper() + name[1][0].upper())
                self.parentImage.setFont(QFont('Arial', 20))
                self.parentImage.setAlignment(QtCore.Qt.AlignCenter)
                self.parentImage.setStyleSheet(
                    "color : #dddddd; background-color: {}; border: 3px; border-radius: 27px".format(self.userColor[name[0][0].upper()]))

                self.btn_register.hide()
                self.loginOk = True
                self.btn_signIn.setText("Çıkış Yap")

    def UserRegisterClick(self):
        self.SW = Register()
        self.SW.exec_()

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        self.setStyleSheet("Background-color:#F6FBE6; border:none;")
        self.setWindowTitle(" ")
        self.setWindowIcon(QIcon(':/icon/images/transparent.png'))

        self.setFixedSize(QSize(200, 270))

    def setupUi(self, Form):
        Form.setObjectName("Form")
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Popup)

        layout = QVBoxLayout()
        self.lbl_img_user.setPixmap(QPixmap(':/icon/images/user1.png'))
        self.lbl_img_user.setScaledContents(True)
        self.lbl_img_user.setFixedWidth(100)
        self.lbl_img_user.setFixedHeight(100)

        self.btn_register.setFixedHeight(40)
        self.btn_signIn.setFixedHeight(40)
        self.btn_register.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_signIn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.lbl_user_name_surname.setAlignment(Qt.AlignCenter)
        self.lbl_user_name_surname.setGeometry(105, 0, 25, 190)
        self.lbl_user_name_surname.setStyleSheet(
            "background-color:transparent; font-size: 14px; color:#a6a6a6;font-weight: bold;")

        btn_style = "color:white; border: 1px solid; border:transparent; border-radius: 8px 8px 8px 8px;"
        self.btn_register.setStyleSheet(
            "QPushButton { background-color: #008891;" + btn_style + "} QPushButton:pressed { background-color: "
                                                                     "#5eaaa8; } ")
        self.btn_signIn.setStyleSheet(
            "QPushButton { background-color: #ad6c80; " + btn_style + "} QPushButton:pressed { background-color: "
                                                                      "#ee99a0; }")
        self.lbl_user_account.setStyleSheet("color:grey")

        layout.addWidget(self.lbl_img_user, alignment=Qt.AlignCenter)
        layout.addWidget(self.lbl_user_account, alignment=Qt.AlignCenter)
        layout.addWidget(self.btn_register)
        layout.addWidget(self.btn_signIn)
        self.setLayout(layout)

    def readToken(self):
        try:
            basename = self.c.checkPath(os.path.dirname(parentdir))
            filename = basename + '/Config/token'
            tokenLine = ""
            if os.path.exists(filename):
                with open(filename, "r") as f:
                    d = f.readlines()
                    f.seek(0)
                    for i in d:
                        if i.split(':')[0] == "token":
                            tokenLine = i
                token = tokenLine.split(':', 1)[1].strip()
                if token == "":
                    return 0

                headers = {'Authorization': 'Bearer ' + token}
                myobj = {'mac_address': hex(uuid.getnode())}
                res = requests.post("http://pynar.org/api/user/info", headers=headers, data=myobj)
                res_json = res.json()
                if res_json['ok'] == True:
                    self.SW = Login()
                    self.SW.kullanici = res_json['result'].get('user_fullname')
                    self.SW.userData = res_json['result']
                    self.SW.token = token
                    self.lbl_user_account.setText("Hoşgeldin " + self.SW.kullanici)
                    self.lbl_user_account.adjustSize()
                    name = self.SW.kullanici.split(" ")
                    self.lbl_user_name_surname.setText("")
                    self.lbl_img_user.setText(name[0][0].upper() + name[1][0].upper())
                    self.lbl_img_user.setFont(QFont('Arial', 40))
                    self.lbl_img_user.setAlignment(QtCore.Qt.AlignCenter)
                    self.lbl_img_user.setStyleSheet(
                        "color : #F9F9F9; background-color: {}; border: 3px; border-radius: 27px;".format(self.userColor[name[0][0].upper()]))
                    self.parentImage.setText(name[0][0].upper() + name[1][0].upper())
                    self.parentImage.setFont(QFont('Arial', 20))
                    self.parentImage.setAlignment(QtCore.Qt.AlignCenter)
                    self.parentImage.setStyleSheet(
                        "color : #F9F9F9; background-color: {}; border: 3px; border-radius: 27px".format(self.userColor[name[0][0].upper()]))

                    self.loginOk = True
                    self.btn_register.hide()
                    self.btn_signIn.setText("Çıkış Yap")

                else:
                    newTokenLine = "token: "
                    with open(filename, "r+") as f:
                        d = f.readlines()
                        f.seek(0)
                        for i in d:
                            if i.split(':')[0] != "token":
                                f.write(i)
                            else:
                                f.write(newTokenLine)
                        f.truncate()
        except:
            pass

    def uploadCloud(self, textpad, log):
        if not self.loginOk:
            self.message("Hata!", "Dosyanızı yükleyebilmeniz için sisteme giriş yapmış olmanız gerekmektedir.")
        elif (len(textpad.text()) == 0):
            self.message("Hata!", "Boş dosya yollayamazsınız")
        else:
            fileManager = fileUploadWindow(textpad,token=self.SW.token, log=log, cloud=True)
            if textpad.filename == None:
                fileManager.exec()
            else:
                fileManager.uploadCloud()
            self.returnValue = fileManager.returnValue


    def downloadCloud(self):
        try:
            if self.loginOk:
                headers = {'Authorization': 'Bearer ' + self.SW.token}
                myobj = {'mac_address': hex(uuid.getnode())}
                res = requests.post("http://pynar.org/api/user/file/uploadedFiles", headers=headers, data=myobj)
                res_json = res.json()

                if res_json['ok'] != True:
                    raise Exception(res_json["description"])

                dialog = FilesWindow("Dosyalar", res_json['result']['files'], self.SW.token)
                dialog.exec()
                if dialog.fullpath != None:
                    self.parent.open(starter=True,getPath=dialog.fullpath)
                    return 1

            else:
                self.message("Hata!", "Dosyalarınızı Görebilmeniz için sisteme giriş yapmış olmanız gerekmektedir.")

        except Exception as e:
            self.dialog_critical(str(e))

    def dialog_critical(self, text):
        mesajKutusu = QMessageBox()
        mesajKutusu.setWindowIcon(QtGui.QIcon(":/icon/images/headerLogo1.png"))
        mesajKutusu.setWindowTitle("Dikkat !!!")
        mesajKutusu.setText(text)
        mesajKutusu.setIcon(QMessageBox.Critical)
        mesajKutusu.setStandardButtons(QMessageBox.Ok)
        mesajKutusu.exec()

    def message(self,title,text,inf=False):
        mesajKutusu = QMessageBox()
        mesajKutusu.setWindowIcon(QtGui.QIcon(":/icon/images/headerLogo1.png"))
        mesajKutusu.setWindowTitle(title)
        mesajKutusu.setText(text)
        if inf:
            mesajKutusu.setIcon(QMessageBox.Information)
        else:
            mesajKutusu.setIcon(QMessageBox.Warning)
        mesajKutusu.setStandardButtons(QMessageBox.Ok)
        mesajKutusu.exec()

    def teacherUpCloud(self, textpad):
        if not self.loginOk:
            self.message("Hata!", "Dosyanızı yükleyebilmeniz için sisteme giriş yapmış olmanız gerekmektedir.")
        elif (len(textpad.text()) == 0):
            self.message("Hata!", "Boş dosya yollayamazsınız")
        else:
            fileManager = fileUploadWindow(textpad,self.SW.token)
            if textpad.filename == None:
                fileManager.exec()
            else:
                fileManager.uploadTeacher()
            self.returnValue = fileManager.returnValue


    def message(self,title,text,inf=False):
        mesajKutusu = QMessageBox()
        mesajKutusu.setWindowIcon(QtGui.QIcon(":/icon/images/headerLogo1.png"))
        mesajKutusu.setWindowTitle(title)
        mesajKutusu.setText(text)
        if inf:
            mesajKutusu.setIcon(QMessageBox.Information)
        else:
            mesajKutusu.setIcon(QMessageBox.Warning)
        mesajKutusu.setStandardButtons(QMessageBox.Ok)
        mesajKutusu.exec()
