from pathlib import Path
from types import NoneType
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
import sys, os

def _files(path):
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            yield file

class Window(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.opened_file = ""
        self.setWindowTitle("EDocBook")
        self.setWindowIcon(QtGui.QIcon('logo.png'))
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        self.resize(600, 400)
        if not os.path.isdir("notebooks"):
            os.mkdir("notebooks")
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.listwidget = QListWidget()
        self.listwidget.itemDoubleClicked.connect(self.clicked)
        self.layout.addWidget(self.listwidget,1,0)
        self.textarea = QTextEdit()
        self.textarea.setHidden(True)
        self.layout.addWidget(self.textarea,1,0)
        self.mylayout = QHBoxLayout()
        self.open_button=QPushButton()
        self.open_button.setText("Open")
        if sys.platform == "linux" or sys.platform == "linux2":
            self.open_button.setIcon(QtGui.QIcon.fromTheme("document-open"))
        else:
            self.open_button.setIcon(qApp.style().standardIcon(QStyle.SP_ArrowForward)) 

        self.open_button.clicked.connect(self.open)
        self.new_button=QPushButton()
        self.new_button.setText("New")
        if sys.platform == "linux" or sys.platform == "linux2":
            self.new_button.setIcon(QtGui.QIcon.fromTheme("document-new"))
        else:
            self.new_button.setText("+ New")

        self.new_button.clicked.connect(self.new)
        self.del_button=QPushButton()
        self.del_button.setText("Delete")
        self.del_button.setIcon(qApp.style().standardIcon(QStyle.SP_DialogCancelButton))
        self.del_button.clicked.connect(self.delete)
        self.mylayout.addWidget(self.open_button)
        self.mylayout.addWidget(self.new_button)
        self.mylayout.addWidget(self.del_button)
        self.layout.addLayout(self.mylayout,2,0)
        self.menubar = QMenuBar()
        self.layout.addWidget(self.menubar, 0, 0)
        self.actionFile = self.menubar.addMenu("File")
        self.open_action = QAction("Open", self)      
        if sys.platform == "linux" or sys.platform == "linux2":
            self.open_action.setIcon(QtGui.QIcon.fromTheme("document-open"))
        else:
            self.open_action.setIcon(qApp.style().standardIcon(QStyle.SP_ArrowForward)) 
            
        self.open_action.triggered.connect(self.open)
        self.open_action.setShortcut("Ctrl+O")
        self.delete_action = QAction("Delete", self)
        self.delete_action.triggered.connect(self.delete)
        self.delete_action.setIcon(qApp.style().standardIcon(QStyle.SP_DialogCancelButton))
        self.delete_action.setShortcut("Ctrl+D")
        self.new_action = QAction("New", self)
        if sys.platform == "linux" or sys.platform == "linux2":
            self.new_action.setIcon(QtGui.QIcon.fromTheme("document-new"))
        self.new_action.triggered.connect(self.new)
        self.new_action.setShortcut("Ctrl+N")
        self.quit_action = QAction("Quit", self)
        self.quit_action.setShortcut("Ctrl+Q")
        self.quit_action.setIcon(qApp.style().standardIcon(QStyle.SP_DialogCloseButton))
        self.quit_action.triggered.connect(self.quit)
        self.actionFile.addAction(self.open_action)
        self.actionFile.addAction(self.new_action)
        self.actionFile.addAction(self.delete_action)
        self.sync_action = QAction("Sync Files", self)
        self.sync_action.setIcon(qApp.style().standardIcon(QStyle.SP_BrowserReload))
        self.sync_action.setShortcut("Ctrl+S")
        self.sync_action.triggered.connect(self.sync)
        self.actionFile.addAction(self.sync_action)
        self.actionFile.addSeparator()
        self.actionFile.addAction(self.quit_action)
        self.actionHelp = self.menubar.addMenu("Help")
        self.help_action = QAction("About", self)
        if sys.platform == "linux" or sys.platform == "linux2":
            self.help_action.setIcon(QtGui.QIcon.fromTheme("help-about"))
        else:
            self.help_action.setIcon(qApp.style().standardIcon(QStyle.SP_TitleBarContextHelpButton)) 
            
        self.help_action.setShortcut("Ctrl+I")
        self.help_action.triggered.connect(self.info)
        self.help_action_qt = QAction("About Qt", self)
        self.help_action_qt.setIcon(qApp.style().standardIcon(QStyle.SP_TitleBarMenuButton)) 
        self.help_action_qt.triggered.connect(self.info_qt)
        self.actionHelp.addAction(self.help_action)
        self.actionHelp.addAction(self.help_action_qt)
        self.sync()

    def clicked(self, qmodelindex):
        item = self.listwidget.currentItem()
        print(item.text())

    def open(self):
        try:
            if not self.listwidget.item(self.listwidget.currentRow()) == None:
                item = self.listwidget.item(self.listwidget.currentRow()).text()
                if item or not item == NoneType:
                    self.enter_edit_mode(item)
        except Exception as e:
            QMessageBox.critical(self, "An internal error occured", "Exact error: "+str(e))
        
        

    def new(self):
        items = []
        for i in range(self.listwidget.count()):
            items.append(self.listwidget.item(i).text())
        text, ok = QInputDialog.getText(self, 'Text Input Dialog', 'Enter document name:')
        if ok and not text == "":
            if text in items:
                QMessageBox.warning(self, "Error", "Notebook already exists.")
            else:
                try:
                    Path('./notebooks/'+text).touch()
                    self.sync()
                except Exception as e:
                    QMessageBox.critical(self, "An internal error occured", "Exact error: "+str(e))

    def delete(self):
        try:
            if not self.listwidget.item(self.listwidget.currentRow()) == None:
                item = self.listwidget.item(self.listwidget.currentRow()).text()
                if item or not item == NoneType:
                    os.unlink("./notebooks/"+item)
                    self.sync()
        except Exception as e:
            QMessageBox.critical(self, "An internal error occured", "Exact error: "+str(e))
    
    def sync(self):
        self.listwidget.clear()
        for e in _files("./notebooks"):
            self.listwidget.addItem(e)
        if self.opened_file:
            file = open("./notebook/"+self.opened_file, "w")
            file.write("")
            file.close()
        self.listwidget.sortItems()

    def quit(self):
        sys.exit(0)

    def info_qt(self):
        QMessageBox.aboutQt(self, "About Qt")

    def info(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("About")
        dlg.resize(400, 100)
        self.layout2 = QGridLayout()
        self.layout2.setContentsMargins(8,8,8,8)
        dlg.setLayout(self.layout2)
        info_label = QLabel()

        info_label.setText("This program is made by Stelios 2022.\nThe project is open source and it is under the GPLv3+ License")
        self.layout2.addWidget(info_label,0,0)
        self.close_button = QPushButton()
        self.close_button.setText("Close")
        self.close_button.clicked.connect(dlg.close)
        self.layout2.addWidget(self.close_button)
        dlg.exec()

    def closeEvent(self, event): 
        can_exit = QMessageBox.question(self,'', "Save before exiting?", QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        if can_exit == QMessageBox.Yes:
            event.ignore()
            self.sync()
            sys.exit()
            
        elif can_exit == QMessageBox.No:
            event.accept()

        else:
            event.ignore()

    def enter_edit_mode(self, file):
        self.listwidget.setHidden(True)
        self.textarea.setHidden(False)
        self.open_action.setEnabled(False)
        self.new_action.setEnabled(False)
        self.delete_action.setEnabled(False)
        self.new_button.setHidden(True)
        self.del_button.setHidden(True)
        self.open_button.setHidden(True)
        self.opened_file = "./notebooks/"+file
        self.setWindowTitle("EDocBook - "+file)

    def exit_edit_mode(self):
        self.listwidget.setHidden(False)
        self.textarea.setHidden(True)
        self.open_action.setEnabled(True)
        self.new_action.setEnabled(True)
        self.delete_action.setEnabled(True)
        self.new_button.setHidden(False)
        self.del_button.setHidden(False)
        self.open_button.setHidden(False)
        self.setWindowTitle("EDocBook")


app = QApplication(sys.argv)
screen = Window()
screen.show()
sys.exit(app.exec_())