import cv2
import numpy as np

img = cv2.imread('roadPictures/homePhoto1.jpg')
img = cv2.GaussianBlur(img, (5, 5), 0)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 120, 200, apertureSize=3, L2gradient = True)
lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi/180, threshold=50, minLineLength=7, maxLineGap=100)

#theoretical perfect
midPointCoord = [int(img.shape[1]/2), int(img.shape[0]/2), int(img.shape[1]/2), int(img.shape[0])]
refPointOne = [int(img.shape[1]/2)-10, int(img.shape[0]/2), int(img.shape[1]/4), int(img.shape[0])]
refPointTwo = [int(img.shape[1]/2)+10, int(img.shape[0]/2), int(img.shape[1]/4)*3, int(img.shape[0])]

def nearBy(x1, y1, x2, y2):
    #left
    if (abs(refPointOne[2] - x1) < 200 and abs(refPointOne[3] - y1) < 200) or (abs(refPointOne[2] - x2) < 200 and abs(refPointOne[3] - y2) < 200):
        #cv2.line(img, (x1, y1), (x2, y2), (0, 255, 255), 1) 
        nearTrueMid(x1, y1, x2, y2)
    
    #right
    if (abs(refPointTwo[2] - x1) < 200 and abs(refPointTwo[3] - y1) < 200) or (abs(refPointTwo[2] - x2) < 200 and abs(refPointTwo[3] - y2) < 200):
        #cv2.line(img, (x1, y1), (x2, y2), (0, 255, 255), 1) 
        nearTrueMid(x1, y1, x2, y2)
    
def nearTrueMid(x1, y1, x2, y2):
    if (abs(midPointCoord[0] - x1) < 50 and abs(midPointCoord[1] - y1) < 50) or (abs(midPointCoord[0] - x2) < 50 and abs(midPointCoord[1] - y2) < 50):
        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 3) 

for line in lines:
    x1, y1, x2, y2 = line[0]
    nearBy(x1, y1, x2, y2)
    print(x1, x2, y1, y2)

#reference area
# cv2.line(img, (midPointCoord[0], midPointCoord[1]), (midPointCoord[2], midPointCoord[3]), (255, 0, 0), 1)
# cv2.line(img, (refPointOne[0], refPointOne[1]), (refPointOne[2], refPointOne[3]), (0, 255, 0), 1)
# cv2.line(img, (refPointTwo[0], refPointTwo[1]), (refPointTwo[2], refPointTwo[3]), (0, 255, 0), 1)

img = cv2.resize(edges, dsize=(500,500))
cv2.imshow('Result', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
