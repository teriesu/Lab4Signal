import cv2
import numpy as np

def nothing(x):
    pass

cap = cv2.VideoCapture(0)
cv2.namedWindow("Trackbars")

cv2.createTrackbar("L – H", "Trackbars", 0, 179, nothing)
cv2.createTrackbar("L – S", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("L – V", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("U – H", "Trackbars", 179, 179, nothing)
cv2.createTrackbar("U – S", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("U – V", "Trackbars", 255, 255, nothing)

#Calibracion camara
def undistort(frame):
    fx = 689.45
    cx = 688.48
    fy = 324.77
    cy = 248.9
    k1, k2, p1, p2, k3 = 0.18226, -0.4574479, 689.44, 688.48, 0.0

    # Conversion matrix from camera coordinate system to pixel coordinate system
    k = np.array([
        [fx, 0, 0],
        [0, cx, 0],
        [fy, cy, 1]
    ])
    # Distortion coefficient
    d = np.array([
        k1, k2, p1, p2, k3
    ])
    h, w = frame.shape[:2]
    mapx, mapy = cv2.initUndistortRectifyMap(k, d, None, k, (w, h), 5)
    return cv2.remap(frame, mapx, mapy, cv2.INTER_LINEAR)
#Calibracion camara

while True:
    ret, frame = cap.read()
    hsv = cv2.cvtColor(undistort(frame), cv2.COLOR_BGR2HSV)

    l_h = cv2.getTrackbarPos("L – H", "Trackbars")
    l_s = cv2.getTrackbarPos("L – S", "Trackbars")
    l_v = cv2.getTrackbarPos("L – V", "Trackbars")
    u_h = cv2.getTrackbarPos("U – H", "Trackbars")
    u_s = cv2.getTrackbarPos("U – S", "Trackbars")
    u_v = cv2.getTrackbarPos("U – V", "Trackbars")

    lower_blue = np.array([l_h, l_s, l_v])
    upper_blue = np.array([u_h, u_s, u_v])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    result = cv2.bitwise_and( undistort(frame),  undistort(frame), mask=mask)

    cv2.imshow("frame",  undistort(frame))
    cv2.imshow("mask", mask)
    cv2.imshow("result", result)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
