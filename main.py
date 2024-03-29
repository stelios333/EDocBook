from pathlib import Path
import warnings
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
try:
    from PyQt5 import QtMultimedia
except ImportError:
    pass
import sys, os

if sys.platform == "darwin":
    print("\033[33mWarning: MacOS isn't supported\033[0m")

def _files(path):
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            yield file

class Window(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        try:
            QtMultimedia
            self.is_multimedia_available = True
        except NameError:
            self.is_multimedia_available = False

        if sys.platform == "win32":
            self.is_multimedia_available = False
        self.opened_file = ""
        self.setWindowTitle("EDocBook")
        self.setWindowIcon(QtGui.QIcon(QtCore.QDir.current().absoluteFilePath("logo.png")))
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        self.resize(600, 400)
        self.is_saved = True
        if not os.path.isdir("notebooks"):
            os.mkdir("notebooks")
        self.layout = QGridLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)
        self.listwidget = QListWidget()
        self.listwidget.installEventFilter(self)
        self.listwidget.itemDoubleClicked.connect(self.clicked)
        self.layout.addWidget(self.listwidget,1,0)
        self.textarea = QTextEdit()
        self.textarea.textChanged.connect(self.set_unsaved_state)
        self.textarea.setHidden(True)
        self.layout.addWidget(self.textarea,1,0)
        self.mylayout = QHBoxLayout()
        self.mylayout.setContentsMargins(8,2,8,8)
        self.open_button=QPushButton()
        self.open_button.setText("Open")
        if sys.platform == "linux" or sys.platform == "linux2":
            self.open_button.setIcon(QtGui.QIcon.fromTheme("document-open"))
        else:
            self.open_button.setIcon(QtGui.QIcon(QtCore.QDir.current().absoluteFilePath("document-open-folder.svg")))

        self.open_button.clicked.connect(self.open)
        self.new_button=QPushButton()
        self.new_button.setText("New")
        if sys.platform == "linux" or sys.platform == "linux2":
            self.new_button.setIcon(QtGui.QIcon.fromTheme("document-new"))
        else:
            self.new_button.setIcon(QtGui.QIcon(QtCore.QDir.current().absoluteFilePath("document-new.svg")))

        self.new_button.clicked.connect(self.new)
        self.rename_button=QPushButton()
        self.rename_button.setText("Rename")
        if sys.platform == "linux" or sys.platform == "linux2":
            self.rename_button.setIcon(QtGui.QIcon.fromTheme("edit-rename"))
        else:
            self.rename_button.setIcon(QtGui.QIcon(QtCore.QDir.current().absoluteFilePath("document-edit.svg")))

        self.rename_button.clicked.connect(self.rename)
        self.del_button=QPushButton()
        self.del_button.setText("Delete")
        if sys.platform == "linux" or sys.platform == "linux2":
            self.del_button.setIcon(QtGui.QIcon.fromTheme("edit-delete"))
        else:
            self.del_button.setIcon(QtGui.QIcon(QtCore.QDir.current().absoluteFilePath("edit-delete.svg")))
        self.del_button.clicked.connect(self.delete)
        self.back_button=QPushButton()
        self.back_button.setText("Back")
        if sys.platform == "linux" or sys.platform == "linux2":
            self.back_button.setIcon(QtGui.QIcon.fromTheme("go-previous"))
        else:
            self.back_button.setIcon(QtGui.QIcon(QtCore.QDir.current().absoluteFilePath("go-previous.svg")))
        self.back_button.setHidden(True)
        self.back_button.clicked.connect(self.back_confirm) 
        self.sync_button=QPushButton()
        self.sync_button.setText("Sync File")
        if sys.platform == "linux" or sys.platform == "linux2":
            self.sync_button.setIcon(QtGui.QIcon.fromTheme("folder-sync"))
        else:
            self.sync_button.setIcon(QtGui.QIcon(QtCore.QDir.current().absoluteFilePath("folder-sync.svg")))
        self.sync_button.setHidden(True)
        self.sync_button.clicked.connect(self.sync) 
        self.mylayout.addWidget(self.back_button) 
        self.mylayout.addWidget(self.sync_button) 
        self.mylayout.addWidget(self.open_button)
        self.mylayout.addWidget(self.new_button)
        self.mylayout.addWidget(self.rename_button)
        self.mylayout.addWidget(self.del_button)
        self.layout.addLayout(self.mylayout,2,0)
        self.menubar = QMenuBar()
        self.layout.addWidget(self.menubar, 0, 0)
        self.actionFile = self.menubar.addMenu("File")
        self.exit_action = QAction("Back", self)
        if sys.platform == "linux" or sys.platform == "linux2":
            self.exit_action.setIcon(QtGui.QIcon.fromTheme("go-previous"))
        else:
            self.exit_action.setIcon(QtGui.QIcon(QtCore.QDir.current().absoluteFilePath("go-previous.svg")))
        self.exit_action.setShortcut("Ctrl+E")
        self.exit_action.setEnabled(False)
        self.exit_action.triggered.connect(self.back_confirm)
        self.actionFile.addAction(self.exit_action)
        self.open_action = QAction("Open", self)      
        if sys.platform == "linux" or sys.platform == "linux2":
            self.open_action.setIcon(QtGui.QIcon.fromTheme("document-open"))
        else:
            self.open_action.setIcon(QtGui.QIcon(QtCore.QDir.current().absoluteFilePath("document-open-folder.svg")))
            
        self.open_action.triggered.connect(self.open)
        self.open_action.setShortcut("Ctrl+O")
        self.delete_action = QAction("Delete", self)
        self.delete_action.triggered.connect(self.delete)
        if sys.platform == "linux" or sys.platform == "linux2":
            self.delete_action.setIcon(QtGui.QIcon.fromTheme("edit-delete"))
        else:
            self.delete_action.setIcon(QtGui.QIcon(QtCore.QDir.current().absoluteFilePath("edit-delete.svg")))
        self.delete_action.setShortcut("Ctrl+D")
        self.rename_action = QAction("Rename", self)
        self.rename_action.triggered.connect(self.rename)
        if sys.platform == "linux" or sys.platform == "linux2":
            self.rename_action.setIcon(QtGui.QIcon.fromTheme("edit-rename"))
        else:
            self.rename_action.setIcon(QtGui.QIcon(QtCore.QDir.current().absoluteFilePath("document-edit.svg")))
        self.rename_action.setShortcut("Ctrl+R")
        self.new_action = QAction("New", self)
        if sys.platform == "linux" or sys.platform == "linux2":
            self.new_action.setIcon(QtGui.QIcon.fromTheme("document-new"))
        else:
            self.new_action.setIcon(QtGui.QIcon(QtCore.QDir.current().absoluteFilePath("document-new.svg")))
        self.new_action.triggered.connect(self.new)
        self.new_action.setShortcut("Ctrl+N")
        self.export_action = QAction("Export", self)
        if sys.platform == "linux" or sys.platform == "linux2":
            self.export_action.setIcon(QtGui.QIcon.fromTheme("document-export"))
        else:
            self.export_action.setIcon(QtGui.QIcon(QtCore.QDir.current().absoluteFilePath("document-export.svg")))

        self.export_action.triggered.connect(self.export)
        self.import_action = QAction("Import", self)
        if sys.platform == "linux" or sys.platform == "linux2":
            self.import_action.setIcon(QtGui.QIcon.fromTheme("document-import"))
        else:
            self.import_action.setIcon(QtGui.QIcon(QtCore.QDir.current().absoluteFilePath("document-import.svg")))
            
        self.import_action.triggered.connect(self.import_)
        self.quit_action = QAction("Quit", self)
        self.quit_action.setShortcut("Ctrl+Q")
        if sys.platform == "linux" or sys.platform == "linux2":
            self.quit_action.setIcon(QtGui.QIcon.fromTheme("application-exit"))
        else:
            self.quit_action.setIcon(QtGui.QIcon(QtCore.QDir.current().absoluteFilePath("application-exit.svg")))
        self.quit_action.triggered.connect(self.quit)
        self.actionFile.addAction(self.open_action)
        self.actionFile.addAction(self.new_action)
        self.actionFile.addAction(self.rename_action)
        self.actionFile.addAction(self.delete_action)
        self.sync_action = QAction("Sync Files", self)
        if sys.platform == "linux" or sys.platform == "linux2":
            self.sync_action.setIcon(QtGui.QIcon.fromTheme("folder-sync"))
        else:
            self.sync_action.setIcon(QtGui.QIcon(QtCore.QDir.current().absoluteFilePath("folder-sync.svg")))
        self.sync_action.setShortcut("Ctrl+S")
        self.sync_action.triggered.connect(self.sync)
        self.actionFile.addAction(self.sync_action)
        self.actionFile.addSeparator()
        self.actionFile.addAction(self.import_action)
        self.actionFile.addAction(self.export_action)
        self.actionFile.addSeparator()
        self.actionFile.addAction(self.quit_action)
        self.actionHelp = self.menubar.addMenu("Help")
        self.help_action = QAction("About", self)
        if sys.platform == "linux" or sys.platform == "linux2":
            self.help_action.setIcon(QtGui.QIcon.fromTheme("help-about"))
        else:
            self.help_action.setIcon(QtGui.QIcon(QtCore.QDir.current().absoluteFilePath("help-about.svg")))
            
        self.help_action.setShortcut("Ctrl+I")
        self.help_action.triggered.connect(self.info)
        self.help_action_qt = QAction("About Qt", self)
        self.help_action_qt.setIcon(qApp.style().standardIcon(QStyle.SP_TitleBarMenuButton)) 
        self.help_action_qt.triggered.connect(self.info_qt)
        self.actionHelp.addAction(self.help_action)
        self.actionHelp.addAction(self.help_action_qt)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_menus)
        self.timer.setInterval(100)
        self.timer.start()
        self.sync()

    def clicked(self, qmodelindex):
        try:
            if not self.listwidget.item(self.listwidget.currentRow()) == None:
                item = self.listwidget.item(self.listwidget.currentRow()).text()
                if item:
                    self.enter_edit_mode(item)
        except Exception as e:
            if self.is_multimedia_available:
                fullpath = QtCore.QDir.current().absoluteFilePath("Oxygen-Sys-App-Error-Critical.ogg") 
                url = QtCore.QUrl.fromLocalFile(fullpath)
                content = QtMultimedia.QMediaContent(url)
                player = QtMultimedia.QMediaPlayer()
                player.setMedia(content)
                player.play()
            QMessageBox.critical(self, "An internal error occured", "Exact error: "+str(e))

    def import_(self):
        items = []
        for i in range(self.listwidget.count()):
            items.append(self.listwidget.item(i).text())
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, ok = QFileDialog.getOpenFileName(self,"Import File", "","Text Files (*.txt);;All Files (*)", options=options)
        if ok and not fileName == "":
            notebook_name = os.path.split(fileName)[1].split(".")[0]
            if notebook_name in items:
                if self.is_multimedia_available:
                    fullpath = QtCore.QDir.current().absoluteFilePath("Oxygen-Sys-Warning.ogg") 
                    url = QtCore.QUrl.fromLocalFile(fullpath)
                    content = QtMultimedia.QMediaContent(url)
                    player = QtMultimedia.QMediaPlayer()
                    player.setMedia(content)
                    player.play()
                QMessageBox.warning(self, "Error", "Notebook already exists.")
            else:
                try:
                    file = open("./notebooks/"+notebook_name, "w")
                    _file = open(fileName, "r")
                    _file_content = _file.read()
                    _file.close()
                    file.write(_file_content)
                    file.close()
                    self.sync()
                except Exception as e:
                    if self.is_multimedia_available:
                        fullpath = QtCore.QDir.current().absoluteFilePath("Oxygen-Sys-App-Error-Critical.ogg") 
                        url = QtCore.QUrl.fromLocalFile(fullpath)
                        content = QtMultimedia.QMediaContent(url)
                        player = QtMultimedia.QMediaPlayer()
                        player.setMedia(content)
                        player.play()
                    QMessageBox.critical(self, "An internal error occured", "Exact error: "+str(e))

    def export(self):
        try:
            if self.opened_file == "":
                if not self.listwidget.item(self.listwidget.currentRow()) == None:
                    item = self.listwidget.item(self.listwidget.currentRow()).text()
                    if item:
                        _file = open("./notebooks/"+item, "r")
                        file_contents = _file.read()
                        _file.close()
                        options = QFileDialog.Options()
                        options |= QFileDialog.DontUseNativeDialog
                        fileName, ok = QFileDialog.getSaveFileName(self,"Export File", "","Text Files (*.txt);;All Files (*)", options=options)
                        if ok:
                            file_ = open(fileName, "w")
                            file_.write(file_contents)
                            file_.close()
            else:
                file_contents = self.textarea.toPlainText()
                options = QFileDialog.Options()
                options |= QFileDialog.DontUseNativeDialog
                fileName, ok = QFileDialog.getSaveFileName(self,"QFileDialog.getOpenFileName()", "","Text Files (*.txt);;All Files (*)", options=options)
                if ok:
                    file_ = open(fileName, "w")
                    file_.write(file_contents)
                    file_.close()
        except Exception as e:
            if self.is_multimedia_available:
                fullpath = QtCore.QDir.current().absoluteFilePath("Oxygen-Sys-App-Error-Critical.ogg") 
                url = QtCore.QUrl.fromLocalFile(fullpath)
                content = QtMultimedia.QMediaContent(url)
                player = QtMultimedia.QMediaPlayer()
                player.setMedia(content)
                player.play()
            QMessageBox.critical(self, "An internal error occured", "Exact error: "+str(e))

    def update_menus(self):
        if self.listwidget.item(self.listwidget.currentRow()) == None:
            self.rename_action.setEnabled(False)
            self.rename_button.setEnabled(False)
            self.del_button.setEnabled(False)
            self.delete_action.setEnabled(False)
            self.rename_action.setEnabled(False)
            self.rename_button.setEnabled(False)
            self.open_action.setEnabled(False)
            self.open_button.setEnabled(False)
            if self.opened_file == "":
                self.export_action.setEnabled(False)
        else:
            if self.opened_file == "":
                self.rename_action.setEnabled(True)
                self.rename_button.setEnabled(True)
                self.del_button.setEnabled(True)
                self.delete_action.setEnabled(True)
                self.rename_action.setEnabled(True)
                self.rename_button.setEnabled(True)
                self.open_action.setEnabled(True)
                self.open_button.setEnabled(True)
            self.export_action.setEnabled(True)

    def open(self):
        try:
            if not self.listwidget.item(self.listwidget.currentRow()) == None:
                item = self.listwidget.item(self.listwidget.currentRow()).text()
                if item:
                    self.enter_edit_mode(item)
        except Exception as e:
            if self.is_multimedia_available:
                fullpath = QtCore.QDir.current().absoluteFilePath("Oxygen-Sys-App-Error-Critical.ogg") 
                url = QtCore.QUrl.fromLocalFile(fullpath)
                content = QtMultimedia.QMediaContent(url)
                player = QtMultimedia.QMediaPlayer()
                player.setMedia(content)
                player.play()
            QMessageBox.critical(self, "An internal error occured", "Exact error: "+str(e))
        
    def set_unsaved_state(self):
        self.is_saved = False

    def rename(self):
        items = []
        for i in range(self.listwidget.count()):
            items.append(self.listwidget.item(i).text())
        if not self.listwidget.item(self.listwidget.currentRow()) == None:
            item = self.listwidget.item(self.listwidget.currentRow()).text()
            if item:
                text, ok = QInputDialog.getText(self, 'EDocBook', 'Enter new document name:')
                if ok and not text == "":
                    if text in items:
                        if self.is_multimedia_available:
                            fullpath = QtCore.QDir.current().absoluteFilePath("Oxygen-Sys-Warning.ogg") 
                            url = QtCore.QUrl.fromLocalFile(fullpath)
                            content = QtMultimedia.QMediaContent(url)
                            player = QtMultimedia.QMediaPlayer()
                            player.setMedia(content)
                            player.play()
                        QMessageBox.warning(self, "Error", "Notebook already exists.")
                    else:
                        try:
                            os.rename("./notebooks/"+item, "./notebooks/"+text)
                            self.sync()
                        except Exception as e:
                            if self.is_multimedia_available:
                                fullpath = QtCore.QDir.current().absoluteFilePath("Oxygen-Sys-App-Error-Critical.ogg") 
                                url = QtCore.QUrl.fromLocalFile(fullpath)
                                content = QtMultimedia.QMediaContent(url)
                                player = QtMultimedia.QMediaPlayer()
                                player.setMedia(content)
                                player.play()
                            QMessageBox.critical(self, "An internal error occured", "Exact error: "+str(e))

    def new(self):
        items = []
        for i in range(self.listwidget.count()):
            items.append(self.listwidget.item(i).text())
        text, ok = QInputDialog.getText(self, 'EDocBook', 'Enter document name:')
        if ok and not text == "":
            if text in items:
                if self.is_multimedia_available:
                    fullpath = QtCore.QDir.current().absoluteFilePath("Oxygen-Sys-Warning.ogg") 
                    url = QtCore.QUrl.fromLocalFile(fullpath)
                    content = QtMultimedia.QMediaContent(url)
                    player = QtMultimedia.QMediaPlayer()
                    player.setMedia(content)
                    player.play()
                QMessageBox.warning(self, "Error", "Notebook already exists.")
            else:
                try:
                    Path('./notebooks/'+text).touch()
                    self.sync()
                except Exception as e:
                    if self.is_multimedia_available:
                        fullpath = QtCore.QDir.current().absoluteFilePath("Oxygen-Sys-App-Error-Critical.ogg") 
                        url = QtCore.QUrl.fromLocalFile(fullpath)
                        content = QtMultimedia.QMediaContent(url)
                        player = QtMultimedia.QMediaPlayer()
                        player.setMedia(content)
                        player.play()
                    QMessageBox.critical(self, "An internal error occured", "Exact error: "+str(e))

    def delete(self):
        try:
            if not self.listwidget.item(self.listwidget.currentRow()) == None:
                item = self.listwidget.item(self.listwidget.currentRow()).text()
                if item:
                    os.unlink("./notebooks/"+item)
                    self.sync()
        except Exception as e:
            if self.is_multimedia_available:
                fullpath = QtCore.QDir.current().absoluteFilePath("Oxygen-Sys-App-Error-Critical.ogg") 
                url = QtCore.QUrl.fromLocalFile(fullpath)
                content = QtMultimedia.QMediaContent(url)
                player = QtMultimedia.QMediaPlayer()
                player.setMedia(content)
                player.play()
            QMessageBox.critical(self, "An internal error occured", "Exact error: "+str(e))
    
    def sync(self):
        self.listwidget.clear()
        for e in _files("./notebooks"):
            self.listwidget.addItem(e)
        if self.opened_file:
            file = open(self.opened_file, "w")
            file.write(self.textarea.toPlainText())
            file.close()
        self.listwidget.sortItems()
        self.is_saved = True

    def quit(self):
        sys.exit(0)

    def info_qt(self):
        QMessageBox.aboutQt(self, "About Qt")

    def info(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("About")
        self.layout2 = QGridLayout()
        self.layout2.setContentsMargins(8,8,8,8)
        dlg.setLayout(self.layout2)
        mylayout = QHBoxLayout()
        icon_label = QLabel()
        pixmap = QtGui.QPixmap(QtCore.QDir.current().absoluteFilePath("help-about.png"))
        icon_label.setPixmap(pixmap)
        info_label = QLabel()

        info_label.setText("EDocBook is an amazing simple text editor, which gathers all your notes in one place.\nIt is made by Stelios333 in 2022.\nThe project is open source and it is under the GPLv3+ License")
        mylayout.addWidget(icon_label)
        mylayout.addWidget(info_label)
        self.close_button = QPushButton()
        self.close_button.setText("Close")
        self.close_button.clicked.connect(dlg.close)
        self.layout2.addLayout(mylayout,0,0)
        self.layout2.addWidget(self.close_button,1,0)
        dlg.setFixedSize(610, 130)
        dlg.exec()

    def closeEvent(self, event): 
        if self.is_saved == False:
            if self.is_multimedia_available:
                fullpath = QtCore.QDir.current().absoluteFilePath("Oxygen-Sys-Warning.ogg") 
                url = QtCore.QUrl.fromLocalFile(fullpath)
                content = QtMultimedia.QMediaContent(url)
                player = QtMultimedia.QMediaPlayer()
                player.setMedia(content)
                player.play()

            can_exit = QMessageBox.question(self,'', "Save before exiting?", QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if can_exit == QMessageBox.Yes:
                event.ignore()
                self.sync()
                sys.exit()
                
            elif can_exit == QMessageBox.No:
                event.accept()

            else:
                event.ignore()
        else:
            event.accept()
    
    def back_confirm(self):
        if self.is_saved == False:
            if self.is_multimedia_available:
                fullpath = QtCore.QDir.current().absoluteFilePath("Oxygen-Sys-Warning.ogg") 
                url = QtCore.QUrl.fromLocalFile(fullpath)
                content = QtMultimedia.QMediaContent(url)
                player = QtMultimedia.QMediaPlayer()
                player.setMedia(content)
                player.play()

            can_exit = QMessageBox.question(self,'', "Save before exiting?", QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if can_exit == QMessageBox.Yes:
                self.sync()
                self.exit_edit_mode()
                
            elif can_exit == QMessageBox.No:
                self.exit_edit_mode()

            else:
                pass
        else: 
            self.exit_edit_mode()
    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.ContextMenu and source is self.listwidget:
            self.contextmenu = QMenu()
            self.contextmenu.addAction(self.open_action)
            self.contextmenu.addAction(self.new_action)
            self.contextmenu.addAction(self.rename_action)
            self.contextmenu.addAction(self.delete_action)
            if self.contextmenu.exec(event.globalPos()):
                item = source.itemAt(event.pos())
                print(item)
            return True
        return super().eventFilter(source, event)

    def enter_edit_mode(self, file):
        self.sync_action.setText("Sync File")
        self.rename_button.setHidden(True)
        self.sync_button.setHidden(False)
        self.back_button.setHidden(False)
        self.exit_action.setEnabled(True)
        self.listwidget.setHidden(True)
        self.textarea.setHidden(False)
        self.open_action.setEnabled(False)
        self.new_action.setEnabled(False)
        self.import_action.setEnabled(False)
        self.delete_action.setEnabled(False)
        self.rename_action.setEnabled(False)
        self.new_button.setHidden(True)
        self.del_button.setHidden(True)
        self.open_button.setHidden(True)
        self.opened_file = "./notebooks/"+file
        self.setWindowTitle("EDocBook - "+file)
        _file = open(self.opened_file, "r")
        file_contents = _file.read()
        _file.close()
        self.textarea.setPlainText(file_contents)
        self.is_saved = True

    def exit_edit_mode(self):
        self.sync_action.setText("Sync Files")
        self.rename_button.setHidden(False)
        self.sync_button.setHidden(True)
        self.back_button.setHidden(True)
        self.exit_action.setEnabled(False)
        self.listwidget.setHidden(False)
        self.textarea.setHidden(True)
        self.open_action.setEnabled(True)
        self.import_action.setEnabled(True)
        self.new_action.setEnabled(True)
        self.delete_action.setEnabled(True)
        self.rename_action.setEnabled(True)
        self.new_button.setHidden(False)
        self.del_button.setHidden(False)
        self.open_button.setHidden(False)
        self.setWindowTitle("EDocBook")
        self.textarea.setPlainText("")
        self.sync()
        self.opened_file = ""


app = QApplication(sys.argv)
screen = Window()
screen.show()
sys.exit(app.exec())