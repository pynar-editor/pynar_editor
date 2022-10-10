# configuration.py

import configparser
import os
import sys

class Configuration():
    
    def __init__(self):
        
        self.config = configparser.ConfigParser()
        file = self.getDir()
        
        self.config.read(file)

    def getHomeDir(self):
        path = os.path.realpath(__file__)
        basename = self.checkPath(os.path.dirname(path))
        return basename + '/'

    def getDir(self):
        path = os.path.realpath(__file__)      # Pfad ermitteln
        
        basename = self.checkPath(os.path.dirname(path))
        path = basename + '/Config/pynar.ini'
        
        return path

    def getRun(self, system):
        return self.config['Run'][system]
    
    def getTerminal(self, system):
        return self.config['Terminal'][system]
    
    def getInterpreter(self, system):
        return self.config['Interpreter'][system]
    
    def getSystem(self):
        return self.config['System']['system']
    
    def getTab(self):
        return self.config['Tab']['tab']
    
    def getFontSize(self):
        return self.config['Size']['size']

    def getEditorFontSize(self):
        return int(self.config['Size']['editorsize'])

    def getHistoryMenuFontSize(self):
        return int(self.config['Size']['historymenusize'])

    # MSTF: Log bilgileri
    def getLogEnabled(self):
        return self.config['Logging']['logging']

    def getLogFolder(self):
        return self.config['Logging']['Log_folder']

    def getExamLogEnabled(self):
        return self.config['ExamLogging']['examLogging']

    def getExamLogFolder(self):
        return self.config['ExamLogging']['ExamLog_folder']

    def getChatbotStatusEnabled(self):
        return self.config['ChatbotStatus']['chatbotStatus']

    def getCodeFont(self):
        return self.config['Font']['code_font']

    def getEditorFont(self):
        return self.config['Font']['editor_font']

    def getHistoryMenuFont(self):
        return self.config['Font']['editor_font']

    def setCodeFont(self,font):
        self.updateConfig('Font', 'code_font', font)

    def setEditorFont(self,font):
        self.updateConfig('Font', 'editor_font', font)

    def getHtmlChatbotPath(self, param):
        return self.config['HtmlChatbot'][param]
              
    def getHtmlExamPath(self, param):
        return self.config['HtmlExam'][param]

    def getDataDirPath(self, param):
        return self.config['Data'][param]

    def getServerAddress(self):
        return self.config['ServerAddress']['server_address']

    def getDurationExamsRefresh(self):
        return self.config['DurationExamsRefresh']['duration_exams_refresh']

    def getReleaseInfo(self):
        return self.config['releaseInfo']['release']
        
    def getAutoCloseOnK(self):
        return self.config['OnK']['autoclose']
        
    def getStatusBarOnK(self):
        return self.config['OnK']['statusbar']

    def setSystem(self, system):
        self.config['System']['system'] = system

        path = os.path.realpath(__file__)    
        basename = self.checkPath(os.path.dirname(path))

        iniPath = basename + "/Config/pynar.ini"
        
        with open(iniPath, 'w', encoding='utf-8') as f:
            self.config.write(f)

    def updateConfig(self,selector,param,value):
        self.config[selector][param] = value

        path = os.path.realpath(__file__)
        basename = self.checkPath(os.path.dirname(path))

        iniPath = basename + "/Config/pynar.ini"

        with open(iniPath, 'w', encoding='utf-8') as f:
            self.config.write(f)

    def setStandard(self):
        config = configparser.ConfigParser()
        
        config['Run'] = {}
        config['Run']['mate'] = 'mate-terminal -x sh -c "python3 {}; exec bash"'
        config['Run']['pardus'] = 'xfce4-terminal -x sh -c "python3 {}; exec bash"'
        config['Run']['gnome'] = 'gnome-terminal -- sh -c "python3 {}; exec bash"'
        config['Run']['kde'] = 'konsole --hold -e "python3 {}"'
        config['Run']['xterm'] = 'xterm -hold -e "python3 {}"'
        config['Run']['windows'] = 'start cmd.exe /k "TITLE PYNAR CALISTIR & color 0F & prompt $G & python {} & echo. &(Pause >nul | echo Devam icin bir tusa basiniz...) & exit"'
        config['Run']['mac'] = 'open -a Terminal ./python3 {}'
        
        config['Terminal'] = {}
        config['Terminal']['mate'] = 'mate-terminal'
        config['Terminal']['pardus'] = 'xfce4-terminal'
        config['Terminal']['gnome'] = 'gnome-terminal'
        config['Terminal']['kde'] = 'konsole'
        config['Terminal']['xterm'] = 'xterm'
        config['Terminal']['windows'] = 'start cmd'
        config['Terminal']['mac'] = 'open -a Terminal ./' 
        
        config['Interpreter'] = {}
        config['Interpreter']['mate'] = 'mate-terminal -x "python3"'
        config['Interpreter']['pardus'] = 'xfce4-terminal -x "python3"'
        config['Interpreter']['gnome'] = 'gnome-terminal -- "python3"'
        config['Interpreter']['kde'] = 'konsole -e python3'
        config['Interpreter']['xterm'] = 'xterm python3'
        config['Interpreter']['windows'] = 'start cmd /K "TITLE PYTHON YORUMLAYICI & python"'
        config['Interpreter']['mac'] = 'open -a Terminal ./python3'
        
        config['System'] = {}
        config['System']['system'] = ''
        config['System']['installed_pythons_versions'] = ''
        config['System']['installed_pythons_exes'] = ''
        config['System']['selected_python_version'] = ''
        config['System']['selected_python_exe'] = ''
        config['System']['automatic_selection'] = 'True'

        
        config['Tab'] = {}
        config['Tab']['tab'] = '6'
        
        config['Size'] = {}
        config['Size']['size'] = '16'
        config['Size']['editorsize'] = '10'

        config['JsonFiles'] = {}
        config['JsonFiles']['recentjson'] = 'Data/recents.json'

        config['PreferenceRecent'] = {}
        config['PreferenceRecent']['prefrecent'] = 'first'

        config['TreeMenuFiles'] = {}
        config['TreeMenuFiles']['tree_menu_path'] = 'Data/TreeMenuFiles/'

        config['HtmlHelpFiles'] = {}
        config['HtmlHelpFiles']['html_help_path'] = 'Data/HtmlHelpFiles/'

        config['HtmlChatbot'] = {}
        config['HtmlChatbot']['html_chatbot'] = 'Data/HtmlChatbot/'

        config['HtmlExam'] = {}
        config['HtmlExam']['html_exam'] = 'Data/HtmlExam/'

        config['LicenseFiles'] = {}
        config['LicenseFiles']['license_files'] = 'Data/LicenseFiles/'

        config['Logging'] = {}
        config['Logging']['logging'] = 'True'
        config['Logging']['log_folder'] = 'Log'

        config['ExamLogging'] = {}
        config['ExamLogging']['examLogging'] = 'True'
        config['ExamLogging']['log_folder'] = 'Log'

        config['ChatbotStatus'] = {}
        config['ChatbotStatus']['chatbotStatus'] = 'True'

        config['Font']['code_font'] = 'Consolas'
        config['Font']['editor_font'] = 'Segoe UI'
        
        config['OnK']['autoclose'] = 'True'
        config['OnK']['statusbar'] = 'True'

        return config


    def checkPath(self, path):
        if '\\' in path:
            path = path.replace('\\', '/')
        return path


    def getJsonPath(self, param):
        return self.config['JsonFiles'][param]

    def getTreeMenuPath(self, param):
        return self.config['TreeMenuFiles'][param]

    def getHtmlHelpPath(self, param):
        return self.config['HtmlHelpFiles'][param]

    def getLicenseFiles(self, param):
        return self.config['LicenseFiles'][param]

    def getParam(self,selector, param):
        return self.config[selector][param]

    def getShell(self):
        return True if self.config['System']['system'] == "windows" else False

    def setInstalledPythonsVersions(self, param):
        self.config['System']['installed_pythons_versions'] = param

        path = os.path.realpath(__file__)
        basename = self.checkPath(os.path.dirname(path))

        iniPath = basename + "/Config/pynar.ini"

        with open(iniPath, 'w', encoding='utf-8') as f:
            self.config.write(f)

    def getInstalledPythonsVersions(self):
        return self.config['System']['installed_pythons_versions']

    def setInstalledPythonsExes(self, param):
        self.config['System']['installed_pythons_exes'] = param

        path = os.path.realpath(__file__)
        basename = self.checkPath(os.path.dirname(path))

        iniPath = basename + "/Config/pynar.ini"

        with open(iniPath, 'w', encoding='utf-8') as f:
            self.config.write(f)

    def getInstalledPythonsExes(self):
        return self.config['System']['installed_pythons_exes']

    def setSelectedPythonVersion(self, param):
        self.config['System']['selected_python_version'] = param

        path = os.path.realpath(__file__)
        basename = self.checkPath(os.path.dirname(path))

        iniPath = basename + "/Config/pynar.ini"

        with open(iniPath, 'w', encoding='utf-8') as f:
            self.config.write(f)

    def getSelectedPythonVersion(self):
        return self.config['System']['selected_python_version']		

    def setSelectedPythonExe(self, param):
        self.config['System']['selected_python_exe'] = param

        path = os.path.realpath(__file__)
        basename = self.checkPath(os.path.dirname(path))

        iniPath = basename + "/Config/pynar.ini"

        with open(iniPath, 'w', encoding='utf-8') as f:
            self.config.write(f)

    def getSelectedPythonExe(self):
        return self.config['System']['selected_python_exe']

    def setAutoSelectState(self, param):
        self.config['System']['automatic_selection'] = param

        path = os.path.realpath(__file__)
        basename = self.checkPath(os.path.dirname(path))

        iniPath = basename + "/Config/pynar.ini"

        with open(iniPath, 'w', encoding='utf-8') as f:
            self.config.write(f)

    def getAutoSelectState(self):
        return self.config['System']['automatic_selection']


if __name__ == '__main__':
    c = Configuration()

    system = c.getSystem()
    runCommand = c.getRun(system)
    terminalCommand = c.getTerminal(system)
    interpreterCommand = c.getInterpreter(system)

    #c.setSystem('gnome')

    print(system + ':\n' + runCommand + '\n' + terminalCommand + '\n' + interpreterCommand)
    
