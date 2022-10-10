import os
import sys
import subprocess
import re

from PyQt5.QtWidgets import QMessageBox

from Components.MessageBox.CustomizeMessageBox import CustomizeMessageBox_Ok

parentdir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
# sys.path.append(parentdir) # nuitka'da sorun çıkarıyor.
from configuration import Configuration

class detectos:
    def writeIni(self):
        self.c = Configuration()
        self.systemName = self.osEnvironment()
        self.installed_pythons_versions , self.installed_python_exes = self.findPythonVersion()

        try:
            if ((self.c.getSystem() != self.systemName) or (self.c.getInstalledPythonsVersions() != self.installed_pythons_versions) or (self.c.getInstalledPythonsExes() != self.installed_python_exes)):
                try:
                    self.c.updateConfig('System', 'system', self.systemName)
                    self.c.updateConfig('System', 'installed_pythons_versions', self.installed_pythons_versions)
                    self.c.updateConfig('System', 'installed_pythons_exes', self.installed_python_exes)
                    self.c.updateConfig('System', 'selected_python_version', ' 3')
                    self.c.updateConfig('System', 'selected_python_exe', 'python' if self.systemName == 'windows' else 'python3')
                except:
                    self.standartWrite()
        except:
            self.standartWrite()

    def osEnvironment(self):
        if sys.platform in ["win32", "cygwin"]:
            return "windows"
        elif sys.platform == "darwin":
            return "mac"
        else:
            desktopEnv = os.environ.get("XDG_MENU_PREFIX")
            if desktopEnv is not None:
                desktopEnv = desktopEnv.lower()
                if desktopEnv in ["xterm-", "gnome-", "mate-", "kde-"]:
                    return desktopEnv.replace("-","")
                elif desktopEnv == "xfce-":
                    return "pardus"

    def standartWrite(self):
        config = self.c.setStandard()
        config['System']['system'] = self.systemName
        config['System']['installed_pythons_versions'] = self.installed_pythons_versions
        config['System']['installed_pythons_exes'] = self.installed_python_exes

        base = self.c.checkPath(parentdir)

        iniPath = base + "/Config/pynar.ini"
        with open(iniPath, 'w', encoding='utf-8') as f:
            config.write(f)

    def findPythonVersion(self):
        self.c = Configuration()
        operating_system = self.osEnvironment()

        if(operating_system == "windows"):
            output = subprocess.run(['where', 'python'], stdout=subprocess.PIPE).stdout.decode('utf-8')
            installed_pythons = output.replace('\r\n', ';').strip()
        elif(operating_system == "mac"):
            print("Python version finder is not supported in Mac")
            return
        else:
            output = subprocess.run(["which", "python3"], stdout=subprocess.PIPE).stdout.decode('utf-8')
            installed_pythons = output.replace('\n', ';').strip()

        installed_pythons_versions = []
        installed_python_exes = []

        for i in installed_pythons.split(';'):
            try:
                _result = subprocess.run([i, "-V"], stdout=subprocess.PIPE, check=True, stderr=subprocess.DEVNULL)
                installed_pythons_versions.append(_result.stdout.decode('utf-8'))
                installed_python_exes.append(repr(i).replace('\'',''))
            except (subprocess.CalledProcessError, OSError):
                pass

        installed_pythons_versions = [self.getVersionFromString(i) for i in installed_pythons_versions]

        #Confige yazmak için listeden ';' ile ayrılmış stringe dönüştür
        installed_pythons_versions = ';'.join(installed_pythons_versions)
        installed_python_exes = ';'.join(installed_python_exes)

        return installed_pythons_versions,installed_python_exes

    def getVersionFromString(self, _str):
        return re.search("[2-3]+(?:\.\d+)+", _str).group()