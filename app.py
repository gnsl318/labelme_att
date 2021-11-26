import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import json
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()
    
    def setupUI(self):
        self.setWindowTitle("Labelme Att")
        self.resize(1500,1500)
        widget = QWidget(self)
        self.Mainlayout = QVBoxLayout(widget)
        self.canvas_layout = QHBoxLayout()
        self.Mainlayout.addLayout(self.canvas_layout)
        self.label = QLabel(self)
        self.label.setContentsMargins(10,10,10,10)
        self.canvas_layout.addWidget(self.label)
        self.label.resize(1300,1000)
        self.make_toolbar()
        self.make_dock()
        





        self.setCentralWidget(widget)
    def make_dock(self):
        self.dock_layout=QHBoxLayout()
        self.result_dock=QDockWidget("Result_list",self)
        self.result_dock.setFixedSize(200,500)
        self.addDockWidget(Qt.RightDockWidgetArea,self.result_dock)

    def make_toolbar(self):
        self.open_file_button = QAction(self.style().standardIcon(QStyle.SP_FileIcon),"Opne_File",self)
        self.open_file_button.setShortcut('Ctrl+O')
        self.open_file_button.triggered.connect(self.open_file)
        self.open_folder_button = QAction(self.style().standardIcon(QStyle.SP_DirOpenIcon),"Opne_Folder",self)
        self.open_folder_button.setShortcut('Ctrl+P')
        self.open_folder_button.triggered.connect(self.open_folder)
        self.next_button = QAction(self.style().standardIcon(QStyle.SP_ArrowForward),"Next_Image",self)
        self.next_button.setShortcut('Ctrl+D')
        self.next_button.triggered.connect(self.next_image)
        self.back_button = QAction(self.style().standardIcon(QStyle.SP_ArrowBack),"Back_Image",self)
        self.back_button.setShortcut('Ctrl+A')
        self.back_button.triggered.connect(self.back_image)

        self.statusBar()

        self.toolbar = QToolBar()
        self.addToolBar(Qt.LeftToolBarArea,self.toolbar)
        self.toolbar.addAction(self.open_file_button)
        self.toolbar.addAction(self.open_folder_button)
        self.toolbar.addAction(self.next_button)
        self.toolbar.addAction(self.back_button)

    def open_file(self):
        print("open_file")
        self.files = QFileDialog.getOpenFileName(self,directory='./',caption="Select a data file",filter="Data File (*.jpg *.jpeg *.png)")
        self.dock_list(list(self.files))
        self.index = 0
        self.image_load(self.files[self.index])
    
    def readjson(self,jsonfile):
        with open(jsonfile) as jf:
            return json.load(jf)
    def image_load(self,file):
        self.label.clear()
        image = QPixmap(file).scaled(self.label.width(),self.label.height(),Qt.KeepAspectRatio,Qt.SmoothTransformation)
        #self.label.resize(self.image.width(),self.image.height())
        #self.label.setPixmap(self.image)
        self.label.show()
        jsonfile=file.replace(file.split(".")[-1],"json")
        try:
            data = self.readjson(jsonfile)
            height=self.label.height()/data['imageHeight']
            width=self.label.width()/data['imageWidth']
            self.pen =QPainter(image)
            for labeling in data['shapes']:
                point_list = labeling['points']
                points=[]
                
                for point in point_list:
                    points.append(QPoint(point[0]*width,point[1]*height))
                    self.draw_point(points)
                self.pen.end
            
        except:
            pass
    def draw_point(self,points):
        polygon = QPolygon(points)
        self.pen.setPen(QPen(Qt.red,3))
        #self.pen.setBrush(QBrush(QColor('#D187EF')))
        self.pen.drawPolygon(polygon)
        self.label.setPixmap(image)

        
    def next_image(self):
        self.index +=1
        if self.index >= len(self.files)-1:
            self.index = len(self.files)-1
            pass
        self.image_load(self.files[self.index])
    def back_image(self):
        self.index -=1
        if self.index <=0:
            self.index = 0
            pass
        self.image_load(self.files[self.index])
    

    def dock_list(self,file_list):
        self.file_list = QListWidget()
        for file in file_list:
            self.file_list.addItem(file)
        self.result_dock.setWidget(self.file_list)
        self.result_dock.setFloating(False)

    def open_folder(self):
        print("open_folder")
        self.files=[]
        folder = QFileDialog.getExistingDirectory(self,"Choose Files",os.getcwd())
        file_list = os.listdir(folder)
        for file in file_list:
            format = file.split(".")[-1].lower()
            if format =="jpg" or format =="jpeg" or format =="png":
                self.files.append(os.path.join(folder,file))
        self.dock_list(self.files)
        self.index = 0
        self.image_load(self.files[self.index])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())