import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import json
import cv2
import numpy as np
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()
        self.color_list={}
        self.index = 0
        self.files = []
        self.bCtrl = False
        self.zoom = 1
        self.att_data=self.readjson(os.path.join(os.getcwd(),"setting.json"))
        

    def setupUI(self):
        self.setMouseTracking(True)
        self.setWindowTitle("Labelme Att")
        self.resize(1800,1200)
        #self.setFixedWidth(1800)
        #self.setFixedHeight(1200)
        widget = QWidget(self)
        self.Mainlayout = QVBoxLayout(widget)
        self.canvas_layout = QHBoxLayout()
        self.scroll = QScrollArea()
        self.label = QLabel(self)
        self.label.setFixedSize(1500,1100)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setContentsMargins(10,10,10,10)
        self.scroll.setWidget(self.label)
        self.canvas_layout.addWidget(self.scroll)
        self.Mainlayout.addLayout(self.canvas_layout)
        #self.dock_layout=QHBoxLayout()
        self.make_toolbar()
        self.make_dock()
        





        self.setCentralWidget(widget)
    def make_dock(self):
        self.result_dock=QDockWidget("Result_list",self)
        self.result_dock.setFixedSize(200,250)
        self.addDockWidget(Qt.RightDockWidgetArea,self.result_dock)
        self.label_dock=QDockWidget("label_list",self)
        self.label_dock.setFixedSize(200,250)
        self.att_dock = QDockWidget("Attribute",self)
        self.att_dock.setFixedSize(200,250)
        self.addDockWidget(Qt.RightDockWidgetArea,self.label_dock)
        self.addDockWidget(Qt.RightDockWidgetArea,self.att_dock)

    def re_make_dock(self):
        self.result_dock=QDockWidget("Result_list",self)
        self.result_dock.setFixedSize(200,250)
        self.addDockWidget(Qt.RightDockWidgetArea,self.result_dock)
        self.label_dock=QDockWidget("label_list",self)
        self.label_dock.setFixedSize(200,250)
        self.addDockWidget(Qt.RightDockWidgetArea,self.label_dock)
        self.result_dock_list(list(self.files))


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
        self.open_file_list_button = QAction(self.style().standardIcon(QStyle.SP_ToolBarHorizontalExtensionButton),"Opne_File_List",self)
        self.open_file_list_button.setShortcut('Ctrl+L')
        self.open_file_list_button.triggered.connect(self.re_make_dock)
        self.raw_image_button = QAction(self.style().standardIcon(QStyle.SP_DialogHelpButton),"Raw_image",self)
        self.raw_image_button.setShortcut('Ctrl+T')
        self.raw_image_button.triggered.connect(self.open_raw)


        self.statusBar()

        self.toolbar = QToolBar()
        self.addToolBar(Qt.LeftToolBarArea,self.toolbar)
        self.toolbar.addAction(self.open_file_button)
        self.toolbar.addAction(self.open_folder_button)
        self.toolbar.addAction(self.next_button)
        self.toolbar.addAction(self.back_button)
        self.toolbar.addAction(self.open_file_list_button)
        self.toolbar.addAction(self.raw_image_button)      
    def open_file(self):
        print("open_file")
        self.select_files = QFileDialog.getOpenFileName(self,directory='./',caption="Select a data file",filter="Data File (*.jpg *.jpeg *.png)")
        if self.select_files != ('',''):
            self.files = self.select_files
            self.result_dock_list(list(self.files))
            self.image_load(self.files[self.index])
            self.att_dock_set()
    
    def readjson(self,jsonfile):
        with open(jsonfile) as jf:
            return json.load(jf)
    def image_load(self,file):
        #self.label.clear()
        #self.label.resize(1700,1000)
        self.img_raw= cv2.imread(file)
        self.img = cv2.cvtColor(self.img_raw,cv2.COLOR_BGR2RGB)
        self.img2 = self.img.copy()
        self.label.show()
        self.jsonfile=file.replace(file.split(".")[-1],"json")
        self.draw_img={}
        label_list=[]
        self.att_list=[]
        try:
            self.data = self.readjson(self.jsonfile)
            height=self.img.shape[0]/self.data['imageHeight']
            width=self.img.shape[1]/self.data['imageWidth']
            self.label_count = 0
            for labeling in self.data['shapes']:
                point_list = labeling['points']
                label = labeling['label']
                label_list.append(label)
                self.att_list.append(labeling['flags'])
                try:
                    if self.color_list[label]:
                        pass
                except:
                    self.color_list[label]=list(np.random.choice(range(256), size=3))
                points=[]
                for point in point_list:
                    points.append([point[0]*width,point[1]*height])
                self.draw_point(label,points)
        except Exception as e:
            print(e)
        try:
            self.label_dock_list(label_list)
            self.img = QImage(self.img.data,self.img.shape[1],self.img.shape[0],self.img.strides[0],QImage.Format_RGB888)
            self.image = QPixmap.fromImage(self.img).scaled(self.label.width(),self.label.height(),Qt.KeepAspectRatio,Qt.SmoothTransformation)
            self.current_image = self.img.copy()
            self.label.resize(self.image.width(),self.image.height())
            self.label.setPixmap(self.image)
            #self.draw_mask()
        except Exception as e:
            print(e)

    def draw_point(self,label,points):
        R = float(self.color_list[label][0])
        G = float(self.color_list[label][1])
        B = float(self.color_list[label][2])
        points=np.array(points,np.int32)
        self.copy_img = self.img2.copy()
        self.img = cv2.polylines(self.img,[points],True,(G,R,B),1)
        self.mask = self.copy_img*0
        self.mask = cv2.fillPoly(self.mask,[points],(G,R,B),1)
        self.draw_img[self.label_count]=self.mask
        self.label_count +=1

    def draw_mask(self):
        self.label_index = self.label_list.currentRow()
        try:
            self.att=self.att_list[self.label_index]
        except:
            self.att_list[self.label_index]={"color":"","materior":"","pattern":""}
            self.color_lb.setText("")
            self.materior_lb.setText("")
            self.pattern_lb.setText("")
        try:
            self.color_lb.setText(self.att["color"])
        except:
            self.color_lb.setText("")
        try:
            self.materior_lb.setText(self.att["materior"])
        except:
            self.materior_lb.setText("")
        try:
            self.pattern_lb.setText(self.att["pattern"])
        except:
            self.pattern_lb.setText("")
        self.mask_img= self.draw_img[self.label_index]
        self.mask_img=cv2.addWeighted(self.img2,0.6,self.mask_img,0.4,0)
        self.mask_img = QImage(self.mask_img.data,self.mask_img.shape[1],self.mask_img.shape[0],self.mask_img.strides[0],QImage.Format_RGB888)
        self.mask_image = QPixmap.fromImage(self.mask_img).scaled(self.label.width(),self.label.height(),Qt.KeepAspectRatio,Qt.SmoothTransformation)
        self.current_image = self.mask_img.copy()
        self.label.setPixmap(self.mask_image)
        self.data['shapes'][self.label_index]['flags'] = self.att_list[self.label_index]
    
    def open_raw(self):
        self.current_image = self.img.copy()
        self.image = QPixmap.fromImage(self.img).scaled(self.label.width(),self.label.height(),Qt.KeepAspectRatio,Qt.SmoothTransformation)
        self.label.setPixmap(self.image)
    
    def next_image(self):
        self.data_save(self.data)
        self.index +=1
        if self.index > len(self.files)-1:
            self.index -=1
        else:
            try:
                
                self.image_load(self.files[self.index])
            except:
                pass


    def back_image(self):
        self.data_save(self.data)
        self.index -=1
        if self.index <0:
            self.index += 1
        else:
            try:
                self.image_load(self.files[self.index])
            except:
                pass
    
    def data_save(self,data):
        with open(self.jsonfile,"w") as jf:
            json.dump(data,jf,indent=2)
        
    def result_dock_list(self,file_list):
        self.file_list = QListWidget()
        for file in file_list:
            self.file_list.addItem(file)
        self.result_dock.setWidget(self.file_list)
        self.result_dock.setFloating(False)

    def label_dock_list(self,label_list):
        self.label_list = QListWidget()
        for label in label_list:
            self.label_list.addItem(label)
        self.label_list.itemClicked.connect(self.draw_mask)
        self.label_dock.setWidget(self.label_list)
        self.label_dock.setFloating(False)

    def att_dock_set(self):
        self.att_widget = QWidget(self)
        self.att_dock_layout = QGridLayout(self)
        self.color_cb = QComboBox()
        self.color_cb.activated[str].connect(self.color_change)
        self.color_lb = QLabel()
        self.materior_cb = QComboBox()
        self.materior_cb.activated[str].connect(self.materior_change)
        self.materior_lb = QLabel()
        self.pattern_cb = QComboBox()
        self.pattern_cb.activated[str].connect(self.pattern_change)
        self.pattern_lb = QLabel()
        self.att_dock_layout.addWidget(self.color_lb,0,0)
        self.att_dock_layout.addWidget(self.materior_lb,1,0)
        self.att_dock_layout.addWidget(self.pattern_lb,2,0)
        self.att_dock_layout.addWidget(self.color_cb,0,1)
        self.att_dock_layout.addWidget(self.materior_cb,1,1)
        self.att_dock_layout.addWidget(self.pattern_cb,2,1)
        self.color_cb.addItems(self.att_data["attribute"]["color"])
        self.materior_cb.addItems(self.att_data["attribute"]["materior"])
        self.pattern_cb.addItems(self.att_data["attribute"]["pattern"])
        self.att_widget.setLayout(self.att_dock_layout)
        self.att_dock.setWidget(self.att_widget)
        self.att_dock.setFloating(False)

    def color_change(self):
        self.color_lb.setText(self.color_cb.currentText())
        self.att_list[self.label_index]['color'] = self.color_cb.currentText()
    def materior_change(self):
        self.materior_lb.setText(self.materior_cb.currentText())
        self.att_list[self.label_index]['materior'] = self.materior_cb.currentText()
    def pattern_change(self):
        self.pattern_lb.setText(self.pattern_cb.currentText())
        self.att_list[self.label_index]['pattern'] = self.pattern_cb.currentText()


    def open_folder(self):
        select_folder = QFileDialog.getExistingDirectory(self,"Choose Files",os.getcwd())
        self.files = []
        if select_folder:
            file_list = os.listdir(select_folder)
            for file in file_list:
                format = file.split(".")[-1].lower()
                if format =="jpg" or format =="jpeg" or format =="png":
                    self.files.append(os.path.join(select_folder,file))
            self.result_dock_list(self.files)
            self.image_load(self.files[self.index])
            self.att_dock_set()

    # def mouseButtonKind(self,buttons):
    #     if buttons & Qt.LeftButton:
    #         print("LEFT")
    #     if buttons & Qt.MidButton:
    #         print("MIDDLE")
    #     if buttons & Qt.RightButton:
    #         print("RIGHT")
    
    # def mousePressEvent(self,e):
    #     print('BUTTON PRESS')
    #     self.mouseButtonKind(e.buttons())

    # def mouseReleaseEvent(self,e):
    #     print("BUTTON RELEASE")
    #     self.mouseButtonKind(e.buttons())

    def wheelEvent(self,e):
        #print("wheel")
        #print(e.angleDelta().x(),e.angleDelta().y())
        if e.angleDelta().y() >0:
            self.zoom += 0.01
        else:
            self.zoom -= 0.01 
        try:
            if self.current_image and self.bCtrl:
                self.label.setFixedSize(1500*self.zoom,1100*self.zoom)
                self.label.setAlignment(Qt.AlignCenter)
                #self.label.resize(1700*self.zoom,1000*self.zoom)
                self.current_zoom_image = QPixmap.fromImage(self.current_image).scaled(self.label.width(),self.label.height(),Qt.KeepAspectRatio,Qt.SmoothTransformation)
                self.label.setPixmap(self.current_zoom_image)
        except:
            pass
    def keyPressEvent(self, event):
        if event.key()==16777249:
            self.bCtrl = True
            #print(f"{event.key()}:press")

    def keyReleaseEvent(self, event):
        if event.key()==16777249:
            self.bCtrl = False
            #print(f"{event.key()}:Release")

    # def processmultikeys(self,keyspressed):
    #     print(keyspressed)
        