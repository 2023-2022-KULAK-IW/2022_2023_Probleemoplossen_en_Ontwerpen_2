import cv2
import numpy as np
import serial.tools.list_ports

serialInst = serial.Serial()

portVal = "COM5"
ports = serial.tools.list_ports.comports()

port_list = []

for onePort in ports:
    port_list.append(str(onePort))
    print(str(onePort))

val = input("select port: ")
for x in range(0,len(port_list)):
    if port_list[x].startswith("COM" + str(val)):
        portVal = "COM" + str(val)
        print(portVal)

serialInst.baudrate = 9600
serialInst.port = portVal
serialInst.open()

cap = cv2.VideoCapture(0)

object_width = 7
objects_detected = 0
focal = 16
my_cam_angle = 60
angle_per_pixel = my_cam_angle/640
lowerLimit = np.array([160,150,50])
upperLimit = np.array([180,255,255])

while objects_detected < 3:
    ret, frame = cap.read()
    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsvImage, lowerLimit, upperLimit)
    mask_contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(mask_contours) != 0:
        for mask_contour in mask_contours:
            area = cv2.contourArea(mask_contour)
            if area > 300:
                x, y, w, h = cv2.boundingRect(mask_contour)
                middle = x + w / 2
                angle_middle_horizontal = (middle - 320) * angle_per_pixel

                if -0.5 < angle_middle_horizontal < 0.5:
                    angle_edge_horizontal = abs(abs((x-320) * angle_per_pixel) - abs(angle_middle_horizontal))
                    object_on_screen = w*0.02645833333
                    distance_focal = object_width * focal / object_on_screen
                    number = np.tan(angle_edge_horizontal*np.pi/180)
                    distance_angle = (object_width / 2) / number
                    distance = (distance_angle + distance_focal)/2
                    print("hoek: "+ str(distance_angle), "focal: " +str(distance_focal), "uiteindelijk: " +str(distance))
                    objects_detected += 1

                    serialInst.write(str(distance).encode("utf-8"))
                    cv2.waitKey(3000)

    cv2.imshow("hsv", mask)
    cv2.imshow("normal", frame)



    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
cap.release()

