# Single-color version of src/color_detection.py, kept for reference.

import numpy as np
import cv2

webcam = cv2.VideoCapture(0)

while True:
    _, image_frame = webcam.read()
    hsv_frame = cv2.cvtColor(image_frame, cv2.COLOR_BGR2HSV)

    red_lower = np.array([0, 50, 20], np.uint8)
    red_upper = np.array([5, 255, 255], np.uint8)
    red_mask = cv2.inRange(hsv_frame, red_lower, red_upper)

    kernel = np.ones((5, 5), "uint8")
    red_mask = cv2.dilate(red_mask, kernel)

    contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 300:
            x, y, w, h = cv2.boundingRect(contour)
            image_frame = cv2.rectangle(image_frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(image_frame, "Red Colour", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255))

    cv2.imshow("Multiple Color Detection in Real-Time", image_frame)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

webcam.release()
cv2.destroyAllWindows()
