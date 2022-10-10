import os
import textdist
from tokenize import tokenize
from difflib import SequenceMatcher
from io import BytesIO
from Components.CheckError import alignment
from Components.CheckError import prepare_output
from unidecode import unidecode
import re


class checkError:
    def __init__(self):
        self.parentDir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
        self.dataSetFile = os.listdir(self.parentDir + "/Data/CodeDataset")
        self.keywordFile = os.listdir(self.parentDir + "/Data/Python_Words")
        self.import_data = []
        self.text = ""  # Kodların satır bilgileri dahil test.py dosyasının içeriği.
        self.line = 0
        self.rule = []
        self.listed_python_data = []
        self.returnData = []

    def run(self, text, line, rule, message,
            errorLen):  # madde 1 için pyright çağırıldı ve çıktılar parse'ye gönderildi.
        self.text = text
        self.line = line
        return self.parse(rule, message, errorLen)

    def parse(self, rule, message,
              errorLen):  # pyright çıktılarındaki ilk hata mesajı ve dosyada karşılık gelen satır alındı.
        if len(errorLen) > 9:
            returnDataString = ("Kodlarda çok fazla hata tespit edildi :( Lütfen kodlarınızı baştan kontrol ediniz..")
            self.returnData.append(returnDataString)
            return self.returnData
        else:
            try:
                errorLine = self.text[self.line].replace("\r",
                                                         "")  # text değişkenin içinden hatalı satırı, errorLine içerisine kaydedildi.
                if errorLine[0:1] == "\t":
                    errorLine = errorLine.replace("\t", "")
                check_turkish_char = bool(re.search('[ÜüĞğİıŞşÇç]', str(errorLine), flags=0))
                if check_turkish_char == True:
                    errorLine = self.change_turkish_char(errorLine)
                try:
                    if (
                            rule == "reportGeneralTypeIssues"):  # from io import BytesIOxxxxx --> gibi hatalarda bu döngüye girecektir.
                        if errorLine.count("from") > 0:
                            split_errorLine = errorLine.split()
                            returnDataString = (
                                        "%s paketi Kurulu Değil veya Yanlış Yazılmış, Lütfen %s paketini kontrol ediniz.." % (
                                line1, line1))
                            self.returnData.append(returnDataString)
                            return self.returnData
                        else:
                            self.read_python_words()  # keywordFile içerisinde ki python oparatörleri okundu.
                            return self.kNN(errorLine)

                    elif (
                            rule == "reportMissingImports"):  # import xPandasx // from xxioxx import BytesIO  --> gibi hatalarda bu döngüye girecektir.
                        self.read_import_file()
                        offer_lib, similarity_score = self.import_similarty(errorLine)

                        if similarity_score > 0.75:
                            offer_lib = offer_lib.replace("\n", "")
                            self.returnData.append(str(offer_lib))
                        else:
                            split_errorLine = errorLine.split()
                            line1 = split_errorLine[1]
                            returnDataString = (
                                        "%s paketi Kurulu Değil veya Yanlış Yazılmış, Lütfen %s paketini kontrol ediniz.." % (
                                line1, line1))
                            self.returnData.append(returnDataString)
                        return self.returnData

                    elif (self.line == -1):
                        returnDataString = ("Hatalı satır doğru tespit edilemedi..")
                        self.returnData.append(returnDataString)
                        return self.returnData

                    elif ((errorLine == "") or (errorLine == " ")):
                        returnDataString = ("Hatalı satır doğru tespit edilemedi..")
                        self.returnData.append(returnDataString)
                        return self.returnData

                    elif (
                            message == "Girintisizlik beklenmiyor"):  # import xPandasx // from xxioxx import BytesIO  --> gibi hatalarda bu döngüye girecektir.
                        returnDataString = "girintihatasi" + errorLine
                        self.returnData.append(returnDataString)
                        return self.returnData

                    elif (
                            message == "Girintili kod bloğu bekleniyor"):  # import xPandasx // from xxioxx import BytesIO  --> gibi hatalarda bu döngüye girecektir.
                        returnDataString = "girintihatasi" + errorLine
                        self.returnData.append(returnDataString)
                        return self.returnData

                    else:
                        errorLine = self.space_checker(errorLine)
                        self.read_python_words()  # keywordFile içerisinde ki python oparatörleri okundu.
                        return self.kNN(errorLine)

                except:  # import hatası yok ise message["rule"] oluşturulmuyor bu yüzden try-except yapısı kuruldu.
                    errorLine = self.space_checker(errorLine)
                    self.read_python_words()  # keywordFile içerisinde ki python oparatörleri okundu.
                    return self.kNN(errorLine)
            except IndexError:
                if rule == []:  # kod bloğunda hata var ise diagnostics'te hatanın türü yazıyor. Hata yok ise boş listedir.
                    print("Test edilen kod parçasında sözdizimi hatası yoktur.")

    def read_python_words(self):  # keywordFile dosyalarının hepsinin data değişkeninde toplandı
        for i in range(len(self.keywordFile)):
            with open(self.parentDir + "/Data/Python_Words/" + self.keywordFile[i], "r",
                      errors="ignore") as f:
                if i == 0:
                    self.listed_python_data = f.read().splitlines()
                else:
                    self.listed_python_data += f.read().splitlines()

    def read_import_file(self):
        with open(self.parentDir + "/Data/CodeDataset/ImportDataset.txt", "r", errors="ignore") as f:
            self.import_data = f.readlines()

    def import_similarty(self, errorLine):
        max_similarity = 0
        for j in self.import_data:
            similarity = SequenceMatcher(None, errorLine, j).ratio()
            if similarity > max_similarity:
                max_similarity = similarity
                python_line_word = j
                # eğer kütüphanede yoksa hesaplat
        return python_line_word, max_similarity

    def is_user_string(self, dataList):

        nData = []
        for i in range(len(dataList)):
            if dataList[
                i] not in self.listed_python_data:  # hatalı satırımızı ve Python_Words tokenlerini karşılaştırıyoruz
                try:
                    if dataList[i - 1] == '"':  # " (tırnak içinde ki) değerlere _STR_ yazdık.
                        nData.append("_STR_")
                    elif dataList[i + 1] == '"':
                        nData.append("_STR_")
                    else:
                        nData.append(dataList[i])
                except:
                    nData.append(dataList[i])
            else:
                nData.append(dataList[i])
        return nData

    def token(self, data):  # ilk olarak hatalı satırı tokenlerine ayırmak için kullandık.
        tokenarray = []  # ikinci olarak KNN algoritmasından gelen 5 en yüksek puanlı önerileri tokenize etmek için kullandık.

        if (((data.count("(") + data.count(")")) % 2 != 0) or  # parantez sayısı eşitmi kontrol ettik.
                ((data.count("[") + data.count("]")) % 2 != 0)):  # değil ise check_brackets metodunu çalıştırdık.

            data = self.check_brackets(data)

        g = tokenize(BytesIO(data.encode('utf-8')).readline)

        for token in g:  # gelen data verisi tokenlerine ayrılarak liste içeriği null karakterden arındırıldı.
            if token.string != '' and token.string != "\n":
                if token.string[0] == '"' and token.string[-1] == '"' and len(
                        token.string) > 2:  # String değerlerde ki " işaretini ayrımak için ayrı bir koşul bloğu yazıldı.
                    tokenarray.append('"')
                    tokenarray.append(token.string[1:-1])
                    tokenarray.append('"')
                else:
                    tokenarray.append(token.string)

        return tokenarray[
               1:]  # ilk değer her zaman utf-8 olduğu için çıkan sonucun 1. indisinden itibaren liste geri döndürüldü

    def check_brackets(self, data):  # tokenizasyon işleminde parantez sayısı eşit olmadığı zaman
        # tokenizasyon sırasında hata meydana geliyor. Bu durumu engellemek için
        # hatalı satırda eşit sayıda parantez yok ise parantezlerin hepsini kaldırdık
        data = data.replace("(", " ")
        data = data.replace(")", " ")
        data = data.replace("[", " ")
        data = data.replace("]", " ")
        return data

    def change_turkish_char(self, errorLine):
        try:
            special_string = re.search('"(.*)"', str(errorLine))
            special_string = (special_string.group(1))
            special_string = ''.join((special_string, '"'))  # Character at end
            special_string = ''.join(('"', special_string))  # Character at start
            text_without_turk_char = unidecode(str(errorLine))
            errorLine = re.sub('".*?"', special_string, text_without_turk_char, flags=re.DOTALL)
            errorLine = errorLine.replace("[", "")
            errorLine = errorLine.replace("]", "")
            errorLine = errorLine.replace("'", "")
            errorLine = errorLine.replace("'", "")
            # errorLine = [errorLine]
        except AttributeError:
            pass
        return errorLine

    def space_checker(self, errorLine):
        while True:
            if errorLine[0] == " ":
                errorLine = errorLine[1:]
            else:
                break
        return errorLine

    def prepare_return_string(self, result_list):
        if len(result_list) == 0:
            returnString = "#"

        else:
            returnString = ""
            for i in result_list:
                if i == "(" or i == ")":
                    try:
                        if returnString[-1] == ')':
                            returnString += i
                        elif (returnString[-1] != "(") and (returnString[-1] != '"'):
                            returnString = returnString[:-1] + i
                        else:
                            returnString += i
                    except:
                        returnString += i
                elif i == ".":
                    returnString = returnString[:-1] + i
                else:
                    try:
                        if returnString[-1] == '.':
                            returnString += i + " "
                        elif returnString[-2] == '"':
                            if ((returnString[-1] == '.') | (returnString[-1] == ',')
                                    | (returnString[-1] == '(') | (returnString[-1] == ')')
                                    | (returnString[-1] == '[') | (returnString[-1] == ']')
                                    | (returnString[-1] == '{') | (returnString[-1] == '}')
                                    | (returnString[-1] == ':') | (returnString[-1] == '=')):
                                returnString += i + " "
                            else:
                                returnString = returnString[:-1] + i
                        else:
                            returnString += i + " "
                    except:
                        returnString += i + " "
        return returnString

    def kNN(self, errorLine):
        # tüm datasetler okundu ve liste olarak data değişkenine kaydedildi.
        with open(self.parentDir + "/Data/CodeDataset/CodeDataset.txt", "r", errors="ignore") as f:
            data = f.readlines()

        errorDataRAW = self.token(errorLine)  # hatalı kod parçası tokenlerine ayrıldı.
        errorData = self.is_user_string(errorDataRAW)
        errorDataCopy = errorData.copy()
        OriginalStrings = list(i for i in errorDataRAW if not i in errorData or errorDataCopy.remove(i))
        # OriginalStrings=list(set(errorDataRAW) - set(errorData))
        for replace_str in OriginalStrings:  # String içerisinde ki özel değişkenlerimizi, _STR_ ile değiştiriyoruz
            errorLine = errorLine.replace(replace_str, "_STR_")

        distance = []
        for i in data:  # textdistance ye göre data değişkenlerinin hatalı koda göre uzaklıkları hesaplandı ve bir listeye atandı
            distance.append(
                textdist.ratcliff_obershelp.distance(i, errorLine))  # jaccard,ratcliff_obershelp,sqrt_ncd,tversky
        _, data = zip(*sorted(zip(distance, data),
                              reverse=False))  # hata mesajları ve uzaklıkları ilişkilendirilerek knn algoritması için uzunluklar küçükten büyüğe doğru sıralandı
        # ve sıralı data değişkeni tekrar data değişkenine aktarıldı.
        knnList = []
        for i in range(
                5):  # kNN algoritması için sıralanan data listesinin ilk 5 üyesi \n ve soldaki boşluk ve tab karakterlerinden temizlendi.
            # ardından tokenlerine ayrılıp iki boyutlu bir dizi olarak prefixList e eklendi.
            tokens = self.token(data[i].replace("\n", "").strip())
            knnList.append(tokens)

        valListDict = {}
        maxVal = -100
        selectedList = []
        errorList = []
        for i in knnList:
            aln = alignment.needle(errorData,
                                   i)  # Hatalı datamız ile kNN çıktılarının Gen alignment algorintmasını çalıştırdık.
            identity = aln[0]
            score = aln[1]
            if score * identity > maxVal:
                maxVal = score * identity
                selectedList = aln[3]
                errorList = aln[2]

            if len(aln[2]) not in valListDict.keys():
                valListDict[len(aln[2])] = [aln[2], [aln[3]], [score]]
            else:
                valListDict[len(aln[2])][1].append(aln[3])
                valListDict[len(aln[2])][2].append(score)

        if selectedList.count("-") > 0:
            selectedList = list(map(lambda x: x.replace('-', ''), selectedList))
            selectedList = list(filter(None, selectedList))

        result_list = prepare_output.my_alliagment_fonc(selectedList, errorList, self.listed_python_data,
                                                        OriginalStrings)
        returnString = self.prepare_return_string(result_list)
        returnString = self.false_answer_check(returnString)
        self.returnData.append(returnString)
        return self.returnData

    def false_answer_check(self, returnString):

        if ((returnString.count("_STR_") > 0) or
                (returnString.count("_NUM_") > 0) or
                (returnString.count("- -") > 0)):
            returnString = "# " + self.text[self.line].replace("\r", "")
            return returnString

        return returnString


a = checkError()