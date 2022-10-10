import os
import sys
import platform
from PyQt5.QtWidgets import QAction, QApplication, QFrame

from PyQt5 import Qsci
from PyQt5.Qsci import QsciScintilla, QsciLexerPython, QsciAPIs
from PyQt5.QtGui import QFont, QFontMetrics, QColor, QPixmap, QMouseEvent
from PyQt5.Qt import Qt

from PyQt5.QtCore import pyqtSignal, QUrl

import re

from runthread import RunThread
from configuration import Configuration

import random
import time
import itertools

#Html dosyalarını açmak için gerekli mödülleri ve anahtar listesi için gerekli json modülünü yükle
from PyQt5.QtWebEngineWidgets import QWebEngineView
from Components.TopMenu.Help.glplicense import GPLDialog
import json

#Parantez vb. listesini tutmak için stack
from collections import deque

#Loglama için QsciAPI sınıfını tekrar tanımla
class QsciAPIs(QsciAPIs):
    
    autocompletelogsignal = pyqtSignal(str)
    
    def __init__(self, lexer):
        super().__init__(lexer)
        self.autocompletelogsignal.connect(self.parent().editor().messenger)
        
    def autoCompletionSelected(self, sel):
        super().autoCompletionSelected(sel)
        self.autocompletelogsignal.emit("Autocomplete: " + sel)
####

#######################################


class PythonLexer(QsciLexerPython):
    def __init__(self):
        super().__init__()

    def keywords(self, index):
        keywords = QsciLexerPython.keywords(self, index) or ''
        if index == 1:
            return 'self ' + ' super ' + keywords


######################################


class CodeEditor(QsciScintilla):

    comment_string = "#"
    line_ending = "\n"
    def __init__(self, parent=None):
        super().__init__(parent)
        # self.setAcceptDrops(True)
        self.c = Configuration()
        self.initUi(parent= parent)
        
        #Autocomplete renk değişimi
        self.setStyleSheet("background-color:#D3EBFF")
        
        #Indicator click func
        self.indicatorReleased.connect(self.onIndicatorReleased)
        #Indicator değerlerinin listesini yükle
        keyValJsonPath = self.c.getHomeDir() + self.c.getHtmlHelpPath("html_help_path") + "HelpKeyValueList.json"
        with open(keyValJsonPath, 'r', encoding = "utf-8") as jsonFile:
            self.valueList = json.loads(jsonFile.read())
        #Indicator uygulanan kelimelerin indexlerinin listesi.
        self.wordDict = {}

    def initUi(self,parent):
        self.filename = None
        # self.fileBrowser = None
        self.mainWindow = parent
        self.debugging = False
        c = Configuration()
        self.pointSize = int(c.getFontSize())
        self.tabWidth = int(c.getTab())

        # Scrollbars
        self.verticalScrollBar().setObjectName("codeEditorScroolBarV")
        self.horizontalScrollBar().setObjectName("codeEditorScroolBarH")

        # matched / unmatched brace color ...
        self.setMatchedBraceBackgroundColor(QColor('#ffffff'))
        self.setMatchedBraceForegroundColor(QColor('green'))
        self.setUnmatchedBraceBackgroundColor(QColor('#ffffff'))
        self.setUnmatchedBraceForegroundColor(QColor('red'))

        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)

        # edge mode ... line at 79 characters
        self.setEdgeColumn(79)
        # self.setEdgeMode(1)
        # self.setEdgeColor(QColor('blue'))

        # Set the default font
        self.font = QFont()

        self.font.setFamily(self.c.getCodeFont())

        self.font.setFixedPitch(True)
        self.font.setPointSize(self.pointSize)
        # self.setFont(self.font)
        self.setMarginsFont(self.font)
        #
        # Margin 0 is used for line numbers
        fontmetrics = QFontMetrics(self.font)
        self.setMarginsFont(self.font)
        self.setMarginWidth(0, fontmetrics.width("0000")-self.tabWidth)
        self.setMarginLineNumbers(0, True)
        self.setMarginsBackgroundColor(QColor("#CAD7E0"))
        self.setMarginsForegroundColor(QColor("#6b899f"))
        #
        # Margin 1 for breakpoints
        self.setMarginSensitivity(1, True)
        self.setMarginWidth(1, fontmetrics.width("00"))
        self.markerDefine(QsciScintilla.RightArrow, 8)
        self.setMarkerBackgroundColor(QColor('#ff0000'), 8)

        # variable for breakpoint
        self.breakpoint = False
        self.breakpointLine = None

        # FoldingBox
        # self.setFoldMarginColors(QColor('#C0C0C0'), QColor('#C0C0C0'))

        # CallTipBox
        self.setCallTipsForegroundColor(QColor('#505050'))
        self.setCallTipsBackgroundColor(QColor('#f1e472'))
        self.setCallTipsHighlightColor(QColor('#ff0000'))
        self.setCallTipsStyle(QsciScintilla.CallTipsContext)
        self.setCallTipsPosition(QsciScintilla.CallTipsBelowText)
        self.setCallTipsVisible(0)

        # change caret's color
        # self.SendScintilla(QsciScintilla.SCI_SETCARETFORE, QColor('#98fb98'))
        self.setCaretWidth(2)

        # tab Width
        self.setIndentationsUseTabs(False)
        self.setTabWidth(self.tabWidth)
        # use Whitespaces instead tabs
        self.SendScintilla(QsciScintilla.SCI_SETUSETABS, False)
        # utf-8 kodlamayı kullan (linuxta türkçe karakter için)
        self.SendScintilla(QsciScintilla.SCI_SETCODEPAGE, 65001)
        self.setAutoIndent(True)
        self.setTabIndents(True)

        # BackTab
        self.setBackspaceUnindents(True)

        # Current line visible with special background color or not :)
        # self.setCaretLineVisible(False)
        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(QColor("#e8e8ff"))#imleç satırını renklendir.
        self.setMinimumSize(300, 300)

        # get style
        self.style = None

        # Call the Color-Function: ...
        self.setPythonStyle()

        # self.SendScintilla(QsciScintilla.SCI_SETHSCROLLBAR, 0)

        # Contextmenu
        self.setContextMenuPolicy(Qt.ActionsContextMenu)
        undoAction = QAction("Geri Al", self)
        undoAction.triggered.connect(self.undoContext)
        redoAction = QAction("İleri Al", self)
        redoAction.triggered.connect(self.redoContext)
        sepAction1 = QAction("", self)
        sepAction1.setSeparator(True)
        cutAction = QAction("Kes", self)
        cutAction.triggered.connect(self.cutContext)
        copyAction = QAction("Kopyala", self)
        copyAction.triggered.connect(self.copyContext)
        pasteAction = QAction("Yapıştır", self)
        pasteAction.triggered.connect(self.pasteContext)
        sepAction2 = QAction("", self)
        sepAction2.setSeparator(True)
        sepAction3 = QAction("", self)
        sepAction3.setSeparator(True)
        selectAllAction = QAction("Tümünü Seç", self)
        selectAllAction.triggered.connect(self.getContext)
        sepAction4 = QAction("", self)
        sepAction4.setSeparator(True)
        breakpointAction = QAction("Gereksiz Kod Analizi", self)
        breakpointAction.triggered.connect(self.breakpointContext)
        terminalAction = QAction("Terminal Aç", self)
        terminalAction.triggered.connect(self.termContext)
        commentUncommentAction = QAction("Yorum işareti ekle/sil                 Ctrl+K", self)
        commentUncommentAction.triggered.connect(self.commentUncommentContext)


        self.addAction(undoAction)
        self.addAction(redoAction)
        self.addAction(sepAction1)
        self.addAction(cutAction)
        self.addAction(copyAction)
        self.addAction(pasteAction)
        self.addAction(sepAction2)
        self.addAction(selectAllAction)
        self.addAction(sepAction3)
        self.addAction(breakpointAction)
        self.addAction(sepAction4)
        self.addAction(terminalAction)
        self.addAction(commentUncommentAction)

        # signals
        self.SCN_FOCUSIN.connect(self.onFocusIn)
        self.textChanged.connect(self.onTextChanged)
        self.marginClicked.connect(self.onMarginClicked)

    def onFocusIn(self):
        self.mainWindow.refresh(self)
        
    #Linke tıklandığı zaman tıklanan pozisyonu kelimeler listesindeki pozisyonlarla karşılaştır
    def onIndicatorReleased(self, line, index, keys):
        position = self.positionFromLineIndex(line, index)
        
        for key, value in reversed(self.wordDict.items()):#Key kelimenin pozisyonunu veriyor(int), value ise kelimenin kendisini(string)
            if(key <= position and value in self.valueList):#valuelist'te olmayan kelimelere tıklayınca bir şey yapma
                c = Configuration()
                view = QWebEngineView()
                dosyaPath = c.getHomeDir() + c.getHtmlHelpPath("html_help_path")
                dosyaPath =  ( "" if (c.getSystem()=="windows") else "file://" ) + dosyaPath + self.valueList[value]
                view.load(QUrl(dosyaPath))
                
                dialog = GPLDialog(self.parent, view)
                dialog.exec_()
                break

    def onTextChanged(self):
        if self.parent.isNewPythonFile is not True:
            notebook = self.mainWindow.notebook
            textPad = notebook.currentWidget()
            index = notebook.currentIndex()
            if index != 0:
                if self.debugging is True:
                    self.mainWindow.statusBar.showMessage('Kod Editördeki  satırları silerseniz veya değiştirirseniz Kod Ekranını güncellemeyi unutmayın!', 3000)

                if textPad == None:
                    return

                if textPad.filename:
                    if not '*' in notebook.tabText(index):
                        fname = os.path.basename(textPad.filename)
                        fname += '*'
                        notebook.setTabText(index, fname)

                else:
                    fname = notebook.tabText(index)
                    fname += '*'

                    if not '*' in notebook.tabText(index):
                        notebook.setTabText(index, fname)
            else:
                if not '*' in notebook.tabText(index):
                    fname = os.path.basename(textPad.filename)
                    fname += '*'
                    notebook.setTabText(index, fname)

        #Indicator fonksiyonunu çalıştır
        self.indicatorFill()

    def setText(self, text):
        super().setText(text)
        self.indicatorFill()

    def indicatorFill(self):
        mainText = self.text().encode("utf-8")
    
        self.indicatorDefine(self.RoundBoxIndicator, 0)
        self.setIndicatorForegroundColor(QColor("#acd33b"), 0)
        self.setIndicatorHoverForegroundColor(QColor("#00acea"), 0)
        self.setIndicatorDrawUnder(True)
        self.SendScintilla(self.SCI_SETINDICATORCURRENT, 0)
        self.SendScintilla(self.SCI_INDICATORCLEARRANGE, 0, len(mainText))
        
        for key in self.valueList:
            keyU = key.encode("utf-8")
            pos = mainText.find(keyU)
            while(pos != -1 and pos < len(mainText)):
                self.wordDict[pos] = key
                self.SendScintilla(self.SCI_INDICATORVALUEAT, 0, pos)
                self.SendScintilla(self.SCI_INDICATORFILLRANGE, pos, len(keyU))
                pos += len(keyU)
                pos = mainText.find(keyU, pos)
                pos = int(pos)

        #Kapanmayan parantez vb. karakterlerin altını çiz
        paranthOpen, paranthClose = self.findUnmatched("(", ")")
        bracketOpen, bracketClose = self.findUnmatched("[", "]")
        squaredbOpen, squaredbClose = self.findUnmatched("{", "}")

        resText = self.OpenBracketsMessage(paranthOpen, bracketOpen, squaredbOpen)
        resText += self.CloseBracketsMessage(paranthClose, bracketClose, squaredbClose)

        
        self.SendScintilla(self.SCI_SETINDICATORCURRENT, 2)
        self.SendScintilla(self.SCI_INDICATORCLEARRANGE, 0, len(mainText))
        self.indicatorDefine(self.SquiggleIndicator, 2)
        self.setIndicatorForegroundColor(QColor("#ff0000"), 2)
        self.setIndicatorHoverForegroundColor(QColor("#ff0000"), 2)
        self.setIndicatorDrawUnder(True)
        self.mainWindow.statusBar.setStyleSheet("")
        self.mainWindow.statusBar.showMessage('', 1)
        for i in itertools.chain(paranthOpen, paranthClose, bracketOpen, bracketClose, squaredbClose, squaredbOpen):
            self.SendScintilla(self.SCI_INDICATORFILLRANGE, i, 1)
            self.mainWindow.statusBar.setStyleSheet("QStatusBar{padding-left:8px;background:rgba(255,0,0,255);color:white;font-weight:bold;}")
            self.mainWindow.statusBar.showMessage(resText, 3000)
        mainText = self.text().encode("utf-8")
		#tek tırnaklar kapatılmış mı hesapla
        singleQuotaIndex=[i for i in range(len(mainText)) if mainText.startswith(b"'", i) and self.SendScintilla(self.SCI_GETSTYLEAT, i) != 1]
        singleQuotaIndexEscaped=[i+1 for i in range(len(mainText)) if mainText.startswith(b"\\'", i)] # \ işaretinin posizyonunu verdiği için +1 ekledik
        doubleQuotaIndex=[i for i in range(len(mainText)) if mainText.startswith(b'"', i) and self.SendScintilla(self.SCI_GETSTYLEAT, i) != 1]
        doubleQuotaIndexEscaped=[i+1 for i in range(len(mainText)) if mainText.startswith(b'\\"', i)] # \ işaretinin posizyonunu verdiği için +1 ekledik

        singleQuotaIndex=list(set(singleQuotaIndex)-set(singleQuotaIndexEscaped)) #escape edilmiş ' işaretini listeden çıkar
        doubleQuotaIndex=list(set(doubleQuotaIndex)-set(doubleQuotaIndexEscaped)) #escape edilmiş " işaretini listeden çıkar

		
        #eğer QuotaIndex tek sayıda elemandan oluşuyorsa listedeki en son indisli elemanın altını çizsin.
        if(len(singleQuotaIndex) % 2 == 1):
            self.SendScintilla(self.SCI_INDICATORFILLRANGE, max(singleQuotaIndex), 1)
            self.mainWindow.statusBar.setStyleSheet("QStatusBar{padding-left:8px;background:rgba(255,0,0,255);color:white;font-weight:bold;}")
            self.mainWindow.statusBar.showMessage('Tek Tırnak kapatılmadı!', 3000)
        if(len(doubleQuotaIndex) % 2 == 1):
            #print(doubleQuotaIndex)
            self.SendScintilla(self.SCI_INDICATORFILLRANGE, max(doubleQuotaIndex), 1)
            self.mainWindow.statusBar.setStyleSheet("QStatusBar{padding-left:8px;background:rgba(255,0,0,255);color:white;font-weight:bold;}")
            self.mainWindow.statusBar.showMessage('Çift Tırnak kapatılmadı!', 3000)
    
    def findUnmatched(self, openChar, closeChar):

        mainText = self.text().encode("utf-8")
        openParanthList = deque()
        closeParanthList = deque()
        
        for i, val in enumerate(mainText):
            x = self.SendScintilla(self.SCI_GETSTYLEAT, i)
            if(x == 1):#1 -> yorum için kullanılan stil numarası
                continue
            
            char = chr(val)
            
            if(char == openChar):
                openParanthList.append(i)
            elif(char == closeChar):
                if(len(openParanthList) == 0):
                    closeParanthList.append(i)
                else:
                    openParanthList.pop()
        
        return (openParanthList, closeParanthList)

    def onMarginClicked(self, margin, line, modifiers):

        if self.markersAtLine(line) != 0:
            self.markerDelete(line, 8)
            self.breakpoint = False
            self.breakpointLine = None
            self.mainWindow.statusBar.showMessage('Hata Ayıklayıcı Silindi', 3000)
        else:
            if self.breakpoint == False:
                self.markerAdd(line, 8)
                self.breakpoint = True
                self.breakpointLine = line + 1
                self.mainWindow.statusBar.showMessage('Hata ayıklayıcı atandı ' + \
                                                      str(self.breakpointLine), 3000)


    def checkPath(self, path):
        if '\\' in path:
            path = path.replace('\\', '/')
        return path


    def undoContext(self):
        self.resetBreakpoint()
        self.undo()

    def redoContext(self):
        self.resetBreakpoint()
        self.redo()

    def cutContext(self):
        self.resetBreakpoint()
        self.cut()

    def copyContext(self):
        self.resetBreakpoint()
        self.copy()

    def pasteContext(self):
        self.resetBreakpoint()
        self.paste()

    def getContext(self):
        self.selectAll()

    def breakpointContext(self):
        # Vulture kullanımı için eklendi.
        codeView = self.mainWindow.codeView
        codeView.onCode()

        # code = ''
        # lines = self.lines()
        #
        # c = Configuration()
        # system = c.getSystem()
        #
        # if self.breakpointLine:
        #     for i in range(lines):
        #         if i < self.breakpointLine:
        #             code += self.text(i)
        #
        # randomNumber = random.SystemRandom()
        # number = randomNumber.randint(0, sys.maxsize)
        # filename = 'temp_file_' + str(number) + '.py'

        # try:
        #     with open(filename, 'w') as f:
        #         f.write(code)
        #         command = c.getRun(system).format(filename)
        #         thread = RunThread(command)
        #         thread.start()
        #
        # except Exception as e:
        #     print(str(e))
        #
        # finally:
        #     time.sleep(2)
        #     os.remove(filename)

    def termContext(self):
        c = Configuration()
        system = c.getSystem()
        command = c.getTerminal(system)

        thread = RunThread(command)
        thread.start()

    def commentUncommentContext(self):
        self.toggle_commenting()

    def getLexer(self):
        return self.lexer

    def setPythonStyle(self):
        self.style = 'Python'

        # Set Python lexer
        self.setAutoIndent(True)

        #self.lexer = QsciLexerPython()
        self.lexer = PythonLexer()
        self.lexer.setFont(self.font)
        self.lexer.setFoldComments(True)

        # set Lexer
        self.setLexer(self.lexer)

        #self.setCaretLineBackgroundColor(QColor('black'))
        self.lexer.setDefaultPaper(QColor('white'))
        self.lexer.setDefaultColor(QColor('black'))
        self.lexer.setColor(QColor('black'), 0) # default
        self.lexer.setPaper(QColor('white'), -1) # default -1 vor all styles
        self.lexer.setColor(QColor('green'), PythonLexer.Comment)  # = 1
        self.lexer.setColor(QColor('#448AFF'), 2)   # Number = 2
        self.lexer.setColor(QColor('#A60092'), 3)   # DoubleQuotedString
        self.lexer.setColor(QColor('#A60092'), 4)   # SingleQuotedString
        self.lexer.setColor(QColor('#0D47A1'), 5)   # Keyword
        self.lexer.setColor(QColor('gray'), 6)   # TripleSingleQuotedString
        self.lexer.setColor(QColor('gray'), 7)   # TripleDoubleQuotedString
        self.lexer.setColor(QColor('#0D47A1'), 8)   # ClassName
        self.lexer.setColor(QColor('#007f7f'), 9)   # FunctionMethodName
        self.lexer.setColor(QColor('black'), 10)   # Operator
        self.lexer.setColor(QColor('black'), 11)   # Identifier
        self.lexer.setColor(QColor('gray'), 12)   # CommentBlock
        self.lexer.setColor(QColor('green'), 13)   # UnclosedString
        self.lexer.setColor(QColor('gray'), 14)   # HighlightedIdentifier
        self.lexer.setColor(QColor('#5DD3AF'), 15)   # Decorator
        self.setPythonAutocomplete()
        self.setFold()


    def setPythonAutocomplete(self):

        self.autocomplete = QsciAPIs(self.lexer)
        self.keywords = self.lexer.keywords(1)

        self.keywords = self.keywords.split(' ')

        for word in self.keywords:
            self.autocomplete.add(word)
        
        self.autocomplete.add('super')
        self.autocomplete.add('self')
        self.autocomplete.add('__name__')
        self.autocomplete.add('__main__')
        self.autocomplete.add('__init__')
        self.autocomplete.add('__str__')
        self.autocomplete.add('__repr__')

        self.autocomplete.prepare()

        ## Set the length of the string before the editor tries to autocomplete
        self.setAutoCompletionThreshold(1)

        ## Tell the editor we are using a QsciAPI for the autocompletion
        self.setAutoCompletionSource(QsciScintilla.AcsAPIs)

        self.updateAutoComplete()


    def setFold(self):
        # setup Fold Styles for classes and functions ...
        x = self.FoldStyle(self.FoldStyle(4))
        #self.textPad.folding()
        if not x:
            self.foldAll(False)

        self.setFolding(x)
        #self.textPad.folding()


    def unsetFold(self):
        self.setFolding(0)

    def keyReleaseEvent(self, e):
        # feed the autocomplete with the words from editor
        # simple algorithm to do this ... everytime after Enter

        # refresh CodeView
        text = self.text()
        self.updateCodeView(text)

        # if ENTER was hit ... :

        if e.key() == Qt.Key_Return:

            self.updateAutoComplete()

        if e.key() == Qt.Key_Backspace:
            self.resetBreakpoint()

    def resetBreakpoint(self):
        self.markerDeleteAll()
        self.breakpoint = False
        self.breakpointLine = None

    def updateCodeView(self, text=''):
        codeView = self.mainWindow.codeView
        codeViewDict = codeView.makeDictForCodeView(text)
        codeView.updateCodeView(codeViewDict)


    def updateAutoComplete(self, text=None):
        self.autocomplete = QsciAPIs(self.lexer)  # clear all

        #Anahtar kelimeleri "keywords" listesine ata
        self.keywords = self.lexer.keywords(1)
        self.keywords = self.keywords.split(' ')
        
        #"keywords" listesine aşağıdaki kelimeleri ekle
        self.keywords.append('super')
        self.keywords.append('self')
        self.keywords.append('__name__')
        self.keywords.append('__main__')
        self.keywords.append('__init__')
        self.keywords.append('__str__')
        self.keywords.append('__repr__')
        
        #Autocomplete resmini yükle ve 1 no'lu referansa ata.
        #img = QPixmap(":/icon/images/redball.png") #bundan vazgeçiyoruz düzgün çalışmıyor 19.04.2022
        #self.registerImage(1, img) #bundan vazgeçiyoruz düzgün çalışmıyor 19.04.2022

        for word in self.keywords:
            self.autocomplete.add(word)  # redball gösterme
        # -----Call Tip Ekleme------------------------

        autoCompleteListFiles = os.listdir(
            self.c.getHomeDir() + self.c.getHtmlHelpPath("html_help_path") + "/AutoCompleteLists")
        for i in range(len(autoCompleteListFiles)):
            with open(self.c.getHomeDir() + self.c.getHtmlHelpPath("html_help_path") + "/AutoCompleteLists/" +
                      autoCompleteListFiles[i], "r",
                      errors="ignore", encoding="utf-8") as f:
                if i == 0:
                    autoCompleteList = f.read().splitlines()
                else:
                    autoCompleteList += f.read().splitlines()

        # Add the functions to the api
        for s in autoCompleteList:
            self.autocomplete.add(s)
        # ------Call Tip Ekleme sonu------------------------

        if not text:

            firstList = []     # list to edit
            secondList = []    # collect all items for autocomplete

            text = self.text()

            # parse complete text ....
            firstList = text.splitlines()

            for line in firstList:
                if 'def' in line:
                    item = line.strip()
                    item = item.strip('def')
                    item = item.replace(':', '')
                    if not item in secondList:
                        secondList.append(item)
                elif 'class' in line:
                    item = line.strip()
                    item = item.strip('class')
                    item = item.replace(':', '')
                    if not item in secondList:
                        secondList.append(item)


            text = text.replace('"', " ").replace("'", " ").replace("(", " ").replace\
                                (")", " ").replace("[", " ").replace("]", " ").replace\
                                (':', " ").replace(',', " ").replace("<", " ").replace\
                                (">", " ").replace("/", " ").replace("=", " ").replace\
                                (";", " ")

            firstList = text.split('\n')

            for row in firstList:

                if (row.strip().startswith('#')) or (row.strip().startswith('//')):
                    continue

                else:
                    wordList = row.split()

                    for word in wordList:

                        if re.match("(^[0-9])", word):
                            continue

                        elif '#' in word or '//' in word:
                            continue

                        elif word in self.keywords:
                            continue

                        elif (word == '__init__') or (word == '__main__') or \
                             (word == '__name__') or (word == '__str__') or \
                             (word == '__repr__'):
                            continue

                        elif word in secondList:
                            continue

                        elif len(word) > 15:
                            continue

                        elif not len(word) < 3:
                            w = re.sub("{}<>;,:]", '', word)
                            #print(w)
                            secondList.append(w)

            # delete doubled entries
            x = set(secondList)
            secondList = list(x)

            # debugging ...
            #print(secondList)
            
            #for item in firstList: #autocomplete listede hata oluşturuyor.
                #self.autocomplete.add(item) #redball gösterme
                
            for item in secondList:
                self.autocomplete.add(item) #redball gösterme
            
            self.autocomplete.prepare()

    def setPythonPrintStyle(self):
        # Set None lexer
        self.font = QFont()

        self.font.setFamily(self.c.getCodeFont())

        self.font.setFixedPitch(True)
        self.font.setPointSize(10)
        self.setFont(self.font)

        self.lexer = PythonLexer()
        self.lexer.setFont(self.font)
        # set Lexer
        self.setLexer(self.lexer)

        #self.setCaretLineBackgroundColor(QColor('black'))
        self.lexer.setDefaultPaper(QColor('white'))
        self.lexer.setDefaultColor(QColor('black'))
        self.lexer.setColor(QColor('black'), 0)  # default
        self.lexer.setPaper(QColor('white'), -1)  # default -1 vor all styles
        self.lexer.setColor(QColor('green'), PythonLexer.Comment)  # = 1
        self.lexer.setColor(QColor('#448AFF'), 2)  # Number = 2
        self.lexer.setColor(QColor('#A60092'), 3)  # DoubleQuotedString
        self.lexer.setColor(QColor('#A60092'), 4)  # SingleQuotedString
        self.lexer.setColor(QColor('#0D47A1'), 5)  # Keyword
        self.lexer.setColor(QColor('gray'), 6)  # TripleSingleQuotedString
        self.lexer.setColor(QColor('gray'), 7)  # TripleDoubleQuotedString
        self.lexer.setColor(QColor('#0D47A1'), 8)  # ClassName
        self.lexer.setColor(QColor('#007f7f'), 9)  # FunctionMethodName
        self.lexer.setColor(QColor('black'), 10)  # Operator
        self.lexer.setColor(QColor('black'), 11)  # Identifier
        self.lexer.setColor(QColor('gray'), 12)  # CommentBlock
        self.lexer.setColor(QColor('green'), 13)  # UnclosedString
        self.lexer.setColor(QColor('gray'), 14)  # HighlightedIdentifier
        self.lexer.setColor(QColor('#5DD3AF'), 15)  # Decorator
        self.setPythonAutocomplete()
        self.setFold()

        self.setNoneAutocomplete()
        self.unsetFold()

        self.font = QFont()

        self.font.setFamily(self.c.getCodeFont())

        self.font.setFixedPitch(True)
        self.font.setPointSize(self.pointSize)



    def setNoneAutocomplete(self):
        #AutoCompletion
        self.autocomplete = Qsci.QsciAPIs(self.lexer)
        self.autocomplete.clear()

        self.autocomplete.prepare()

        self.setAutoCompletionThreshold(1)
        self.setAutoCompletionSource(QsciScintilla.AcsAPIs)


    def resetPythonPrintStyle(self, lexer):

        self.font = QFont()

        self.font.setFamily(self.c.getCodeFont())

        self.font.setFixedPitch(True)
        self.font.setPointSize(self.pointSize)
        self.setFont(self.font)

        lexer.setFont(self.font)
        # set Lexer
        self.setLexer(lexer)

        # margins reset

        # Margin 0 is used for line numbers
        fontmetrics = QFontMetrics(self.font)
        self.setMarginsFont(self.font)
        self.setMarginWidth(0, fontmetrics.width("0000") + 5)
        self.setMarginLineNumbers(0, True)
        self.setMarginsBackgroundColor(QColor("#000000"))
        self.setMarginsForegroundColor(QColor("#FFFFFF"))

        # FoldingBox
        self.setFoldMarginColors(QColor('blue'), QColor('blue'))

    def keyPressEvent(self, event):
        # Execute the superclasses event
        super().keyPressEvent(event)
        # Check pressed key information
        key = event.key()
        key_modifiers = QApplication.keyboardModifiers()
        if (key == Qt.Key_K and key_modifiers == Qt.ControlModifier):
            self.toggle_commenting()

        self.on_k(event.text())

    def on_k(self, id):
        if self.isReadOnly():
            return

        c = Configuration()
        # 40 ( - 39 ' - 34 " - 91 [ - 123 {
        if c.getAutoCloseOnK():
            # if id == 40:
            if id == "(":
                self.insert(")")
            # elif id == 39:
            elif id == "'":
                self.insert("'")
            # elif id == 34:
            elif id == '"':
                self.insert('"')
            # elif id == 91:
            elif id == "[":
                self.insert(']')
            # elif id == 123:
            elif id == "{":
                self.insert('}')
        #
        if c.getStatusBarOnK():
            line, column = self.getCursorPosition()
            lines = self.lines()
            if not self.mainWindow.statusBar.currentMessage():
                self.mainWindow.statusBar.showMessage("Satır: {0} Sütun: {1}".format(line+1, column))


    def toggle_commenting(self):
        # Check if the selections are valid
        selections = self.get_selections()
        if selections == None:
            return
        # Merge overlapping selections
        while self.merge_test(selections) == True:
            selections = self.merge_selections(selections)
        # Start the undo action that can undo all commenting at once
        self.beginUndoAction()
        # Loop over selections and comment them
        for i, sel in enumerate(selections):
            if self.text(sel[0]).lstrip().startswith(self.comment_string):
                self.set_commenting(sel[0], sel[1], self._uncomment)
            else:
                self.set_commenting(sel[0], sel[1], self._comment)
        # Select back the previously selected regions
        self.SendScintilla(self.SCI_CLEARSELECTIONS)
        for i, sel in enumerate(selections):
            start_index = self.positionFromLineIndex(sel[0], 0)
            # Check if ending line is the last line in the editor
            last_line = sel[1]
            if last_line == self.lines() - 1:
                end_index = self.positionFromLineIndex(sel[1], len(self.text(last_line)))
            else:
                end_index = self.positionFromLineIndex(sel[1], len(self.text(last_line)) - 1)
            if i == 0:
                self.SendScintilla(self.SCI_SETSELECTION, start_index, end_index)
            else:
                self.SendScintilla(self.SCI_ADDSELECTION, start_index, end_index)
        # Set the end of the undo action
        self.endUndoAction()

    def get_selections(self):
        # Get the selection and store them in a list
        selections = []
        for i in range(self.SendScintilla(self.SCI_GETSELECTIONS)):
            selection = (
                self.SendScintilla(self.SCI_GETSELECTIONNSTART, i),
                self.SendScintilla(self.SCI_GETSELECTIONNEND, i)
            )
            # Add selection to list
            from_line, from_index = self.lineIndexFromPosition(selection[0])
            to_line, to_index = self.lineIndexFromPosition(selection[1])
            selections.append((from_line, to_line))
        selections.sort()
        # Return selection list
        return selections

    def merge_test(self, selections):
        """
        Test if merging of selections is needed
        """
        for i in range(1, len(selections)):
            # Get the line numbers
            previous_start_line = selections[i - 1][0]
            previous_end_line = selections[i - 1][1]
            current_start_line = selections[i][0]
            current_end_line = selections[i][1]
            if previous_end_line == current_start_line:
                return True
        # Merging is not needed
        return False

    def merge_selections(self, selections):
        """
        This function merges selections with overlapping lines
        """
        # Test if merging is required
        if len(selections) < 2:
            return selections
        merged_selections = []
        skip_flag = False
        for i in range(1, len(selections)):
            # Get the line numbers
            previous_start_line = selections[i - 1][0]
            previous_end_line = selections[i - 1][1]
            current_start_line = selections[i][0]
            current_end_line = selections[i][1]
            # Test for merge
            if previous_end_line == current_start_line and skip_flag == False:
                merged_selections.append(
                    (previous_start_line, current_end_line)
                )
                skip_flag = True
            else:
                if skip_flag == False:
                    merged_selections.append(
                        (previous_start_line, previous_end_line)
                    )
                skip_flag = False
                # Add the last selection only if it was not merged
                if i == (len(selections) - 1):
                    merged_selections.append(
                        (current_start_line, current_end_line)
                    )
        # Return the merged selections
        return merged_selections

    def set_commenting(self, arg_from_line, arg_to_line, func):
        # Get the cursor information
        from_line = arg_from_line
        to_line = arg_to_line
        # Check if ending line is the last line in the editor
        last_line = to_line
        if last_line == self.lines() - 1:
            to_index = len(self.text(to_line))
        else:
            to_index = len(self.text(to_line)) - 1
        # Set the selection from the beginning of the cursor line
        # to the end of the last selection line
        self.setSelection(
            from_line, 0, to_line, to_index
        )
        # Get the selected text and split it into lines
        selected_text = self.selectedText()
        selected_list = selected_text.split("\n")
        # Find the smallest indent level
        indent_levels = []
        for line in selected_list:
            indent_levels.append(len(line) - len(line.lstrip()))
        min_indent_level = min(indent_levels)
        # Add the commenting character to every line
        for i, line in enumerate(selected_list):
            selected_list[i] = func(line, min_indent_level)
        # Replace the whole selected text with the merged lines
        # containing the commenting characters
        replace_text = self.line_ending.join(selected_list)
        self.replaceSelectedText(replace_text)

    def _comment(self, line, indent_level):
        if line.strip() != "":
            return line[:indent_level] + self.comment_string + line[indent_level:]
        else:
            return line

    def _uncomment(self, line, indent_level):
        if line.strip().startswith(self.comment_string):
            return line.replace(self.comment_string, "", 1)
        else:
            return line

    def OpenBracketsMessage(self, paranthO, bracketO, squaredbO):
        charlist = []
        text = ""
        for i in itertools.chain(paranthO, bracketO, squaredbO):
            charlist.append(chr(self.text().encode("utf-8")[i]))
        charlist = list(set(charlist))

        if len(charlist) != 0 and charlist is not None:
            if len(charlist) > 1:
                text = ", ".join(charlist) +" Parantezlerini kapatınız. "
            else:
                text = charlist[0] + " Parantezini kapatınız. "
        return text

    def CloseBracketsMessage(self, paranthC, bracketC,  squaredbC):
        charlist = []
        text = ""
        for i in itertools.chain(paranthC, bracketC, squaredbC):
            charlist.append(chr(self.text().encode("utf-8")[i]))
        charlist = list(set(charlist))

        if len(charlist) != 0 and charlist is not None:
            if len(charlist) > 1:
                text = ", ".join(charlist) + " Parantezlerinin açma parantezlerini ekleyiniz. "
            else:
                text = charlist[0] +" Parantezinin açma parantezini ekleyiniz. "

        return text
