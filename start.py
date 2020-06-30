import sys
import os

from coordinates_generator import CoordinatesGenerator
from object_detector import ObjectDetector

from PyQt5.QtWidgets import QApplication,QMainWindow, QWidget
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer
from PyQt5 import QtCore, QtGui, QtWidgets

import cv2

class DetectionWindow():
    def __init__(self):
        self.data_file = "./coordinates.py"
        self.image_file = "./image.png"
        
        if os.stat(self.data_file).st_size == 0:
            self.setupCoordinates(self.image_file, self.data_file)
        
        else:
            self.launchParkingDetector() 
        
    def setupCoordinates(self, image_file, data_file):
        if image_file is not None:
            self.ex = CoordinatesGenerator(self.data_file, self.image_file)
    
    def launchParkingDetector(self):
        ob = ObjectDetector(self.data_file)
        ob.detect_motion()

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setupUI()
        self.timer = QTimer()
        self.timer.timeout.connect(self.viewCam)
        self.control_bt.clicked.connect(self.controlTimer)        
        self.capture_bt.clicked.connect(self.capture_image)
        
        self._image_counter = 0
    
    def setupUI(self):
        self.setGeometry(30, 50, 800, 500)
        self.setWindowTitle('Cam View')
        
        self.image_label = QtWidgets.QLabel(self)
        self.image_label.setObjectName("image_label")
        self.image_label.resize(640,480)
        
        self.control_bt = QtWidgets.QPushButton(self)
        self.control_bt.setObjectName("control_bt")
        self.control_bt.move(645, 200)
        self.control_bt.resize(150, 50)
        
        self.capture_bt = QtWidgets.QPushButton(self)
        self.capture_bt.setObjectName("capture_bt")
        self.capture_bt.move(645, 280)
        self.capture_bt.resize(150, 50) 
        
        self.control_bt.setText("Start")
        self.capture_bt.setText("Setup Parking")

    def viewCam(self):
        ret, image = self.cap.read()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width, channel = image.shape
        
        step = channel * width
        qImg = QImage(image.data, width, height, step, QImage.Format_RGB888)
        self.image_label.setPixmap(QPixmap.fromImage(qImg))

    def controlTimer(self):
        if not self.timer.isActive():
            self.cap = cv2.VideoCapture("./videoplayback.mp4")
            self.timer.start(20)
            self.control_bt.setText("Stop")
        else:
            self.timer.stop()
            self.cap.release()
            self.control_bt.setText("Start")
    
    def capture_image(self):
        try:
            flag, frame= self.cap.read()
            self.timer.stop()
            self.cap.release()
            self.control_bt.setText("Start")
            if flag:
                name = "image.png"
                cv2.imwrite(name, frame)
                self.uiD = DetectionWindow()
                self._image_counter += 1
        except Exception  as e:
            print(e)
            


if __name__ == '__main__':
    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)
    else:
        app = QtWidgets.QApplication.instance() 

    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(app.exec_())