import sqlite3 as sql
from datetime import datetime
import os
import uuid
import tempfile
import datetime

class error_outputs_to_db:

    def __init__(self):
        self.parentdir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

    def writeLog(self, systemId, data, textPad):
        conn = sql.connect(self.parentdir + '/Config/errors.db')
        c = conn.cursor()

        machineId = systemId
        dateTime = datetime.fromtimestamp(int(data['time'])/1000)
        diagnostics = data['diagnostics']
        for i in range(len(diagnostics)):
            log = self.parseLog(diagnostics[i])
            c.execute("CREATE TABLE IF NOT EXISTS [error]([id] INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,[MachineId] TEXT NULL,[DateTime] TEXT NULL,[file] TEXT NULL,[severity] TEXT NULL,[message] TEXT NULL,[startLine] INTEGER NULL,[startChar] INTEGER NULL,[endLine] INTEGER NULL,[endChar] INTEGER NULL,[rule] TEXT NULL,[IndicatedText] TEXT NULL)")
            c.execute("INSERT INTO error('MachineId','DateTime','file','severity','message','startLine','startChar','endLine','endChar', 'rule', 'IndicatedText') VALUES (?,?,?,?,?,?,?,?,?,?,?)",(machineId, dateTime, log[0], log[1], log[2], log[3] + 1, log[4], log[5] + 1, log[6], log[7], self.getText(textPad, log)))

        conn.commit()
        c.close()
        conn.close()

    def parseLog(self, diagnostics):
        file = diagnostics['file']
        severity = diagnostics['severity']
        message = diagnostics['message']
        startLine = diagnostics['range']['start']['line']
        startChar = diagnostics['range']['start']['character']
        endLine = diagnostics['range']['end']['line']
        endChar = diagnostics['range']['end']['character']
        try:
            rule = diagnostics['rule']
        except:
            rule = None

        return [file, severity, message, startLine, startChar, endLine, endChar, rule]

    def getText(self,textPad,log):
        text = ""
        for k in range(log[3],log[5] + 1):
            text += textPad.text(k)
        return text

    def writeNewLog(self, file, errorMessage):
        machineId = self.generate_system_id()
        dateTime = datetime.datetime.now()

        if errorMessage != "" and errorMessage != None:
            conn = sql.connect(self.parentdir + '/Config/errors.db')
            c = conn.cursor()

            c.execute("CREATE TABLE IF NOT EXISTS [error]([id] INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,[MachineId] TEXT NULL,[DateTime] TEXT NULL,[file] TEXT NULL,[severity] TEXT NULL,[message] TEXT NULL,[startLine] INTEGER NULL,[startChar] INTEGER NULL,[endLine] INTEGER NULL,[endChar] INTEGER NULL,[rule] TEXT NULL,[IndicatedText] TEXT NULL)")
            c.execute("INSERT INTO error('MachineId','DateTime','file','severity','message') VALUES (?,?,?,?,?)",(machineId, dateTime,file,"runtime error",errorMessage,))

            conn.commit()
            c.close()
            conn.close()

    def writeCmdError(self,file,message,startLine,rule,IndicatedText):
        machineId = self.generate_system_id()
        dateTime = datetime.datetime.now()

        conn = sql.connect(self.parentdir + '/Config/errors.db')
        c = conn.cursor()

        c.execute(
            "CREATE TABLE IF NOT EXISTS [error]([id] INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,[MachineId] TEXT NULL,[DateTime] TEXT NULL,[file] TEXT NULL,[severity] TEXT NULL,[message] TEXT NULL,[startLine] INTEGER NULL,[startChar] INTEGER NULL,[endLine] INTEGER NULL,[endChar] INTEGER NULL,[rule] TEXT NULL,[IndicatedText] TEXT NULL)")
        c.execute("INSERT INTO error('MachineId','DateTime','file','severity','message','startLine','rule','IndicatedText') VALUES (?,?,?,?,?,?,?,?)",
                  (machineId, dateTime, file, "runtime error", message,startLine,rule,IndicatedText,))

        conn.commit()
        c.close()
        conn.close()

    def writePyrightError(self,errorMessage,textPad):
        conn = sql.connect(self.parentdir + '/Config/errors.db')
        c = conn.cursor()

        c.execute(
            "CREATE TABLE IF NOT EXISTS [error]([id] INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,[MachineId] TEXT NULL,[DateTime] TEXT NULL,[file] TEXT NULL,[severity] TEXT NULL,[message] TEXT NULL,[startLine] INTEGER NULL,[startChar] INTEGER NULL,[endLine] INTEGER NULL,[endChar] INTEGER NULL,[rule] TEXT NULL,[IndicatedText] TEXT NULL)")
        for jsonData in errorMessage:
            file = jsonData['file']
            severity = jsonData['severity']
            message = jsonData['message']
            try:
                rule = jsonData['rule']
            except:
                rule = None
            startLine = int(jsonData['range']['start']['line']) + 1
            startChar = int(jsonData['range']['start']['character'])
            endLine = int(jsonData['range']['end']['line']) + 1
            endChar = int(jsonData['range']['end']['character'])

            text = textPad.text().split("\n")
            IndicatedText = ""

            if startLine == endLine:
                IndicatedText = text[startLine - 1]
            else:
                for i in range(startLine-1,endLine):
                    IndicatedText += text[i]

            machineId = self.generate_system_id()
            dateTime = datetime.datetime.now()

            c.execute("INSERT INTO error('MachineId','DateTime','file','severity','message','startLine','startChar','endLine','endChar','rule','IndicatedText') VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                      (machineId, dateTime, file, severity, message,startLine,startChar,endLine,endChar,rule,IndicatedText,))

            conn.commit()
        c.close()
        conn.close()
    def generate_system_id(self):
        mac_address = uuid.getnode()
        system_id = (mac_address & 0xffffffffff)
        return system_id