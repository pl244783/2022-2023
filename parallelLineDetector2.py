import cv2
import numpy as np

# Load the photo
img = cv2.imread('img6.jpg')

# Convert the photo to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply adaptive thresholding to binarize the image
thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

# Apply morphological operations to remove noise and fill gaps
kernel = np.ones((5,5),np.uint8)
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)

# Apply Hough Transform to detect lines
lines = cv2.HoughLinesP(closing, rho=1, theta=np.pi/180, threshold=100, minLineLength=50, maxLineGap=10)

# Find pairs of parallel lines
parallel_lines = []
for i in range(len(lines)):
    for j in range(i+1, len(lines)):
        line1 = lines[i][0]
        line2 = lines[j][0]
        angle1 = np.arctan2(line1[1]-line1[3], line1[0]-line1[2]) * 180 / np.pi
        angle2 = np.arctan2(line2[1]-line2[3], line2[0]-line2[2]) * 180 / np.pi
        if np.abs(angle1 - angle2) < 5:
            parallel_lines.append((line1, line2))

# Draw the detected lines on the photo
if len(parallel_lines) == 1:
    line = parallel_lines[0]
    cv2.line(img, (line[0][0], line[0][1]), (line[0][2], line[0][3]), (0, 255, 0), 2)
    cv2.line(img, (line[1][0], line[1][1]), (line[1][2], line[1][3]), (0, 255, 0), 2)

img = cv2.resize(img, dsize=(800,800))

# Show the result
cv2.imshow('Result', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
