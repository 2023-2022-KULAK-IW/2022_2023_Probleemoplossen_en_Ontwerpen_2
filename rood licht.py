import cv2
import numpy as np
import serial.tools.list_ports
from scipy.optimize import fsolve

serialInst = serial.Serial()
ports = serial.tools.list_ports.comports()
port_list = []

start = "start"


def hoekV(afstandBeker):
    waterDebiet = 3.95  # l/min (3.95 is standaardwaarde), komt van waterflowsensor
    straal = 0.0029
    hoogtePlatform = 0.5
    lengteArm = 0.48
    afstandCamera = 0.02  # lengte tussen beginpunt arm en camera
    hoogteBeker = 0

    snelheid = (waterDebiet * 1.6667 * 10 ** (-5)) / (np.pi * (straal ** 2))

    def func(a):
        return [-afstandBeker + np.cos(a[0]) * snelheid * a[1] + np.cos(a[0]) * lengteArm - afstandCamera,
                -hoogteBeker + hoogtePlatform + np.sin(a[0]) * lengteArm + np.sin(a[0]) * snelheid * a[
                    1] - 1 / 2 * 9.81 * (a[1] ** 2)]

    opl = fsolve(func, [np.pi / 2, 10])
    opl[0] = opl[0] * 180 / np.pi
    # opl[0]: hoek (in graden)
    return opl[0]





def select_port():
    for onePort in ports:
        port_list.append(str(onePort))
        print(str(onePort))
    val = input("select port: ")
    for x in range(0, len(port_list)):
        if port_list[x].startswith("COM" + str(val)):
            portVal = "COM" + str(val)
        print(portVal)

    serialInst.baudrate = 9600
    serialInst.port = str("COM" + val)
    serialInst.open()


cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_EXPOSURE, -7)

object_height = 25
object_width = 6
objects_detected = 0
focal = 25
my_cam_angle = 60
angle_per_pixel = my_cam_angle / 640
lowerLimit = np.array([0, 0, 230])
upperLimit = np.array([179, 50, 255])
serialInst.write(str(start).encode("utf-8"))


def camera_mode():
    while True:
        ret, frame = cap.read()
        hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsvImage, lowerLimit, upperLimit)
        mask_contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for i in range(len(mask_contours)):
            cv2.drawContours(mask, mask_contours, i, (0, 255, 0), 3)

        if len(mask_contours) != 0:
            for mask_contour in mask_contours:
                area = cv2.contourArea(mask_contour)
                if area > 300:
                    x, y, w, h = cv2.boundingRect(mask_contour)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    middle = x + w / 2
                    angle_middle_horizontal = (middle - 320) * angle_per_pixel

                    if -0.5 < angle_middle_horizontal < 0.5:
                        angle_edge_horizontal = abs(abs((x - 320) * angle_per_pixel) - abs(angle_middle_horizontal))
                        object_on_screen = h * 0.02645833333
                        distance_focal = object_height * focal / object_on_screen
                        print("focal: " + str(distance_focal))
                        objects_detected += 1
                        hoek = hoekV(distance_focal)
                        print(hoek)
                        serialInst.write(str(hoek).encode("utf-8"))
                        cv2.waitKey(8000)

        cv2.imshow("hsv", mask)
        cv2.imshow("normal", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


cv2.destroyAllWindows()
cap.release()

def detect_light(image):
    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imshow("mask", gray)
    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply threshold to obtain binary image
    _, thresholded = cv2.threshold(blurred, 220, 255, cv2.THRESH_BINARY)
    cv2.imshow("", thresholded)
    # Find contours in the thresholded image
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    light_centers = []
    if len(contours) > 0:
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if 310 < x+w/2 < 330:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                calculate_distance(w, focal_length=25, object_width=100)




def calculate_distance(image_width, focal_length, object_width):
    distance = (object_width * focal_length) / image_width

# Open video capture
cap = cv2.VideoCapture(0)  # Use 0 for the default camera, or specify the camera index

while True:
    # Read frame from video capture
    ret, frame = cap.read()


    detect_light(frame)

    # Show the frame
    cv2.imshow('Light Detection', frame)

    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video capture and close windows
cap.release()
cv2.destroyAllWindows()
