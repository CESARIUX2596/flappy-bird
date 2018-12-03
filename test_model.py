import numpy as np
from grabscreen import grab_screen
import cv2
import time
import os 
from scipy import signal
from getkeys import key_check
from alexnet import alexnet
from directkeys import PressKey, ReleaseKey, W

WIDTH = 81
HEIGHT = 73
LR = 1e-3
EPOCHS = 10
MODEL_NAME = 'aprende-a-seguir{}-{}-{}-el-pajarito-data.model'.format(LR, 'alexnetv2',EPOCHS)

def Up():
    PressKey(W)
    time.sleep(.05)
    ReleaseKey(W)
    
def Down():
    ReleaseKey(W)
    time.sleep(.05)

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
        cv2.circle(frame, (cX, cY), 5, (255, 0, 0), -1)
        cv2.circle(object_detected, (cX, cY), 15, (255, 0, 0), -1)
    except:
        pass
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    return frame, object_detected, cX, cY
 

def ObstacleDetector(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_green = np.array([37,110,85])
    upper_green = np.array([87,255,255])
    mask = cv2.inRange(hsv, lower_green, upper_green)
    obstacle_detected = cv2.bitwise_and(frame, frame, mask = mask)
    obstacle_detected = cv2.cvtColor(obstacle_detected, cv2.COLOR_BGR2RGB)
    return mask, obstacle_detected


def GapDetector(frame, obstacle, mask, _birdX):
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
                    #cv2.circle(obstacle, (cX, cY), 15, (0, 0, 255), -1)
                    #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                return frame, obstacle, cX, cY
                    
            except:
                pass
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return frame, obstacle, cX, cY

model = alexnet(WIDTH, HEIGHT, LR)
model.load(MODEL_NAME)

def main():
    for i in list(range(1)) [::-1]:
        print(i+1)
        time.sleep(1)

    while (True):
        screen = grab_screen(region=(0,0, 284 * 2, 512))
        #screen = np.array(ImageGrab.grab(bbox = (0,0, 284 * 2, 512)))

        _object, _objectOutput, _birdX, _birdY = ObjectDetector(screen)
        _obstacleMask, _obstacleOutput = ObstacleDetector(screen)
        _gap, _gapOutput, _gapX, _gapY = GapDetector(screen, _obstacleOutput,_obstacleMask,_birdX)
        #print('Bird ' +  str(_birdX) + ' ' + str(_birdY))
        #print('Gap ' + str(_gapX)+ ' ' + str(_gapY))
        total = np.zeros_like(screen)
        total = _objectOutput + _gapOutput
        _screenOut = cv2.cvtColor(total, cv2.COLOR_BGR2GRAY)
        _screenOut = cv2.resize(_screenOut, (73,81))

        prediction = model.predict([_screenOut.reshape(WIDTH,HEIGHT,1)])[0]
        moves = list(np.around(prediction))
        print(moves, prediction)
        if moves == [0]:
            Down()
        else:
            Up()



        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

if __name__ == '__main__':
    main()