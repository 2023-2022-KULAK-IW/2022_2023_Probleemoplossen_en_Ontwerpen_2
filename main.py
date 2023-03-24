import cv2
from PIL import Image

from util import get_limits

yellow = [0,0,0]#yellow in BGR colorspace

cap = cv2.VideoCapture(1)
while True:
    ret, frame = cap.read()

    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lowerLimit, upperLimit = get_limits(color=yellow)

    mask = cv2.inRange(hsvImage, lowerLimit, upperLimit)

    mask_ = Image.fromarray(mask)

    bbox = mask_.getbbox()
    if bbox is not None:
        x1, y1, x2, y2 = bbox

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 5)
        grootte = (x2-x1, y2-y1)
        distancex = 0.0005*grootte[0]**2 - 0.4006*grootte[0] + 100.71
        distancey = y = 0.0528*grootte[1]**2 - 4.191*grootte[1] + 104.21
        distance = (distancey+ distancex)/2

        print(distance)



    cv2.imshow('frame', frame)



    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()

cv2.destroyAllWindows()