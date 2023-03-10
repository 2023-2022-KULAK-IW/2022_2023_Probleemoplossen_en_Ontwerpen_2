import numpy as np
import cv2

def get_limits(color):

    c = np.uint8([[color]])
    hsvC = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)

    lowerLimit = hsvC[0][0][0] + 160, 95, 111
    upperLimit = hsvC[0][0][0] + 180, 255, 255

    lowerLimit = np.array(lowerLimit,dtype = np.uint8)
    upperLimit = np.array(upperLimit,dtype = np.uint8)

    return lowerLimit, upperLimit
