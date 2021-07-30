import subprocess,os,sys
import json
import uuid
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon
from datetime import datetime
from pathlib import Path
from configuration import Configuration
from Components.ErrorConsole.error_outputs_to_db import error_outputs_to_db
import hashlib
import sqlite3 as sl

class writeLog():
    cmdControl = 0
    def __init__(self, data_folder, errorConsole, splitterV):
        self.c = Configuration()
        self.errDict = {}
        self.splitterV = splitterV
        self.errorConsole = errorConsole
        self.closeButton = self.errorConsole.closeButton
        self.data_folder = data_folder
        self.data_folder = Path(self.data_folder)
        self.data_folder = self.data_folder / self.c.getLogFolder()
        self.dataBase = error_outputs_to_db()
        osSystem = self.c.getSystem()
        if osSystem == "windows":
            self.pyright = 'pyright-win.exe'
        elif osSystem == "mac":
            self.pyright = 'pyright-mac'
        else:
            self.pyright = 'pyright-linux'

    def parser(self,textPad):
        self.cmdControl = 0
        parentdir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
        try:
            pyright_exe_path = parentdir + '/Bin'
            pyright_exe_file = os.path.join(pyright_exe_path, self.pyright)
            if self.pyright == 'pyright-linux':
                os.chmod(pyright_exe_file, 0o755)
            self.result = subprocess.run([pyright_exe_file, "-p", pyright_exe_path, "--outputjson", textPad.filename], capture_output=True, text=True, encoding='utf-8', shell = self.c.getShell())
			#pyright 1.1.144 sürümünde diagnostics yerine generalDiagnostics şeklinde json property üretiyor, bunun için replace fix eklendi.
            self.parseData = json.loads(self.result.stdout.replace("generalD","d"))
            if(self.parseData['summary']['errorCount']):
                if self.c.getLogEnabled() == "True":
                    #Loglama degeri True ise log degerlerini gonder
                    textPad.mainWindow.errorgridlog(self.parseData)
                self.errDict[textPad] = self.parseData['diagnostics']
                self.addErrorConsole(textPad)
                self.splitterV.setSizes([500, 214])
                self.cmdControl = 1

                self.dataBase.writePyrightError(self.parseData['diagnostics'],textPad)

            else:
                self.closePressed(textPad)
                self.splitterV.setSizes([714, 0])
                self.cmdControl = 2
        except:
            messageBox = QMessageBox(QMessageBox.Question, "text", "text")
            messageBox.setWindowIcon(QIcon(parentdir+'/images/headerLogo1.png'))
            messageBox.setStandardButtons(QMessageBox.Ok)
            messageBox.setWindowTitle("Uyarı!")
            messageBox.setText("Hata mesajlarını görüntüleyebilmeniz için lütfen pyright programının Windows, Linux ve MacOS binary dosyalarını programın kurulu olduğu Bin klasörü içine kopyalayınız.")
            messageBox.setIcon(QMessageBox.Warning)
            messageBox = messageBox.exec()


    def generate_system_id(self):
        mac_address = uuid.getnode()
        system_id = (mac_address & 0xffffffffff)
        return system_id

    def initialize_log(self, textPad):
        time = datetime.now()
        timestamp = str(time.strftime('%Y_%m_%d-%H_%M_%S.%f')[:-3])
        systemId = str(self.generate_system_id())
        try:
            self.data_folder.mkdir(parents=True, exist_ok=False)
        except Exception as err:
            pass
        file_to_write = self.data_folder / ("Error_" + systemId + "-" + timestamp + ".json")
        with open(file_to_write,"w") as f:
            json.dump(self.parseData, f, indent=4)

    def addErrorConsole(self, textPad):
        if(self.errDict.get(textPad, False)):
            self.errorConsole.add(self.errDict[textPad], textPad)

    def newErrorConsole(self, textPad):
        if(self.errDict.get(textPad, False)):
            self.addErrorConsole(textPad)
            self.splitterV.setSizes([500, 214])
        else:
            self.errorConsole.clear()
            self.splitterV.setSizes([714, 0])

    def removeError(self, textPad):
        if(self.errDict.get(textPad, False)):
            del self.errDict[textPad]

    def clearIndıcator(self,textPad):
        self.errorConsole.closeTab(textPad)


    def updateLines(self,textPad,prev_position,position):
        if (self.errDict.get(textPad, False)):
            if((prev_position[0] - position[0]) < 0):
                for i in range(len(self.errDict[textPad])):
                    if (self.errDict[textPad][i]['range']['start']['line'] > prev_position[0]):
                        self.errDict[textPad][i]['range']['start']['line'] += 1
                        self.errDict[textPad][i]['range']['end']['line'] += 1
                        self.addErrorConsole(textPad)
                    elif (self.errDict[textPad][i]['range']['start']['line'] < prev_position[0] < self.errDict[textPad][i]['range']['end']['line']):
                        self.errDict[textPad][i]['range']['end']['line'] += 1
                        self.addErrorConsole(textPad)
                    elif (self.errDict[textPad][i]['range']['end']['line'] == self.errDict[textPad][i]['range']['end']['line']) and (self.errDict[textPad][i]['range']['end']['line'] == prev_position[0]):
                        if (prev_position[1] == 0):
                            self.errDict[textPad][i]['range']['start']['line'] += 1
                            self.errDict[textPad][i]['range']['end']['line'] += 1
                            self.addErrorConsole(textPad)
                        elif (self.errDict[textPad][i]['range']['end']['line'] == prev_position[0]) and (self.errDict[textPad][i]['range']['end']['character'] == prev_position[1]):
                            pass
                        else:
                            self.errDict[textPad][i]['range']['end']['line'] += 1
                            self.errDict[textPad][i]['range']['end']['character'] -= prev_position[1]
                            self.addErrorConsole(textPad)
                    elif (self.errDict[textPad][i]['range']['end']['line'] == prev_position[0]):
                        if (prev_position[1] == 0):
                            self.errDict[textPad][i]['range']['end']['line'] += 1
                            self.addErrorConsole(textPad)
                        elif (self.errDict[textPad][i]['range']['end']['character'] == prev_position[1]):
                            pass
                        else:
                            self.errDict[textPad][i]['range']['end']['line'] += 1
                            self.errDict[textPad][i]['range']['end']['character'] -= prev_position[1]
                            self.addErrorConsole(textPad)
                    elif (self.errDict[textPad][i]['range']['start']['line'] == prev_position[0]):
                        if (prev_position[1] == 0):
                            self.errDict[textPad][i]['range']['start']['line'] += 1
                        self.errDict[textPad][i]['range']['end']['line'] += 1

            elif((prev_position[0] - position[0]) > 0):
                for i in range(len(self.errDict[textPad])):
                    if (self.errDict[textPad][i]['range']['start']['line'] > prev_position[0]):
                        self.errDict[textPad][i]['range']['start']['line'] -= 1
                        self.errDict[textPad][i]['range']['end']['line'] -= 1
                        self.addErrorConsole(textPad)
                    elif (self.errDict[textPad][i]['range']['start']['line'] < prev_position[0] <= self.errDict[textPad][i]['range']['end']['line']):
                        self.errDict[textPad][i]['range']['end']['line'] -= 1
                        self.addErrorConsole(textPad)
                    elif (self.errDict[textPad][i]['range']['start']['line'] == prev_position[0]):
                        if (prev_position[1] == 0):
                            self.errDict[textPad][i]['range']['start']['line'] -= 1
                            self.errDict[textPad][i]['range']['end']['line'] -= 1
                            self.addErrorConsole(textPad)

    def showCmdMessage(self,message,textPad):
        cmdError = """{
   "diagnostics":[
      {
         "file":" ",
         "severity":"error",
         "message":" ",
         "range":{
            "start":{
               "line":-1,
               "character":-1
            },
            "end":{
               "line":-1,
               "character":-1
            }
         },
         "rule":" "
      }
   ]
}"""
        typeList = ["str", "int", "float", "complex", "list", "tuple", "range", "dict", "set", "frozenset", "bool",
                    "bytes", "bytearray", "memoryview"]
        numList = []
        apostropheList = []
        doubleList = []
        tyList = []
        funcList = []
        try:
            messageParse = message.split("\n")
            line = messageParse[1].split(",")[1].split(" ")[2]
            errorValue = messageParse[2].strip()
            errorMessage = messageParse[3].split(" ")
            length = len(errorMessage)
            k = 0

            hashErrorMessage = ""

            for i in errorMessage:
                k += 1
                data = ""
                comma = False
                semicolon = False
                brackets = False
                dots = False
                square = False
                slash = False

                if "," in i:
                    i = i.replace(",", "")
                    comma = True
                if ";" in i:
                    i = i.replace(";", "")
                    semicolon = True
                if i.startswith("("):
                    i = i[1:]
                    brackets = True
                if i.endswith("]"):
                    i = i[:-1]
                    square = True
                if ":" in i:
                    i = i.replace(":","")
                    dots = True
                if i.endswith("#"):
                    slash = True

                if i[-2:] == "()":
                    data = "func() "
                    funcList.append(i)
                elif len(i.split("-")) == 2:
                    digit = True
                    for k in i.split("-"):
                        if not k.isdigit:
                            digit = False
                            break
                    if digit:
                        data = "#-# "
                        for k in i.split("-"):
                            numList.append(k)
                elif i.isdigit():
                    data = "#" + " "
                    numList.append(i)
                elif i in typeList and k == length:
                    data = "<TYPE> "
                    tyList.append(i)
                elif i.startswith("'") and i.endswith("'"):
                    data = "'' "
                    apostropheList.append(i)
                elif i.startswith('"') and i.endswith('"'):
                    data = '" '
                    doubleList.append(i)
                else:
                    data = i + " "

                if comma:
                    data = data[:-1] + ", "
                if semicolon:
                    data = data[:-1] + "; "
                if brackets:
                    data = "(" + data
                if dots:
                    data = data[:-1] + ": "
                if square:
                    data = data[:-1] + "] "
                if slash:
                    data = "#" + data

                hashErrorMessage += data
            hashErrorMessage = hashErrorMessage[:-1]
            hash_object = hashlib.md5(hashErrorMessage.encode())
            hashCode = hash_object.hexdigest()
            parentdir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))) + "/Config"
            db = sl.connect(parentdir + "/error_texts.db")
            cs = db.cursor()
            cs.execute("select message from errorMessage where hash = ?", (hashCode,))
            data = cs.fetchall()
            data = data[0][0].split(' ')
            hashErrorMessage = ""
            db.close()

            for i in data:
                comma = False
                semicolon = False
                if "," in i:
                    i = i.replace(",", "")
                    comma = True
                if ";" in i:
                    i = i.replace(";", "")
                    semicolon = True

                if i == "func()":
                    hashErrorMessage += funcList[0] + " "
                    del funcList[0]
                elif "##" in i:
                    index = i.rfind("#")
                    hashErrorMessage += i[:index] + numList[0] + i[index+1:] + " "
                elif "#" in i:
                    hashErrorMessage += i.replace("#", numList[0]) + " "
                    del numList[0]
                elif i == "<TYPE>":
                    hashErrorMessage += tyList[0] + " "
                    del tyList[0]
                elif i == "''":
                    hashErrorMessage += apostropheList[0] + " "
                    del apostropheList[0]
                elif i == '""':
                    hashErrorMessage += doubleList[0] + " "
                    del doubleList[0]
                else:
                    hashErrorMessage += i + " "

                if comma:
                    hashErrorMessage = hashErrorMessage[:-1] + ", "
                if semicolon:
                    hashErrorMessage += hashErrorMessage[:-1] + "; "
            hashErrorMessage = hashErrorMessage[:-1]
            hashErrorMessageShow = errorValue + "\n" + hashErrorMessage
            self.parseData = json.loads(cmdError)
            self.errDict[textPad] = self.parseData['diagnostics']
            self.errDict[textPad][0]['severity'] = "runtime error"
            self.errDict[textPad][0]['file'] = textPad.filename
            self.errDict[textPad][0]['message'] = hashErrorMessageShow
            self.errDict[textPad][0]['range']['start']['line'] = int(line) - 2
            self.errDict[textPad][0]['range']['end']['line'] = int(line) - 2
            self.errorConsole.add(self.errDict[textPad], textPad)
            self.splitterV.setSizes([500, 214])
            self.dataBase.writeCmdError(textPad.filename,hashErrorMessage,int(line) - 1,messageParse[3].split(":")[0],errorValue)
            return hashErrorMessageShow

        except :
            self.parseData = json.loads(cmdError)
            self.errDict[textPad] = self.parseData['diagnostics']
            self.errDict[textPad][0]['severity'] = "runtime error"
            self.errDict[textPad][0]['file'] = textPad.filename
            self.errDict[textPad][0]['message'] = message
            self.errorConsole.add(self.errDict[textPad], textPad)
            self.splitterV.setSizes([500, 214])

            self.dataBase.writeNewLog(textPad.filename, message)

            return message


    def closePressed(self, textPad):
        if (self.errDict.get(textPad, False)):
            self.errorConsole.textPadClear(textPad)
            del self.errDict[textPad]
        self.errorConsole.clear()
        self.splitterV.setSizes([714, 0])
