import cv2
import numpy as np

# Load the photo
#use 5 is pretty good ,questionable 4, 2 is also questionable
#nvm 2 is peak
img = cv2.imread('bent2.jpg')

# Convert the photo to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply Canny edge detection
edges = cv2.Canny(gray, 50, 150, apertureSize=3)

# Apply Hough Transform to detect lines
lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi/180, threshold=100, minLineLength=0, maxLineGap=400)

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

def draw_line(img, x1, y1, x2, y2, colour, thickness):
    #var def uwu
    nearBy = False
    #checks for idk tbh close lines maybe
    for other_line in parallel_lines:
        if (abs(other_line[0][0] - x1) < 100 and abs(other_line[0][1] - y1) < 100) or (abs(other_line[0][2] - x2) < 100 and abs(other_line[0][3] - y2) < 100):
            nearBy = True
            break
    if nearBy:
        colour = (0, 255, 0)
    cv2.line(img, (x1, y1), (x2, y2), colour, thickness)

# Draw the detected lines on the photo
for line in parallel_lines:
    cv2.line(img, (line[0][0], line[0][1]), (line[0][2], line[0][3]), (0, 255, 0), 2)
    cv2.line(img, (line[1][0], line[1][1]), (line[1][2], line[1][3]), (0, 255, 0), 2)
    draw_line(img, int((line[0][0]+line[1][0])/2), int((line[0][1]+line[1][1])/2), int((line[0][2]+line[1][2])/2), int((line[0][3]+line[1][3])/2), (0, 0, 255), 2)
    #cv2.line(img, (int((line[0][0]+line[1][0])/2), int((line[0][1]+line[1][1])/2)), (int((line[0][2]+line[1][2])/2), int((line[0][3]+line[1][3])/2)), (0, 255, 0), 2)

# cv2.line(img, (line1[0], line1[1]), (line1[2], line1[3]), (0, 0, 255), 5)
# cv2.line(img, (line2[0], line2[1]), (line2[2], line2[3]), (0, 0, 255), 5)

#print((int((line[0][0]+line[1][0])/2), int((line[0][1]+line[1][1])/2)), line1, line2)

#maybe put this in an if statement
contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

#i love inefficienices!!!!!
for x in contours:
    print(x)
cv2.drawContours(img, contours, -1, (0, 255, 0), 3)

#comment this out when on school computer
img = cv2.resize(img, dsize=(500,500))
cv2.imshow('Result', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

#build idea, check for if the x y coord is within a specific value (read x and y > 10 of the prev)