import cv2
import numpy as np

img = cv2.imread('stockphoto.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 50, 150, apertureSize=3)
lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi/180, threshold=60, minLineLength=1000, maxLineGap=50)

# parallelLines = []
# for i in range(len(lines)):
#     for j in range(i+1, len(lines)):
#         line1 = lines[i][0]
#         line2 = lines[j][0]
#         angle1 = np.arctan2(line1[1]-line1[3], line1[0]-line1[2]) * 180 / np.pi
#         angle2 = np.arctan2(line2[1]-line2[3], line2[0]-line2[2]) * 180 / np.pi
#         if np.abs(angle1 - angle2) < 5:
#             parallelLines.append((line1, line2))
#             print(line1, line2)

# def draw_line(img, x1, y1, x2, y2, colour, thickness):
#     nearBy = False
#     for other_line in parallelLines:
#         if (abs(other_line[0][0] - x1) < 100 and abs(other_line[0][1] - y1) < 100) or (abs(other_line[0][2] - x2) < 100 and abs(other_line[0][3] - y2) < 100):
#             nearBy = True
#             break
#     if nearBy:
#         colour = (0, 255, 0)
#     cv2.line(img, (x1, y1), (x2, y2), colour, thickness)

# for line in parallelLines:
#     cv2.line(img, (line[0][0], line[0][1]), (line[0][2], line[0][3]), (0, 255, 0), 2)
#     cv2.line(img, (line[1][0], line[1][1]), (line[1][2], line[1][3]), (0, 255, 0), 2)
#     #draw_line(img, int((line[0][0]+line[1][0])/2), int((line[0][1]+line[1][1])/2), int((line[0][2]+line[1][2])/2), int((line[0][3]+line[1][3])/2), (0, 0, 255), 2)

img = cv2.resize(edges, dsize=(1000,1000))
cv2.imshow('Result', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

