from PyQt5.QtWidgets import *
from PyQt5 import QtGui
import sys, os

class Window(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle("EDocBook")
        self.setWindowIcon(QtGui.QIcon('logo.png'))
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        self.resize(600, 400)
        if not os.path.isdir("notebooks"):
            os.mkdir("notebooks")
        layout = QGridLayout()
        self.setLayout(layout)
        self.listwidget = QListWidget()
        self.listwidget.insertItem(0, "Red")
        self.listwidget.insertItem(1, "Orange")
        self.listwidget.insertItem(2, "Blue")
        self.listwidget.insertItem(3, "White")
        self.listwidget.insertItem(4, "Green")
        self.listwidget.itemDoubleClicked.connect(self.clicked)
        layout.addWidget(self.listwidget,1,0)
        mylayout = QHBoxLayout()
        open_button=QPushButton()
        open_button.setText("Open")
        open_button.clicked.connect(self.open)
        new_button=QPushButton()
        new_button.setText("New")
        new_button.clicked.connect(self.new)
        del_button=QPushButton()
        del_button.setText("Delete")
        del_button.clicked.connect(self.delete)
        mylayout.addWidget(open_button)
        mylayout.addWidget(new_button)
        mylayout.addWidget(del_button)
        layout.addLayout(mylayout,2,0)
        menubar = QMenuBar()
        layout.addWidget(menubar, 0, 0)
        actionFile = menubar.addMenu("File")
        open_action = QAction("Open", self)
        open_action.triggered.connect(self.open)
        open_action.setShortcut("Ctrl+O")
        delete_action = QAction("Delete", self)
        delete_action.triggered.connect(self.delete)
        delete_action.setShortcut("Ctrl+D")
        new_action = QAction("New", self)
        new_action.triggered.connect(self.new)
        new_action.setShortcut("Ctrl+N")
        quit_action = QAction("Quit", self)
        quit_action.setShortcut("Ctrl+Q")
        quit_action.triggered.connect(self.quit)
        actionFile.addAction(open_action)
        actionFile.addAction(new_action)
        actionFile.addAction(delete_action)
        actionFile.addSeparator()
        actionFile.addAction(quit_action)
        actionHelp = menubar.addMenu("Help")
        help_action = QAction("About", self)
        help_action.setShortcut("Ctrl+I")
        help_action.triggered.connect(self.info)
        actionHelp.addAction(help_action)

    def clicked(self, qmodelindex):
        item = self.listwidget.currentItem()
        print(item.text())

    def open(self):
        print("o")

    def new(self):
        text, ok = QInputDialog.getText(self, 'Text Input Dialog', 'Enter document name:')
        if ok and not text == "":
            self.listwidget.addItem(text)

    def delete(self):
        self.listwidget.takeItem(self.listwidget.currentRow())
    
    def quit(self):
        sys.exit(0)

    def info(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("About")
        layout = QGridLayout()
        dlg.setLayout(layout)
        info_label = QLabel()
	
        info_label.setText("This program is made by Stelios 2022.\nThe project is open source and it is under the MIT License")
        layout.addWidget(info_label,0,0)
        self.close_button = QPushButton()
        self.close_button.setText("Close")
        self.close_button.clicked.connect(dlg.close)
        layout.addWidget(self.close_button)
        dlg.exec()

app = QApplication(sys.argv)
screen = Window()
screen.show()
sys.exit(app.exec_())