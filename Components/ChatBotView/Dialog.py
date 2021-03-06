import os
import sqlite3
import tempfile
import enchant
from TurkishStemmer import TurkishStemmer
from Components.ChatBotView.langaware import TurkishStr
from Components.ChatBotView.replace_emoji import areAllEmojis, replaceToEmoji
from trnlp import *

dialogButtons = []
lang = enchant.Dict("en_US")


class Message:
    def __init__(self, otherMessage, userOptions, messageLinks=None):
        self.otherMessage = otherMessage
        self.userOptions = userOptions
        self.messageLinks = messageLinks
        self.prevMessage = None


def getNumLeading(s, char):
    num = 0
    pos = 0
    while pos < len(s) and s[pos] == char:
        num += 1
        pos += 1
    return num


def IntersecOfSets(arr):
    arr = list(filter(None, arr))
    if arr:
        result = set(arr[0])
        for curr in arr[1:]:
            result.intersection_update(curr)
            if result != set():
                return list(result)

        return list(result)
    else:
        return None


def GetSentenceId(conn_cur, words):
    mainList = []
    for word in words:
        query = ("SELECT Id from Dialogs WHERE ' ' || DialogKeyword LIKE \'% {0}%\'").format(word)
        conn_cur.execute(query)
        records = conn_cur.fetchall()
        liste = []
        for Id in records:
            liste.append(Id)
        liste = [item for t in liste for item in t]
        mainList.append(liste)
    commenElemans = IntersecOfSets(mainList)
    if commenElemans is None or len(commenElemans) == 0:
        return None
    return commenElemans[0]


def LoadDialog(sentenceORJ):
    try:
        sentence = ' '.join(cleanStopWords(sentenceORJ))
        if len(sentence) == 1:
            return None

        parentDir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
        connection = sqlite3.connect(parentDir + '/Config/' + 'chatbot-database.db')
        conn_cur = connection.cursor()
        words = wordPreprocessing(sentence)

        if len(words) == 1:
            # 1-Dialog Keywordlere bakılmalı
            new_sentence = cleanStopWords(sentence)
            if len(new_sentence) > 0:
                k = convertToLowercase(new_sentence[0])
                searchedWord = ("SELECT Dialog from Dialogs WHERE DialogKeyword LIKE \'%{0}%\' LIMIT 1").format(k)

                conn_cur.execute(searchedWord)
                sqlite_result = conn_cur.fetchall()

                if len(sqlite_result) > 0:
                    return sqlite_result[0][0].replace('\r\n', '\n')

                else:  # 2-Dialog Keywordlerde bulunamadı butonlara bakılmalı
                    buttonInfo = getButtonId(convertSentenceToLowercase(sentence), words)
                    if buttonInfo is not None:
                        buttonId = buttonInfo[0]
                        sqlite_result = getDialogWithButtonId(conn_cur, buttonId)
                        return sqlite_result
        elif len(words) > 1:
            buttonInfo = getButtonId(convertSentenceToLowercase(sentence), words)
            dialog_result, button_result = None , None
            if buttonInfo is not None:
                buttonId = buttonInfo[0]
                button_result = getDialogWithButtonId(conn_cur, buttonId)
                if buttonInfo[1] > 1:
                    return button_result

            DialogId = GetSentenceId(conn_cur, words)
            if DialogId is not None:
                searchedWord = ("SELECT Dialog from Dialogs WHERE Id LIKE \'%{0}%\'").format(DialogId)
                conn_cur.execute(searchedWord)
                dialog_result = conn_cur.fetchall()
                dialog_result = dialog_result[0][0].replace('\r\n', '\n')

            if dialog_result:
                return dialog_result
            elif button_result:
                return button_result
            else:
                return None

    except Exception as err:
        print("Load Dialog Error: {0}".format(err))


def LoadMessage(word='python2'):
    result = None
    if len(word) > 2:
        isEmoji = areAllEmojis(word)
        if isEmoji:
             result = '.'+replaceToEmoji(word)+';'
        else:
            result = LoadDialog(word)

    if result is not None:
        with tempfile.NamedTemporaryFile(mode="w+t", encoding="utf-8") as fp:
            fp.write(result)
            fp.seek(0)
            root = Message("", [])
            lastMsg = root
            prevLevel = 0
            for line in fp:
                line = line.strip()
                if len(line) == 0:
                    continue
                parts = line.split(";")
                otherMsg = parts[0].strip()
                user = [x.strip() for x in parts[1].split("|")]
                level = getNumLeading(otherMsg, '.')
                newMsg = Message(otherMsg[level:], user)

                if level == prevLevel:
                    newMsg.prevMessage = lastMsg.prevMessage
                    lastMsg.prevMessage.messageLinks.append(newMsg)

                elif level > prevLevel:
                    newMsg.prevMessage = lastMsg
                    if lastMsg.messageLinks is None:
                        lastMsg.messageLinks = [newMsg]
                    else:
                        lastMsg.messageLinks.append(newMsg)

                else:
                    newMsg.prevMessage = lastMsg.prevMessage.prevMessage
                    lastMsg.prevMessage.prevMessage.messageLinks.append(newMsg)
                    nOpts = len(lastMsg.prevMessage.userOptions)
                    nLinks = len(lastMsg.prevMessage.messageLinks)
                    while nOpts > nLinks:
                        lastMsg.prevMessage.messageLinks.append(None)
                        nLinks += 1

                lastMsg = newMsg
                prevLevel = level
            return root.messageLinks[0]
    else:
        return None


def wordPreprocessing(sentence):
    words = cleanStopWords(sentence)
    new_words = words.copy()

    for index, value in enumerate(new_words):
        eleman = convertToLowercase(value)

        stemmer = TurkishStemmer()
        new_words[index] = stemmer.stem(eleman)

    new_words = new_words

    return new_words


def convertToLowercase(word):
    LangStr = TurkishStr
    if word != '' and lang.check(word):
        return word.lower()
    else:
        return LangStr(word).lower()


def convertSentenceToLowercase(sentence):  # köklere bakmadan cümleyi küçük harfe çevirir.
    sentence = sentence.split(' ')
    for index, eleman in enumerate(sentence):
        sentence[index] = convertToLowercase(eleman)
    return ' '.join(sentence)


def sentencePreprocessing(sentence):
    sentence = sentence.split(' ')
    stemmer = TurkishStemmer()
    for index, eleman in enumerate(sentence):
        new_eleman = convertToLowercase(eleman)
        sentence[index] = stemmer.stem(new_eleman)
    return ' '.join(sentence)


def cleanStopWords(text):
    return word_token(text)


def LoadDialogButtons():
    try:

        parentdir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
        conn = sqlite3.connect(parentdir + '/Config/' + 'chatbot-database.db')
        c = conn.cursor()
        LangStr = TurkishStr
        query = ("SELECT Id, Dialog from Dialogs")
        c.execute(query)
        records = c.fetchall()
        count = 0
        for data in records:
            str_data = data[1].split("\n")[:-1]
            for index, i in enumerate(str_data):
                level = getNumLeading(i, ".")
                parts = i.split(";")
                parts[1] = parts[1].strip()

                new_parts = parts[1].split(' | ')

                if len(new_parts) > 0:
                    for index, val in enumerate(new_parts):
                        new_parts[index] = convertToLowercase(val)

                if parts[1] != '':
                    btnTupple = (data[0], level, new_parts)
                    dialogButtons.append(btnTupple)
            count += 1
    except Exception as err:
        print("Error: {0}".format(err))


def getNumLeading(s, char):
    num = 0
    pos = 0
    while pos < len(s) and s[pos] == char:
        num += 1
        pos += 1
    return num


def getDialogWithButtonId(conn_cur, buttonId):
    deleteItem = []
    info = buttonId.split(',')
    id = info[0]
    level = info[1]
    dialog = info[2]
    query = ("SELECT Dialog from Dialogs WHERE Id LIKE \'%{0}%\'").format(id)

    conn_cur.execute(query)
    records = conn_cur.fetchall()
    records = records[0][0].split('\n')
    for i, data in enumerate(records):
        records[i] = data.replace(".", "", int(level))
        if records[i] != '' and records[i][0] != '.':
            deleteItem.append(i)

    indices = deleteItem
    newlist = [i for j, i in enumerate(records) if j not in indices]

    aranan = None
    sayac = -1
    for i in newlist:
        if sayac < int(dialog):
            if i[0:2] != '..':
                if i[0:1] == '.':
                    sayac += 1
                    aranan = i
        else:
            if i[0:2] == '..':
                aranan = aranan + '\n' + i
    return aranan


def concatenateArray(sameLevelButtons):
    new_sameLevelButtons = []
    for a in sameLevelButtons:
        new_sameLevelButtons += a

    return new_sameLevelButtons


def getButtonId(sentence, words):
    try:
        res_words = words.copy()
        dictFound = {}

        for dialog_data in dialogButtons:
            id = dialog_data[0]
            level = dialog_data[1]
            dialog = dialog_data[2]

            for index, buttonText in enumerate(dialog):

                if sentence in buttonText:  # kelime buttonText de olduğu gibi geçiyor, köklere bakmaya gerek yok,
                    sameLevelButtons = [f[2] for f in dialogButtons if f[0] == id and f[1] == level]
                    sira = concatenateArray(sameLevelButtons).index(buttonText)
                    key = ",".join([str(id), str(level), str(sira)])
                    return key, 2  # 1den büyük değer döndürmesi kontrol eden yerler için yeterli

                else:
                    for aranan in res_words:
                        buttonWords = wordPreprocessing(buttonText)
                        for buttonWord in buttonWords:
                            if aranan == buttonWord:
                                sameLevelButtons = [f[2] for f in dialogButtons if f[0] == id and f[1] == level]
                                sira = concatenateArray(sameLevelButtons).index(buttonText)
                                key = ",".join([str(id), str(level), str(sira)])
                                if key in dictFound:
                                    dictFound[key] += 1
                                else:
                                    dictFound[key] = 1

        if dictFound != {}:
            result = max(dictFound, key=dictFound.get)
            return result, dictFound[result]
    except Exception as err:
        print("Error: {0}".format(err))


