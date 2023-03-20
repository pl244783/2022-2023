import cv2
import numpy as np

# Load the photo
#use 1, 2, 6
img = cv2.imread('test.jpg')

# Convert the photo to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply Canny edge detection
edges = cv2.Canny(gray, 50, 150, apertureSize=3)

# Apply Hough Transform to detect lines
lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi/180, threshold=100, minLineLength=200, maxLineGap=1000)

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
            print(line1, line2)

# Draw the detected lines on the photo
for line in parallel_lines:
    cv2.line(img, (line[0][0], line[0][1]), (line[0][2], line[0][3]), (0, 255, 0), 2)
    cv2.line(img, (line[1][0], line[1][1]), (line[1][2], line[1][3]), (0, 255, 0), 2)
    cv2.line(img, (int((line[0][0]+line[1][0])/2), int((line[0][1]+line[1][1])/2)), (int((line[0][2]+line[1][2])/2), int((line[0][3]+line[1][3])/2)), (0, 255, 255), 2)

# cv2.line(img, (line1[0], line1[1]), (line1[2], line1[3]), (0, 0, 255), 5)
# cv2.line(img, (line2[0], line2[1]), (line2[2], line2[3]), (0, 0, 255), 5)

#print((int((line[0][0]+line[1][0])/2), int((line[0][1]+line[1][1])/2)), line1, line2)

#comment this out when on school computer
img = cv2.resize(img, dsize=(900,900))

# Show the result
cv2.imshow('Result', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
