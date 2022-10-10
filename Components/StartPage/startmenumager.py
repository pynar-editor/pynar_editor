import os
import sys
from configuration import Configuration
from widgets import MessageBox
from datetime import datetime
import json


class StartMenuModel():
    def __init__(self, pMenuName,pMenuDesc,pMenuIcon, pMenuCode):
        self.MenuName = pMenuName
        self.MenuDesc = pMenuDesc
        self.MenuIcon = pMenuIcon
        self.MenuCode = pMenuCode

class StartMenuManager():
    def __init__(self):
        self.c = Configuration()
        self.menus = [
            StartMenuModel("Örnek Uygulama", "Merhaba Dünya uygulaması oluştur", ":/icon/images/pythonstart.png", "example"),
            StartMenuModel("Yeni", "Boş Python dosyası oluştur", ":/icon/images/addfile.png","new"),
            StartMenuModel("Aç", "Mevcut Python Dosyası Aç", ":/icon/images/openfile.png","open"),
            StartMenuModel("Atla", "Editör Ekranını Aç", ":/icon/images/skip.png", "skip"),
        ]