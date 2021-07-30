import os
import sys

parentdir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
# sys.path.append(parentdir) # nuitka'da sorun çıkarıyor.
from configuration import Configuration

class detectos:
    def writeIni(self):
        self.c = Configuration()
        self.systemName = self.osEnvironment()
        try:
            if self.c.getSystem() != self.systemName:
                try:
                    self.c.updateConfig('System', 'system', self.systemName)
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

        base = self.c.checkPath(parentdir)

        iniPath = base + "/Config/pynar.ini"
        with open(iniPath, 'w', encoding='utf-8') as f:
            config.write(f)
