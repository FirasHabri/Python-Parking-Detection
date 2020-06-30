import numpy as np
import cv2
import re

class ObjectDetector:
    
    def __init__(self, output):
        self.coordinates = output
        self.ids = []
        self.coordinatesList = []
        
        self.readCoordinates(self.coordinates)
        
    def readCoordinates(self, coordinates):
        with open(coordinates, "r") as f:
            for x in f.readlines():
                if "id" in x:
                    self.ids.append(int(x.strip()[4:]))
                elif "coordinates" in x:
                    x = x.strip()[12:]
                    x = re.findall(r'\d+', x)
                    x = np.array(self.toInt(x))
                    x = np.reshape(x, (-1, 2))
                    
                    self.coordinatesList.append(x)
                                        
    def drawPolygons(self, interID, frame):
        for i in range(len(self.coordinatesList)): 
            if(i not in interID):
                cv2.polylines(frame,[self.coordinatesList[i]],True,(0,255,0),2) 
            else:
                cv2.polylines(frame,[self.coordinatesList[i]],True,(0,0,255),2)
            x,y = self.polygonCenter(self.coordinatesList[i])
            cv2.putText(frame,str(i),(int(x),int(y)),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2) 
            
        return frame
        
    def detect_motion(self):
        net = cv2.dnn.readNet("yolov3-tiny.weights", "yolov3-tiny.cfg")
        classes = ['car']
        
        layer_names = net.getLayerNames()
        outputlayers = [layer_names[i[0]-1] for i in net.getUnconnectedOutLayers()]
        
        
        cap=cv2.VideoCapture("./videoplayback.mp4")
        frame_id = 0
        
        while True:
            _,frame= cap.read() 
            frame = cv2.resize(frame, (800, 640))
            frame_id+=1
    
            height,width,channels = frame.shape
            
            #frame = self.drawPolygons(999, frame)
            
            blob = cv2.dnn.blobFromImage(frame,0.00392,(416,416),(0,0,0),True,crop=False)    
    
            net.setInput(blob)
            outs = net.forward(outputlayers)

            class_ids=[]
            confidences=[]
            boxes=[]
            red = []
            
            font = cv2.FONT_HERSHEY_PLAIN
            
            for out in outs:
                for detection in out:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                    if confidence > 0.1:
                        center_x= int(detection[0]*width)
                        center_y= int(detection[1]*height)
                        w = int(detection[2]*width)
                        h = int(detection[3]*height)

                        x=int(center_x - w/2)
                        y=int(center_y - h/2)
        
                        boxes.append([x,y,w,h])
                        confidences.append(float(confidence)) 
                        class_ids.append(class_id)

            indexes = cv2.dnn.NMSBoxes(boxes,confidences,0.1,0.1)
            
            for i in range(len(self.coordinatesList)):
                for k in range(len(boxes)):
                    x,y,w,h = boxes[k]
                                       
                    if(self.point_inside_polygon((x+w/2),(y+h/2),self.coordinatesList[i]) != False or
                       self.point_inside_polygon((x),(y),self.coordinatesList[i]) != False or
                       self.point_inside_polygon((x+w),(y),self.coordinatesList[i]) != False or
                       self.point_inside_polygon((x),(y+h),self.coordinatesList[i]) != False or
                       self.point_inside_polygon((x+w),(y+h),self.coordinatesList[i]) != False):
                        red.append(i)
                        
            frame = self.drawPolygons(set(red), frame)
            
            for i in range(len(boxes)):
                if i in indexes:
                    x,y,w,h = boxes[i]
                    label = str(classes[0])
                    confidence= confidences[i]
                    color = [255, 0, 0]
                    #cv2.rectangle(frame,(x,y),(x+w,y+h),color,2)
                    #cv2.putText(frame,label,(x,y+30),font,1,(255,255,255),2)
            
            cv2.imshow("Parking Detection",frame)
            key = cv2.waitKey(1)
            
            if key == 27:
                break;
            
        cap.release()    
        cv2.destroyAllWindows()
    
    def point_inside_polygon(self,x,y,poly):
        n = len(poly)
        inside =False
    
        p1x,p1y = poly[0]
        for i in range(n+1):
            p2x,p2y = poly[i % n]
            if y > min(p1y,p2y):
                if y <= max(p1y,p2y):
                    if x <= max(p1x,p2x):
                        if p1y != p2y:
                            xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x,p1y = p2x,p2y
    
        return inside
    
    def toInt(self,ls):
        for i in range(0, len(ls)): 
            ls[i] = int(ls[i])
        return ls
    
    def polygonCenter(self, ls):
        x_list = [ls[0][0], ls[1][0], ls[2][0], ls[3][0]]
        y_list = [ls[0][1], ls[1][1], ls[2][1], ls[3][1]]
        
        _x = sum(x_list) / 4
        _y = sum(y_list) / 4
        return(_x, _y)   
    
def main():
    ob = ObjectDetector("./coordinates.py")
    ob.detect_motion()
        
if __name__ == '__main__':
    main()