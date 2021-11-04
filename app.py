import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()
    
    def setupUI(self):
        self.setWindowTitle("Labelme Att")

        self.open_file_button = QAction(QIcon(os.path.join(os.getcwd(),"images/file.png")),"Opne_File",self)
        self.open_file_button.setShortcut('Ctrl+O')
        self.open_file_button.triggered.connect(self.open_file)
        self.open_folder_button = QAction(QIcon(os.path.join(os.getcwd(),"images/folder.png")),"Opne_Folder",self)
        self.open_folder_button.setShortcut('Ctrl+P')
        self.open_folder_button.triggered.connect(self.open_folder)

        self.statusBar()

        self.toolbar = QToolBar()
        self.addToolBar(Qt.LeftToolBarArea,self.toolbar)
        self.toolbar.addAction(self.open_file_button)
        self.toolbar.addAction(self.open_folder_button)
        

    def open_file(self):
        print("open_file")
        file = QFileDialog.getOpenFileName(self)
    
    def open_folder(self):
        print("open_folder")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())