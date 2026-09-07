import cv2
import numpy as np

drone_cam = cv2.VideoCapture(0)

red = (0, 0, 255)
blue = (255, 0, 0)
green = (0, 255, 0)

while True:
    _, frame = drone_cam.read()
    frame = cv2.flip(frame, 1)
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Red-mask extraction, left disabled while the HSV thresholds were
    # still being tuned for the competition bottle's exact shade of red.
    """
    low_red = np.array([160, 20, 70])
    #low_red = np.array([0, 50, 50])
    #low_red = np.array([161, 155, 84])
    high_red = np.array([179, 255, 255])
    red_mask = cv2.inRange(hsv_frame, low_red, high_red)
    red = cv2.bitwise_and(frame, frame, mask=red_mask)
    """

    cv2.imshow("drone_cam", frame)

    key = cv2.waitKey(1)
    if key & 0xFF == ord("q") or key & 0xFF == ord("Q"):  # exit when Q or q is pressed
        break

drone_cam.release()
cv2.destroyAllWindows()
