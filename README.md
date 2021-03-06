# Python-Parking-Detection
 a Python GUI that monitors the actual occupancy of a specific parking slot
 
 ## Description:
The project is for parking slots vacancy detection. the user must specify and choose the slot he wants and then the program will detect if there is a car already parking on the parking slot or not.
The drawing functionality has been made with PyQt painter functions. while the detection was made by the YOLO pre trained weights.
 
 ### Requirements:
 * OpenCv
 * PyQt5
 * Shapely
 * NumPy
 
 ### Dataset:
 * Pre-trained YOLOv3 Tiny edition
 
 ### Usages:
 Download the video to use in the program, I used (https://www.youtube.com/watch?v=ymuYdUT5p7Q) as a refrence. If you want to use a live cam or the computer's webcam just change the `cap=cv2.VideoCapture("./videoplayback.mp4")` to `cap=cv2.VideoCapture(0)`. Then launch `start.py`.
 
 ### Screenshots : 
 #### main window
 ![alt text](https://github.com/FirasHabri/Python-Parking-Detection/blob/master/images/1.JPG)
 
 #### Select parking slots
 ![alt text](https://github.com/FirasHabri/Python-Parking-Detection/blob/master/images/3.JPG)
 
 #### Run parking vacancy detector
 ![alt text](https://github.com/FirasHabri/Python-Parking-Detection/blob/master/images/6.JPG)
 
 ### Acknowledgment
Big thanks to [  KhansaSaeed  ](https://github.com/KhansaSaeed/Car-Parking-OpenCV-Python-Rpi) for providing the base code.
 
