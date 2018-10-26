import numpy as np
from PIL import ImageGrab
import cv2
import time
from scipy import signal


#for i in list(range(4)) [::-1]:
#    time.sleep(1)
def ObjectDetector(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_red = np.array([120,95,200])
    upper_red = np.array([170,255,255])
    mask = cv2.inRange(hsv, lower_red, upper_red)
    object_detected = cv2.bitwise_and(frame, frame, mask = mask)
    object_detected = cv2.cvtColor(object_detected, cv2.COLOR_BGR2RGB)
    return object_detected

def ObstacleDetector(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_green = np.array([37,110,85])
    upper_green = np.array([87,255,255])
    mask = cv2.inRange(hsv, lower_green, upper_green)
    obstacle_detected = cv2.bitwise_and(frame, frame, mask = mask)
    obstacle_detected = cv2.cvtColor(obstacle_detected, cv2.COLOR_BGR2RGB)
    return obstacle_detected

while (True):
    screen = np.array(ImageGrab.grab(bbox = (40,40, 540, 790)))

    #object detection
    #MASK
    _object = ObjectDetector(screen)
    _obstacle = ObstacleDetector(screen)

    cv2.imshow('object', _object)
    cv2.imshow('_obstacle',_obstacle)



    

    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break