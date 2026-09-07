import cv2
import numpy as np

# Frame is split into a 3x3 grid; each zone is (top-left, bottom-right, label).
ZONES = [
    ((0, 0), (214, 160), "Top-Left"),
    ((214, 0), (428, 160), "Top"),
    ((428, 0), (640, 160), "Top-Right"),
    ((0, 160), (214, 320), "Left"),
    ((214, 160), (428, 320), "Center"),
    ((428, 160), (640, 320), "Right"),
    ((0, 320), (214, 480), "Bottom-Left"),
    ((214, 320), (428, 480), "Bottom"),
    ((428, 320), (640, 480), "Bottom-Right"),
]


def nothing(x):
    # required callback for cv2.createTrackbar
    pass


def area_location(start, stop, point, text):
    if (start[0] < point[0] < stop[0]) and (start[1] < point[1] < stop[1]):
        cv2.putText(frame, text, (100, 200), font, 1, black)


cap = cv2.VideoCapture(0)

cv2.namedWindow("Trackbars")
cv2.createTrackbar("L-H", "Trackbars", 0, 180, nothing)
cv2.createTrackbar("L-S", "Trackbars", 30, 255, nothing)
cv2.createTrackbar("L-V", "Trackbars", 206, 255, nothing)
cv2.createTrackbar("U-H", "Trackbars", 180, 180, nothing)
cv2.createTrackbar("U-S", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("U-V", "Trackbars", 255, 255, nothing)

black = (0, 0, 0)
red = (0, 0, 255)
green = (0, 255, 0)
blue = (255, 0, 0)
white = (255, 255, 255)

font = cv2.FONT_HERSHEY_COMPLEX

while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    l_h = cv2.getTrackbarPos("L-H", "Trackbars")
    l_s = cv2.getTrackbarPos("L-S", "Trackbars")
    l_v = cv2.getTrackbarPos("L-V", "Trackbars")
    u_h = cv2.getTrackbarPos("U-H", "Trackbars")
    u_s = cv2.getTrackbarPos("U-S", "Trackbars")
    u_v = cv2.getTrackbarPos("U-V", "Trackbars")

    lower_red = np.array([l_h, l_s, l_v])
    upper_red = np.array([u_h, u_s, u_v])

    mask = cv2.inRange(hsv, lower_red, upper_red)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.erode(mask, kernel)

    cv2.line(frame, (214, 0), (214, 480), blue, 3)
    cv2.line(frame, (428, 0), (428, 480), blue, 3)
    cv2.line(frame, (0, 160), (640, 160), blue, 3)
    cv2.line(frame, (0, 320), (640, 320), blue, 3)

    # Contours detection
    if int(cv2.__version__[0]) > 3:
        # Opencv 4.x.x
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    else:
        # Opencv 3.x.x
        _, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)
        x = approx.ravel()[0]
        y = approx.ravel()[1]

        # compute the center of the contour
        moments = cv2.moments(cnt)
        if moments["m00"] != 0:
            center_x = int(moments["m10"] / moments["m00"])
            center_y = int(moments["m01"] / moments["m00"])
        else:
            center_x, center_y = 0, 0

        if area > 400:
            if len(approx) == 4:
                cv2.drawContours(frame, [approx], 0, green, 5)
                cv2.drawContours(frame, [cnt], -1, (0, 255, 0), 2)
                cv2.circle(frame, (center_x, center_y), 7, (255, 255, 255), -1)
                cv2.putText(frame, "center", (center_x - 20, center_y - 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

                cv2.putText(frame, "Rectangle", (x, y), font, 1, red)

                for start, stop, label in ZONES:
                    area_location(start, stop, (center_x, center_y), label)
            else:
                cv2.putText(frame, "no shape detection", (10, 25), font, 1, white)

    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
