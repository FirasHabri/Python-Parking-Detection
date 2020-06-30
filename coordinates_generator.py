from PyQt5.QtWidgets import (QApplication, QLabel, QWidget)
from PyQt5.QtWidgets import QApplication,QMainWindow, QMessageBox
from PyQt5.QtWidgets import QWidget, QPushButton
from PyQt5.QtGui import QImage, QPolygon
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import QTimer, QPoint
from PyQt5 import QtCore, QtGui, QtWidgets

from object_detector import ObjectDetector

class Polygon:
    def __init__(self,x1,y1,x2,y2,x3,y3,x4,y4):
        self.x1 = x1
        self.x2 = x2
        self.x3 = x3
        self.x4 = x4
        
        self.y1 = y1
        self.y2 = y2
        self.y3 = y3
        self.y4 = y4
        
    def getPoints(self):
        return self.x1,self.y1,self.x2,self.y2,self.x3,self.y3,self.x4,self.y4


class CoordinatesGenerator(QMainWindow):
    def __init__(self, output, image):
        super().__init__()
        self.output = output
        self.image = image
        
        self.initUI()
        
        f = open(self.output, "w").close()
        
    def initUI(self):
        self.setGeometry(30, 50, 800, 640)
        self.setWindowTitle('Detection Window')
        self.label = QLabel(self)
        self.label.resize(200, 40)  
        
        D_button = QPushButton('Finish', self)
        D_button.move(0, 00)
        D_button.resize(150, 50)
        
        R_button = QPushButton('Reset', self)
        R_button.move(160, 0)
        R_button.resize(150, 50)
        
        D_button.clicked.connect(self.startDetection)
        R_button.clicked.connect(self.on_click)
        
        self.show()
        
        self.Polygons = []
        self.points = QtGui.QPolygon()
        self.count = 0

    def mousePressEvent(self, e):
        self.points << e.pos()
        self.update()
        
    def paintEvent(self, ev):
        qp = QtGui.QPainter(self)
        pixmap = QPixmap(self.image)
        qp.drawPixmap(self.rect(), pixmap)
        qp.setRenderHint(QtGui.QPainter.Antialiasing)
        pen = QtGui.QPen(QtCore.Qt.blue, 2)
        qp.setPen(pen)
        
        qp.drawPolygon(self.points)
        with open(self.output, "a") as f:
            if(self.points.count() == 4):
                self.Polygons.append(Polygon(
                            self.points[0].x(),
                            self.points[0].y(),
                            
                            self.points[1].x(),
                            self.points[1].y(),
                            
                            self.points[2].x(),
                            self.points[2].y(),
                            
                            self.points[3].x(),
                            self.points[3].y()
                        ))
                
                self.outputCoordinates(self.count, self.Polygons[self.count], f)
                self.count += 1 
                self.points = QtGui.QPolygon()
        
        for i in range(len(self.Polygons)):
            self.drawPolygons(qp,self.Polygons[i])
            self.putText(qp,str(i),self.Polygons[i])
            
        
                
    def drawPolygons(self, painter, polygon):
        points = QPolygon([
            QPoint(polygon.x1,polygon.y1),
            QPoint(polygon.x2,polygon.y2),
            QPoint(polygon.x3,polygon.y3),
            QPoint(polygon.x4,polygon.y4)
        ])

        painter.drawPolygon(points)
        
    def outputCoordinates(self, id, polygon, f):
        f.write("-\n          id: " + str(id) + "\n          coordinates: [" +
                          "[" + str(polygon.x1) + "," + str(polygon.y1) + "]," +
                          "[" + str(polygon.x2) + "," + str(polygon.y2) + "]," +
                          "[" + str(polygon.x3) + "," + str(polygon.y3) + "]," +
                          "[" + str(polygon.x4) + "," + str(polygon.y4) + "]]\n")
    
    def on_click(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Are you sure you want to reset all inputs?")
        msgBox.setWindowTitle("Confirmation")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        
        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            self.resetStatus()
            
    def startDetection(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Do you confirm these coordiations?")
        msgBox.setWindowTitle("Confirmation")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        
        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            detector = ObjectDetector(self.output)
            detector.detect_motion()
            
    def resetStatus(self):
        self.Polygons = []
        self.points = QtGui.QPolygon()
        self.count = 0
        f = open(self.output, "w").close()
        
    
    def polygonCenter(self, polygon):
        x_list = [polygon.x1,polygon.x2,polygon.x3,polygon.x4]
        y_list = [polygon.y1,polygon.y2,polygon.y3,polygon.y4]
        
        _x = sum(x_list) / 4
        _y = sum(y_list) / 4
        return(_x, _y)
        
    def putText(self, qp, text, polygon):
        font = QFont()
        font.setFamily('Times')
        font.setBold(False)
        font.setPointSize(16)
        qp.setFont(font)
        
        x , y = self.polygonCenter(polygon)

        qp.drawText(x, y, text)
        
            
        