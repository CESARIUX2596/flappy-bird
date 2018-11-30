import numpy as np
from PIL import ImageGrab
import cv2
import time
import os 
from scipy import signal

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (900,0)
def ObjectDetector(frame):
    cX = 0 
    cY = 0
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_yellow = np.array([90,235,60])
    upper_yellow = np.array([110,255,255])
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    #Returns only the object in RBG
    object_detected = cv2.bitwise_and(frame, frame, mask = mask)
    #object_detected = cv2.medianBlur(object_detected, 3)
    object_detected = cv2.cvtColor(object_detected, cv2.COLOR_BGR2RGB)
    try: 
        #Centroid of the bird :D
        M = cv2.moments(mask)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        #print (cX,cY)
        cv2.circle(frame, (cX, cY), 5, (0, 0, 255), -1)
    except:
        pass
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    return frame, cX, cY
 
def ObstacleDetector(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_green = np.array([37,110,85])
    upper_green = np.array([87,255,255])
    mask = cv2.inRange(hsv, lower_green, upper_green)
    #obstacle_detected = cv2.bitwise_and(frame, frame, mask = mask)
    #obstacle_detected = cv2.cvtColor(obstacle_detected, cv2.COLOR_BGR2RGB)
    return mask

def GapDetector(frame, mask, _birdX):
    cX = 0 
    cY = 0
    _, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    #count = 0
    for contour in contours:
        area = cv2.contourArea(contour)
        if area < 1850:
            try:
                #cv2.drawContours(frame, contour, -1, (0, 0, 255), 10)
                M = cv2.moments(contour)
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                if cX > _birdX:
                    cX = cX+35
                    cY = cY-75
                    cv2.circle(frame, (cX, cY), 5, (0, 0, 255), -1)
                    #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                return frame, cX, cY
                    
            except:
                pass
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return frame, cX, cY

while (True):
    screen = np.array(ImageGrab.grab(bbox = (0,0, 284 * 2, 512)))
    
    _object, _birdX, _birdY = ObjectDetector(screen)
    _obstacleMask = ObstacleDetector(screen)
    _gap, _gapX, _gapY = GapDetector(screen,_obstacleMask,_birdX)
    print('Bird ' +  str(_birdX) + ' ' + str(_birdY))
    print('Gap ' + str(_gapX)+ ' ' + str(_gapY))
    cv2.imshow('_obstacle',_gap)



    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break