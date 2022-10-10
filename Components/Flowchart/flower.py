from PyQt5.QtWidgets import QMainWindow,QFileDialog,QFrame,QHBoxLayout,QWidget,QAction,QToolBar,QStatusBar,QTabWidget,QLabel,QLineEdit,QMessageBox,QDialog,QGridLayout,QRadioButton,QComboBox,QPushButton,QSizePolicy,QSpacerItem
from PyQt5.QtGui import QPixmap, QIcon, QPageSize, QPageLayout, QMovie
from PyQt5.QtWebEngineWidgets import QWebEngineSettings as Settings
from PyQt5.QtWebEngineWidgets import QWebEngineView as Web
from PyQt5.QtCore import Qt, QUrl, QSize, QRect, QTimer
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from os.path import  join, abspath, exists
from subprocess import check_output
from os import environ, makedirs
from platform import system
import tempfile
import ast
import sys
import inspect
from configuration import Configuration
from Components.MessageBox.CustomizeMessageBox import CustomizeMessageBox_Ok

CONDITION = "condition"
OPERATION = "operation"
INPUTOUTPUT = "inputoutput"
PARALLEL = "parallel"
SUBROUTINE = "subroutine"
START = "start"
END = "end"
fnode_id = 0

class CodeflowVisitor(ast.NodeVisitor):

    def __init__(self, source):
        self._source = source
        self._srclines = source.splitlines() 
        self._fnodes = [{"name": START,"type": START,"text": START,"yesno": None}]  
        self._flines = []  
        self._fstack = [{"name": START,"type": START,"text": START,"yesno": None}] 
        super().__init__()

    def _add_fnode(self, nodetype, text, stype=None, soption=None):
        global fnode_id
        fnode_id += 1
        fnode = {"name": nodetype + str(fnode_id),"type": nodetype,"text": text,"stype": stype,"yesno": None}
        self._fnodes.append(fnode)
        lastnode = self._fstack.pop()
        if stype == "for" or stype == "while" or stype == "if":  
            self._add_fline({"from": lastnode,"to": fnode,"yesno": lastnode["yesno"]})
            fnodeNO = fnode.copy()
            fnodeNO["yesno"] = "no"
            fnodeYES = fnode.copy()
            fnodeYES["yesno"] = "yes"
            self._fstack.append(fnodeNO) 
            self._fstack.append(fnodeYES)
        else:
            self._add_fline({"from": lastnode,"to": fnode,"yesno": lastnode["yesno"]})
            self._fstack.append(fnode) 

        return fnode

    def _add_fline(self, dict_fline):
        _from = dict_fline["from"]
        _to = dict_fline["to"]
        if _from["type"] == CONDITION and _from["yesno"] == "terminal":
            for fnode in _from["terminal"]:
                yesno = fnode["yesno"]
                if yesno not in ["yes", "no"]:
                    yesno = None
                self._flines.append({"from": fnode, "to": _to, "yesno": yesno})
        else:
            self._flines.append(dict_fline)

    def _end_statement(self, stype, yesno=None):
        if stype == "for" or stype == "while":
            lastnode = self._fstack.pop()  
            fornode = self._fstack[-1]  
            lineyesno = lastnode["yesno"]
            if not lineyesno:
                lineyesno = "left"  
            self._add_fline({"from": lastnode,"to": fornode,"yesno": lineyesno}) 
        elif stype == "if":
            if yesno == "terminal":
                ifnode = self._fstack[-1]
                ifnode["yesno"] = "terminal" 
                return
            lastnode = self._fstack.pop()
            ifnode = self._fstack[-1]
            if yesno == "yes" or yesno == "no": 
                self._put_terminal_node(lastnode, ifnode)
            if yesno == "yes":
                self._fstack.append(ifnode) 

        elif stype == "prog":
            endnode = {"name": END, "type": END, "text": END}
            lastnode = self._fstack.pop() 
            self._fnodes.append(endnode)
            self._add_fline({"from": lastnode,"to": endnode,"yesno": lastnode["yesno"]}) 

    def _put_terminal_node(self, lastnode, ifnode):
        if not "terminal" in ifnode:
            ifnode["terminal"] = []
        if lastnode["yesno"] != "terminal":
            ifnode["terminal"].append(lastnode) 
        else:
            ifnode["terminal"] += lastnode["terminal"] 

    def _get_outter_node(self, stypes: list):
        i = len(self._fstack) - 1
        while True:
            if self._fstack[i]["stype"] in stypes:
                break
            i -= 1
            if i < 0:
                return None 
        return self._fstack[i]          

    def dovisit(self, with_explain=False):
        str_text = self.visit(ast.parse(self._source))
        self._end_statement("prog") 
        str_flowchart = "\n" 
        for fnode in self._fnodes:
            str_flowchart += f'{fnode["name"]}=>{fnode["type"]}: {fnode["text"]}'
            if fnode["text"].startswith("for ") or fnode["text"].startswith(
                    "while "):
                str_flowchart += '|past'
            str_flowchart += '\n'
        for fline in self._flines:
            str_flowchart += f'{fline["from"]["name"]}'
            if fline["yesno"]:
                str_flowchart += f'({fline["yesno"]})'
            str_flowchart += f'->{fline["to"]["name"]}\n'
        str_flowchart += "\n"  #```
        return (str_text if with_explain else "") + str_flowchart

    def _parse_symbols(self, val: str) -> str:
        return val

    def get_node_source(self, node):
        if not node:
            return ""
        if isinstance(node, str):
            return node
        if not hasattr(node, "lineno"):
            return str(node)
        line0 = node.lineno - 1
        c0 = node.col_offset
        line1 = node.end_lineno - 1
        c1 = node.end_col_offset
        src = ""
        if line0 == line1:
            src = self._srclines[line0][c0:c1]
        else:
            scr = self._srclines[line0][c0] + "\n"
            for n in range(line0 + 1, line1):
                src += self._srclines[n] + "\n"
            src += self._srclines[line1][:c1]
        return src

    def generic_visit(self, node, addfnode=True):
        if not hasattr(node, "lineno"):
            return str(node)
        src = self.get_node_source(node)
        if addfnode:
            ftype = OPERATION
            if "input(" in src or "print(" in src or "write(" in src or "read(" in src:
                ftype = INPUTOUTPUT
            self._add_fnode(ftype, src)
        return src

    def visit_Module(self, node):
        s = ""
        for n in node.body:
            src = self.get_node_source(n)
            s += self.visit(n)
        return s

    def visit_FunctionDef(self, node):
        name_str = r'函数 ' + str(node.name) + ' '
        arg_strs = [self._parse_symbols(str(arg.arg)) for arg in node.args.args]  

        body_str = ""
        for i in range(len(node.body)):
            body_str += " " + self.visit(node.body[i])
        return name_str + '(' + ', '.join(arg_strs) + r') 的流程： ' + body_str

    def visit_If(self, node):
        explain = r' 判断:'

        while isinstance(node, ast.If):
            cond_str = self.generic_visit(node.test, addfnode=False)
            cfnode = self._add_fnode(CONDITION, "if " + cond_str, "if")
            true_str = ""
            for n in node.body:
                true_str += " " + self.visit(n)
            self._end_statement("if", "yes")
            explain += r' 如果 ' + cond_str + r' 则 ' + true_str
            if node.orelse:
                node = node.orelse
            else:
                node = None
                break
        if node:
            false_str = ""
            if hasattr(node, '__iter__'):
                for n in node:
                    false_str += " " + self.visit(n)
            else:
                false_str += " " + self.visit(node)
            explain += r', 否则 ' + false_str
        else:
            self._add_fnode(OPERATION, "pass", "pass") 
        self._end_statement("if", "no")
        self._end_statement("if", "terminal")
        return explain

    def visit_For(self, node):
        try:
            varname = node.target.id  
            if hasattr(node.iter, "func"):
                func = node.iter.func.id
                args = node.iter.args
                args = [self.visit(arg, False) for arg in args]
                str_for = "for " + varname + " in " + func + "(" + ", ".join(args) + ")"
            else:
                str_for = "for " + varname + " in " + self.generic_visit(node.iter, False)
        except:
            varname = self.get_node_source(node.target)  
            iter_str = self.get_node_source(node.iter)  
            str_for = "for " + varname + " in " + iter_str
        self._add_fnode(CONDITION, str_for, "for")
        str_body = " 执行 "
        for n in node.body:
            str_body = " " + self.visit(n)
        self._end_statement("for")
        return "循环: " + str_for + str_body

    def visit_While(self, node):
        cond_str = self.generic_visit(node.test, addfnode=False)
        cfnode = self._add_fnode(CONDITION, "while " + cond_str, "while")
        str_body = " 执行 "
        for n in node.body:
            str_body = " " + self.visit(n)
        self._end_statement("while")
        return "循环: while " + cond_str + str_body

    def visit_Break_notwork(self, node):   
        fnode = self._add_fnode(OPERATION, "break", "break")
        outter = self._get_outter_node(["for", "while"]) 
        outter["yesno"] = "no" 
        self._put_terminal_node(fnode,  outter)
        return "break"

    def visit_Assign(self, node):
        return self.generic_visit(node)

    def visit_Expr(self, node):
        if isinstance(node.value, ast.Call) or isinstance(node.value, ast.Assign):
            return self.generic_visit(node.value)
        return self.generic_visit(node)

    def visit_Name(self, node):
        return node.id

    def visit_Pass(self, node):
        return self.generic_visit(node)

    def visit_Return(self, node):
        return self.generic_visit(node)


def get_flowchart(fn, with_explain=False):
    if isinstance(fn, str):
        source = fn
    else:
        source = inspect.getsource(fn)
    return CodeflowVisitor(source).dovisit(with_explain)


class LoadingMessageBox(QMessageBox):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        movie = QMovie(":/icon/images/loading.gif")
        label_gif = QLabel(self)
        label_gif.setMovie(movie)
        label_gif.setAlignment(Qt.AlignCenter)
        label_gif.setGeometry(QRect(18, 0, 205, 20))
        label_text = QLineEdit("Akış Şeması Düzenleniyor", self)
        label_text.setReadOnly(True)
        label_text.setGeometry(QRect(68, 110, 195, 25))
        label_text.setAlignment(Qt.AlignCenter)
        label_text2 = QLineEdit("Lütfen bekleyiniz...", self)
        label_text2.setReadOnly(True)
        label_text2.setGeometry(QRect(68, 135, 185, 25))
        label_text2.setAlignment(Qt.AlignCenter)
        movie.start()
        movie.setSpeed(250)
        movie.setPaused(False)
        self.setStyleSheet("QLineEdit{border:none; background-color:transparent}QMessageBox{opacity: 0;border: 10px solid #00ff88;background-color: #ffff88;border-radius:10px;}QLabel{margin: 10px 10px;font-size: 12pt;height: 110px; min-height: 110px; max-height: 110px; width: 255px; min-width: 255px; max-width: 255px;}QPushButton{background-color: #00aaff;color: white;font-size: 12pt;padding: 5px 18px 5px 18px;text-align: center;text-decoration: none;display: inline-block;margin: 4px 2px;border-radius: 7px;}QPushButton:hover {background: #58c1e7;}")
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)
        self.setStandardButtons(QMessageBox.NoButton)


class GetPageSize(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Sayfa Düzenlemesi")
        self.setWindowIcon(QIcon(QPixmap(":/icon/images/startflow.png")))
        self.resize(375, 292)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setMinimumSize(QSize(375, 0))
        self.setMaximumSize(QSize(375, 16777215))
        self.setStyleSheet("QDialog{background-color: #CAD7E0;}QPushButton {min-width:70px;width:70px; color: white;padding: 5px;font-size: 14px;margin: 4px 2px;border-radius: 4px; background-color: rgb(0, 170, 255);}QPushButton::hover{background-color:rgb(4, 124, 184)}")
        self.glay1 = QGridLayout(self)
        self.paperlab = QLabel(self)
        self.frame = QFrame(self)
        self.hlay = QHBoxLayout(self.frame)
        self.okbut = QPushButton("Tamam",self.frame)
        self.frame_2 = QFrame(self)
        self.glay2 = QGridLayout(self.frame_2)
        self.sizelab = QLabel("Kağıt Boyutu:",self.frame_2)
        self.sizeBox = QComboBox(self.frame_2)
        self.directlab = QLabel("Kağıt Yönü:",self.frame_2)
        self.horrad = QRadioButton("Yatay",self.frame_2)
        self.verrad = QRadioButton("Dikey",self.frame_2)
        self.cancelbut = QPushButton("İptal",self.frame)
        self.hlay.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.glay1.addItem(QSpacerItem(158, 20, QSizePolicy.Expanding, QSizePolicy.Minimum), 1, 2, 1, 1)
        self.glay1.addItem(QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Expanding), 0, 1, 1, 1)
        self.glay1.addItem(QSpacerItem(158, 68, QSizePolicy.Expanding, QSizePolicy.Minimum), 1, 0, 1, 1)
        self.glay1.addItem(QSpacerItem(20, 31, QSizePolicy.Minimum, QSizePolicy.Expanding), 2, 1, 1, 1)
        self.glay1.addWidget(self.paperlab, 1, 1, 1, 1)
        self.glay1.addWidget(self.frame, 4, 1, 1, 2)
        self.glay1.addWidget(self.frame_2, 3, 0, 1, 3)
        self.glay2.addWidget(self.sizelab, 0, 0, 1, 1)
        self.glay2.addWidget(self.sizeBox, 0, 1, 1, 2)
        self.glay2.addWidget(self.directlab, 1, 0, 1, 1)
        self.glay2.addWidget(self.horrad, 1, 1, 1, 1)
        self.glay2.addWidget(self.verrad, 1, 2, 1, 1)
        self.hlay.addWidget(self.okbut)
        self.hlay.addWidget(self.cancelbut)
        self.sizeBox.addItem("A0")
        self.sizeBox.addItem("A1")
        self.sizeBox.addItem("A2")
        self.sizeBox.addItem("A3")
        self.sizeBox.addItem("A4")
        self.sizeBox.addItem("B0")
        self.sizeBox.addItem("B1")
        self.sizeBox.addItem("B2")
        self.sizeBox.addItem("B3")
        self.sizeBox.addItem("B4")
        self.verrad.setChecked(True)
        self.sizeBox.setCurrentIndex(4)
        self.paperorientation()
        self.verrad.clicked.connect(self.paperorientation)
        self.horrad.clicked.connect(self.paperorientation)
        self.okbut.clicked.connect(self.accept)
        self.cancelbut.clicked.connect(self.reject)
        
    def paperorientation(self):
        if(self.horrad.isChecked()):
            self.paperlab.setPixmap(QPixmap(":/icon/images/x.png"))
        else:
            self.paperlab.setPixmap(QPixmap(":/icon/images/y.png"))


class FlowchartMaker(QMainWindow):

    def __init__(self,source=''):
        super(FlowchartMaker, self).__init__()
        self.loading = LoadingMessageBox()
        self.papersize = GetPageSize()
        self.pagelay= QPageLayout()
        self.pagewidth = 0
        self.pageheight = 0
        self.source = source
        self.mainWid = QWidget(self)
        self.horLay = QHBoxLayout(self.mainWid)
        self.view = QFrame(self.mainWid)
        self.tabWidget = QTabWidget(self.view)
        self.horLay_2 = QHBoxLayout(self.view)
        self.chartStatus = QStatusBar(self)
        self.toolBar = QToolBar(self)
        self.savebut = QAction(self, icon=QIcon(QPixmap(":/icon/images/savefile.png")))
        self.magnifyplus = QAction(self, icon=QIcon(QPixmap(":/icon/images/zoom_in.png")))
        self.magnifyminus = QAction(self, icon=QIcon(QPixmap(":/icon/images/zoom_out.png")))
        self.defhome = QAction(self, icon=QIcon(QPixmap(":/icon/images/defhome.png")))
        self.grabpage = QAction(self, icon=QIcon(QPixmap(":/icon/images/grab.png")))
        self.printpreview = QAction(self, icon=QIcon(QPixmap(":/icon/images/printicon.png")))
        self.helppage = QAction(self, icon=QIcon(QPixmap(":/icon/images/help.png")))
        self.setWindowIcon(QIcon(QPixmap(":/icon/images/startflow.png")))
        self.setCentralWidget(self.mainWid)
        self.setStatusBar(self.chartStatus)
        self.addToolBar(Qt.TopToolBarArea, self.toolBar)
        self.setWindowTitle("Pynar Akış Şeması")
        self.horLay.setSpacing(0)
        self.horLay_2.setSpacing(0)
        self.horLay.setContentsMargins(0, 0, 0, 0)
        self.horLay_2.setContentsMargins(0, 0, 0, 0)
        self.horLay.addWidget(self.view)
        self.horLay_2.addWidget(self.tabWidget)
        self.view.setMinimumSize(QSize(800, 500))
        self.toolBar.setIconSize(QSize(40, 40))
        self.toolBar.addAction(self.savebut)
        self.toolBar.addAction(self.magnifyplus)
        self.toolBar.addAction(self.magnifyminus)
        self.toolBar.addAction(self.defhome)
        self.toolBar.addAction(self.grabpage)
        self.toolBar.addAction(self.printpreview)
        self.toolBar.addAction(self.helppage)
        self.toolBar.setStyleSheet("QToolBar{ background: #394b58;border:none;spacing:4px;}QToolButton{min-width:45px;min-height:45px;}QToolButton::hover {background: #6b899f; margin-left:2px;margin-bottom:2px;};QToolButton:pressed{background-color: transparent;}")
        self.toolBar.setMovable(False)
        self.savebut.setToolTip("Kaydet.")
        self.defhome.setToolTip("Eski Haline getir.")
        self.grabpage.setToolTip("Sayfayı Sürükle.")
        self.printpreview.setToolTip("Sayfayı Önizle ve Yazdır.")
        self.magnifyplus.setToolTip("Yakınlaştır.")
        self.magnifyminus.setToolTip("Uzaklaştır.")
        self.helppage.setToolTip("Yardım.")
        self.printpreview.setShortcut("Ctrl+P")
        self.magnifyplus.setShortcut("Ctrl++")
        self.savebut.setShortcut("Ctrl+S")
        self.magnifyminus.setShortcut("Ctrl+-")
        self.helppage.setShortcut("Ctrl+H")
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setTabBarAutoHide(False)
        self.tabWidget.setCurrentIndex(-1)
        self.tabWidget.setMovable(False)
        self.savebut.triggered.connect(self.saveFile)
        self.magnifyplus.triggered.connect(lambda: self.browser.setZoomFactor(self.browser.zoomFactor() + 0.1))
        self.magnifyminus.triggered.connect(lambda: self.browser.setZoomFactor(self.browser.zoomFactor() - 0.1))
        self.helppage.triggered.connect(self.helpme)
        self.defhome.triggered.connect(lambda: self.htmlOpener("noGrab"))
        self.grabpage.triggered.connect(lambda: self.htmlOpener("grab"))
        self.printpreview.triggered.connect(self.previewflow)
        self.defhome.setDisabled(True)
        self.helppage.setDisabled(True)
        self.printpreview.setDisabled(True)
        self.grabpage.setDisabled(True)
        self.magnifyminus.setDisabled(True)
        self.magnifyplus.setDisabled(True)
        self.savebut.setDisabled(True)
        self.mainWid.setStyleSheet("QTabWidget::pane { background: transparent;color: white;}QTabBar::tab{height: 0px;width: 0px;}QTabWidget::tab-bar:top {top: 0px;}QTabWidget::tab-bar:bottom {bottom: 0px;}QTabWidget::tab-bar:left {right: 0px;}QTabWidget::tab-bar:right {left: 0px;}QTabBar::tab:selected {color: white;background: #394b58;}QTabBar::tab:!selected {background: transparent;color: white;}QTabBar::tab:!selected:hover {background: #6b899f;color: black;}QTabBar::tab:top:last,QTabBar::tab:bottom:last,QTabBar::tab:top:only-one,QTabBar::tab:bottom:only-one {margin-right: 0;}QTabBar::tab:left:last,QTabBar::tab:right:last,QTabBar::tab:left:only-one,QTabBar::tab:right:only-one {margin-bottom: 0;}")
        self.chartStatus.setStyleSheet("QStatusBar{background-color: rgb(0,96,132);color:white;}")
        self.toolBar.setMinimumHeight(60)
        self.htmlOpener("noGrab")

    def onLoadFinished(self, ok):
        if ok:
            self.browser.page().runJavaScript("document.getElementsByTagName('svg')[0]['clientWidth'];", self.ready1)
            self.browser.page().runJavaScript("document.getElementsByTagName('svg')[0]['clientHeight'];", self.ready2)
            self.browser.page().runJavaScript("document.getElementsByTagName('svg')[0].outerHTML;",self.ready3)

    def ready1(self, width):
        if self.pagewidth == 0:
            self.pagewidth += width

    def ready2(self, height):
        if self.pageheight == 0:
            self.pageheight += height

    def ready3(self, html: str):
        self.tempfilename = tempfile.mktemp(prefix="Flowchart", suffix=".pdf", dir=tempfile.gettempdir())
        if self.papersize != None:
            if self.papersize.verrad.isChecked():
                self.pagelay.setOrientation(QPageLayout.Orientation.Portrait)
            if self.papersize.horrad.isChecked():
                self.pagelay.setOrientation(QPageLayout.Orientation.Landscape)
            self.pagelay.setPageSize(QPageSize(QSize(self.pagewidth, self.pageheight), self.papersize.sizeBox.currentText()))
        else:
            if self.pagewidth > self.pageheight:
                self.pagelay.setOrientation(QPageLayout.Orientation.Landscape)
            else:
                self.pagelay.setOrientation(QPageLayout.Orientation.Portrait)
            self.pagelay.setPageSize(QPageSize(QSize(self.pagewidth, self.pageheight), "A4"))
        self.browser.page().printToPdf(self.tempfilename, pageLayout=self.pagelay)
        jschange = open(Configuration().getHomeDir() + Configuration().getHtmlHelpPath("html_help_path") + 'FlowchartFiles/Pdfpreview/viewer.js', encoding="utf-8").readlines()
        use, tmp = "'use strict';\n","var DEFAULT_URL = '" + self.tempfilename.replace("\\", "/") + "';\n"
        with open(Configuration().getHomeDir() + Configuration().getHtmlHelpPath("html_help_path") + 'FlowchartFiles/Pdfpreview/viewer.js', "w", encoding="utf-8") as f:
            for i in range(0, len(jschange)):
                if i == 0:
                    f.write(use)
                elif i == 1:
                    f.write(tmp)
                else:
                    f.write(jschange[i])
        self.printpreview.setEnabled(True)
        

    def htmlOpener(self, situation):
        self.pagewidth = 0
        self.pageheight = 0
        QTimer.singleShot(1000, lambda: self.loading.done(0))
        sys.argv.append("--disable-web-security")
        self.loading.exec_()
        start, grabcss, grabjs, middle, end = "<!DOCTYPE html><html lang='en'><head><meta charset='utf-8'><style type='text/css'>body{ margin:0px;}.start-element {fill : #d594f4;}.end-element {fill : #00FF55;}.condition-element {fill : #ffa0ea;}.inputoutput-element {fill : #55FFFF;}.operation-element {fill : #FFFF99;}.subroutine-element {fill : #a0e0ff;}.parallel-element {fill : #FFCCFF;}#code{display: none;}::-webkit-scrollbar {display:block;}::-webkit-scrollbar-thumb {border:1px solid #60a0e0;background: #c0e0ff;}::-webkit-scrollbar-thumb:hover {background: #00ffff;}</style>","<style>#canvas { cursor:move; height:100vh;width:100vw;overflow: auto;}::-webkit-scrollbar {width: 0rem;height: 0rem;}#canvas::-webkit-scrollbar { width: 1rem;height: 1rem;}</style>","<script>document.addEventListener('DOMContentLoaded',function () {const ele = document.getElementById('canvas');ele.style.cursor = 'move';let pos = { top: 0,left: 0,x: 0,y: 0};const mouseDownHandler = function (e) {ele.style.cursor = 'move';ele.style.userSelect = 'none';pos = { left: ele.scrollLeft,top: ele.scrollTop,x: e.clientX,y: e.clientY,};document.addEventListener('mousemove',mouseMoveHandler);document.addEventListener('mouseup',mouseUpHandler);};const mouseMoveHandler = function (e) {const dx = e.clientX-pos.x;const dy = e.clientY-pos.y;ele.scrollTop = pos.top-dy;ele.scrollLeft = pos.left-dx;};const mouseUpHandler = function () {ele.style.cursor = 'move';ele.style.removeProperty('user-select');document.removeEventListener('mousemove',mouseMoveHandler);document.removeEventListener('mouseup',mouseUpHandler);};ele.addEventListener('mousedown',mouseDownHandler);});</script>","<script>window.onload = function () {var chart;if (chart) {chart.clean();}chart = flowchart.parse(document.getElementById('code').value);chart.drawSVG('canvas',{'x': 20,'y': 20,'roundness': 5,'arrow-end': 'diamond','line-width': 1,'maxWidth': 80,'line-length': 40,'text-margin': 15,'font-size': 11,'font': 'normal','font-family': 'Arial','font-weight': 'normal','font-color': 'black','line-color': 'black','element-color': 'black','fill': 'white','yes-text': 'Doğru','no-text': 'Yanlış','scale': 1,'symbols': {'start': {'font-color': 'black','element-color': 'green','class': 'start-element'},'end':{'class': 'end-element'},'condition': {'class': 'condition-element'},'inputoutput': {'class': 'inputoutput-element'},'operation': {'class': 'operation-element'},'subroutine': {'class': 'subroutine-element'},'parallel': {'class': 'parallel-element'} },'flowstate' : {'past' : {'fill' : '#CCCCCC','font-size' : 12},'current' : {'fill' : 'yellow','font-color' : 'red','font-weight' : 'bold'},'future' : {'fill' : '#FFFF99'},'request' : {'fill' : 'blue'},'invalid': {'fill' : '#444444'},'approved' : {'fill' : '#58C4A3','font-size' : 12,'yes-text' : 'APPROVED','no-text' : 'n/a'},'rejected' : {'fill' : '#C45879','font-size' : 12,'yes-text' : 'n/a','no-text' : 'REJECTED'} } });};</script></head><body><div><textarea id='code' style='width: 100%;' rows='11'>","</textarea></div><div style='margin-left:20px;' id='canvas'></div></body></html>"
        if self.tabWidget.currentIndex() >= 0:
            self.tabWidget.removeTab(self.tabWidget.currentIndex())
        self.tab = QWidget()
        self.horLay_3 = QHBoxLayout(self.tab)
        self.horLay_3.setContentsMargins(0, 0, 0, 0)
        self.horLay_3.setSpacing(0)
        self.tabWidget.setCurrentIndex(self.tabWidget.count())

        self.isExcept = False

        jsfile = "<script>\n"+ open(Configuration().getHomeDir() + Configuration().getHtmlHelpPath("html_help_path") + 'FlowchartFiles/flowchart.js', encoding="utf-8").read()+ "</script>\n"
        try:
            fc = get_flowchart(self.source).replace(": start", ": Başla").replace(": end", ": Son").replace(": pass", ": Geç")
        except:
            self.isExcept = True
            self.chartStatus.showMessage("Akış Şeması Oluşturulamadı!", 3000)

        if situation == "grab":
            self.browser = Web()
            try:
                self.browser.setHtml(start + grabcss + grabjs + jsfile + middle + fc + end)
                self.chartStatus.showMessage("Akış Şeması Düzenlendi.", 3000)
            except:
                self.chartStatus.showMessage("Akış Şeması Oluşturulamadı!", 3000)
                self.isExcept = True
        if situation == "noGrab":
            self.browser = Web()
            try:
                self.browser.setHtml(start + jsfile + middle + fc + end)
                self.chartStatus.showMessage("Akış Şeması Düzenlendi.", 3000)
            except:
                self.isExcept = True
                self.chartStatus.showMessage("Akış Şeması Oluşturulamadı!", 3000)

        self.horLay_3.addWidget(self.browser)
        self.tabWidget.addTab(self.tab, f"")
        self.browser.loadFinished.connect(self.onLoadFinished)
        self.defhome.setEnabled(True)
        self.grabpage.setEnabled(True)
        self.magnifyminus.setEnabled(True)
        self.magnifyplus.setEnabled(True)
        self.helppage.setEnabled(True)
        self.savebut.setEnabled(True)

    def saveFile(self):
        if self.pagewidth != 0 and self.pageheight != 0:
            dialog = QFileDialog(self)
            dialog.setViewMode(QFileDialog.List)
            plt = system()
            if plt == "Windows":
                documents_dir = join(environ["USERPROFILE"] + "/Documents/PynarKutu/")
            elif plt == "Linux":
                documents_dir = check_output(["xdg-user-dir", "DOCUMENTS"], universal_newlines=True).strip()+ "/PynarKutu"      
            if not exists(documents_dir):
                makedirs(documents_dir)
            filename = dialog.getSaveFileName(self, "Kaydet", documents_dir, "Flowchart Pdf (*.pdf)")
            if filename[0]:
                fullpath = filename[0]
                if self.papersize.exec_():
                    if self.papersize.verrad.isChecked():
                        self.pagelay.setOrientation(QPageLayout.Orientation.Portrait)
                    if self.papersize.horrad.isChecked():
                        self.pagelay.setOrientation(QPageLayout.Orientation.Landscape)
                    self.pagelay.setPageSize(QPageSize(QSize(self.pagewidth, self.pageheight), self.papersize.sizeBox.currentText()))
                else:
                    if self.pagewidth > self.pageheight:
                        self.pagelay.setOrientation(QPageLayout.Orientation.Landscape)
                    else:
                        self.pagelay.setOrientation(QPageLayout.Orientation.Portrait)
                    self.pagelay.setPageSize(QPageSize(QSize(self.pagewidth, self.pageheight), "A4"))
                if not fullpath.endswith(".pdf"):
                    fullpath += ".pdf"
                try:
                    self.browser.page().printToPdf(abspath(fullpath), pageLayout=self.pagelay)
                    self.chartStatus.showMessage(fullpath + " kaydedildi.", 3000)
                except Exception as e:
                    self.chartStatus.showMessage("Akış Şeması kayıt edilemedi !", 3000)
            else:
                self.chartStatus.showMessage("Akış Şeması kayıt edilemedi !", 3000)
        else:
            self.chartStatus.showMessage("Akış Şeması kayıt edilemedi !", 3000)

    def previewflow(self):
        self.preview = PdfPreview()
        self.preview.show()
        self.preview.webView.page().printRequested.connect(self.printflow)

    def printflow(self):
        printer = QPrinter(QPrinter.HighResolution)
        dialog = QPrintDialog(printer, self)
        if dialog.exec_() == QPrintDialog.Accepted:
            self.saveFile()

    def helpme(self):
        self.helpmepage = HelpDialog()
        self.helpmepage.show()


class HelpDialog(QWidget):
    def __init__(self):
        super(HelpDialog, self).__init__()
        self.setWindowTitle("Akış Şeması Yardımı")
        self.resize(1000, 500)
        self.setMinimumSize(QSize(1000, 500))
        self.setWindowIcon(QIcon(QPixmap(":/icon/images/startflow.png")))
        self.horlay2 = QHBoxLayout(self)
        self.horlay2.setSpacing(0)
        self.horlay2.setObjectName("horlay2")
        self.horlay2.setContentsMargins(0, 0, 0, 0)
        self.webView = Web()
        self.horlay2.addWidget(self.webView)
        self.webView.setContextMenuPolicy(Qt.NoContextMenu)
        self.webView.setUrl(QUrl.fromLocalFile(Configuration().getHomeDir() + Configuration().getHtmlHelpPath("html_help_path") + 'FlowchartFiles/Help/Yardim.html'))

class PdfPreview(QWidget):
    def __init__(self):
        super(PdfPreview, self).__init__()
        self.setWindowTitle("Akış Şeması Önizlemesi")
        self.resize(1000, 500)
        self.setMinimumSize(QSize(1000, 500))
        self.setWindowIcon(QIcon(QPixmap(":/icon/images/startflow.png")))
        self.horlay2 = QHBoxLayout(self)
        self.horlay2.setSpacing(0)
        self.horlay2.setObjectName("horlay2")
        self.horlay2.setContentsMargins(0, 0, 0, 0)
        self.webView = Web()
        self.webView.settings().setAttribute(Settings.PluginsEnabled, True)
        self.webView.settings().setAttribute(Settings.PdfViewerEnabled, True)
        self.horlay2.addWidget(self.webView)
        self.webView.setContextMenuPolicy(Qt.NoContextMenu)
        self.webView.setUrl(QUrl.fromLocalFile(Configuration().getHomeDir() + Configuration().getHtmlHelpPath("html_help_path") + 'FlowchartFiles/Pdfpreview/viewer.html'))
