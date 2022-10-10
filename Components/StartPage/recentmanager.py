import os
import sys
from PyQt5.QtWidgets import QMessageBox

from Components.MessageBox.CustomizeMessageBox import CustomizeMessageBox_Ok
from configuration import Configuration
from datetime import datetime
import json

class RecentManager():
    def __init__(self):
        self.limit = 10
        self.c = Configuration()
        self.jsonFile = self.c.getHomeDir() + self.c.getJsonPath("recentJson")
        
    # Recent dosyası yoksa oluşturan method
    def createRecentJson(self):
        data = {}
        data['files'] = []

        with open(self.jsonFile, 'w') as outfile:
            json.dump(data, outfile)

    # Recent dosyasına yeni açılan dosyayı ekler, dosya varsa tarihini günceller
    def addItem(self,pFileName,pFilePath):

        try:
            # Recent dosyası yoksa recent dosyası oluşturulur.
            if not os.path.exists(self.jsonFile):
                self.createRecentJson()

            with open(self.jsonFile) as json_file:
                data = json.load(json_file)

                hasRecord = False
                now = datetime.now()
                self.datetime = now.strftime("%d/%m/%Y %H:%M:%S")

                for p in data['files']:
                    if p['filepath'] == pFilePath:

                        p['opendate'] = self.datetime
                        hasRecord = True
                        break

                sorted_obj = dict(data)
                sorted_obj['files'] = sorted(data['files'], key=lambda x: x['opendate'],
                                             reverse=True)

                new_data = dict(sorted_obj)
                # IF START
                # yeni açılan dosya dizide yoksa ekleme işlemi yapılır
                if not hasRecord:
                    dataLength = len(sorted_obj['files'])
                    # Eğer gösterim limiti üzerinde açılan dosya varsa en eski tarihli açılan dosya diziden çıkarılır
                    if dataLength >= self.limit:
                        removeIndex = dataLength - 1
                        sorted_obj['files'].pop(removeIndex)

                    sorted_obj['files'].append({
                        'filename': pFileName,
                        'filepath': pFilePath,
                        'opendate': self.datetime
                    })

                    # Yeni eklenen ve güncellenen item listesi için sırala
                    data = dict(sorted_obj)
                    data['files'] = sorted(sorted_obj['files'], key=lambda x: x['opendate'],
                                                 reverse=True)
                    new_data = dict(data)
                # IF END

                with open(self.jsonFile, 'w') as outfile:
                    json.dump(new_data, outfile)

            return True
        except Exception as err:
            print("error: {0}".format(err))
            return False

    # Recent dosyasında olmayan path varsa siler
    def removeItem(self,pFilePath):
        try:
            with open(self.jsonFile) as json_file:

                data = json.load(json_file)

                #FIND START
                index=0
                for p in data['files']:
                    if p['filepath'] == pFilePath :
                        data['files'].pop(index)
                        break
                    index = index +1
                # FIND END


                with open(self.jsonFile, 'w') as outfile:
                   json.dump(data, outfile)

            return True
        except:
            CustomizeMessageBox_Ok('Listeden çıkarma işlemi gerçekleştirilemedi!', "critical")
            return False

    # recent dosyası içindeki pathlar geçersiz ise hepsini siler
    # (Başka kullanıcı programı ilk kez yüklediyse eğer boş gelmesi gerektiği için böyle yapıldı)
    # production üretilirken prefrecent değeri her zman first olarak atanacak
    def removeAllItemNotExist(self):
        if self.c.config['PreferenceRecent']['prefrecent'] == 'first':
            try:
                new_data = {}
                new_data['files'] = []

                with open(self.jsonFile, 'w') as outfile:
                    json.dump(new_data, outfile)

                self.c.updateConfig('PreferenceRecent','prefrecent','second')
            except Exception as err:
                print("error: {0}".format(err))
