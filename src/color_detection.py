# Multiple color detection: locates red, green and blue regions in the
# webcam feed and draws a labeled bounding box around each one.

import numpy as np
import cv2


def detect_color(mask, frame, color_bgr, label):
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 300:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), color_bgr, 2)
            cv2.putText(frame, label, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, color_bgr)


webcam = cv2.VideoCapture(0)
kernel = np.ones((5, 5), "uint8")

while True:
    _, image_frame = webcam.read()
    hsv_frame = cv2.cvtColor(image_frame, cv2.COLOR_BGR2HSV)

    red_lower = np.array([0, 50, 20], np.uint8)
    red_upper = np.array([5, 255, 255], np.uint8)
    red_mask = cv2.dilate(cv2.inRange(hsv_frame, red_lower, red_upper), kernel)

    green_lower = np.array([25, 52, 72], np.uint8)
    green_upper = np.array([102, 255, 255], np.uint8)
    green_mask = cv2.dilate(cv2.inRange(hsv_frame, green_lower, green_upper), kernel)

    blue_lower = np.array([94, 80, 2], np.uint8)
    blue_upper = np.array([120, 255, 255], np.uint8)
    blue_mask = cv2.dilate(cv2.inRange(hsv_frame, blue_lower, blue_upper), kernel)

    detect_color(red_mask, image_frame, (0, 0, 255), "Red Colour")
    detect_color(green_mask, image_frame, (0, 255, 0), "Green Colour")
    detect_color(blue_mask, image_frame, (255, 0, 0), "Blue Colour")

    cv2.imshow("Multiple Color Detection in Real-Time", image_frame)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

webcam.release()
cv2.destroyAllWindows()
