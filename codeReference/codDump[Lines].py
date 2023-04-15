import cv2
import numpy as np

img = cv2.imread('gitHubPhoto1.jpg')
#img = cv2.GaussianBlur(img, (5, 5), 0)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 120, 200, apertureSize=3, L2gradient = True)
lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi/180, threshold=50, minLineLength=7, maxLineGap=1)

for line in lines:
    x1, y1, x2, y2 = line[0]
    cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

img = cv2.resize(img, dsize=(500,500))
cv2.imshow('Result', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
