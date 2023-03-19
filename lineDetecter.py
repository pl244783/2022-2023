import cv2
import numpy as np

# Load the image
img = cv2.imread('img1.jpg')

# Convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply Canny edge detection
edges = cv2.Canny(gray, 50, 150, apertureSize=3)

# Apply Hough Transform to detect lines
lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi/180, threshold=50, minLineLength=200, maxLineGap=1000)

# Draw the detected lines on the original image
for line in lines:
    x1, y1, x2, y2 = line[0]
    cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

#comment this out when on school computer
img = cv2.resize(img, dsize=(500,500))

# Show the result
cv2.imshow('Result', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
