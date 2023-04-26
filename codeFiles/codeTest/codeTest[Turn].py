import cv2
import numpy as np

# window_name = 'Image'
# image = cv2.imread('codeFiles/roadPictures/homePhoto2.jpg')

# # Polygon corner points coordinates
# pts = np.array([[200, 300], [200, 245], [200, 170], [150, 125], [75, 100]], np.int32)
 
# isClosed = False
# color = (0, 255, 0)
# thickness = 8
 
# image = cv2.polylines(image, [pts], isClosed, color, thickness)
 
# # Displaying the image
# image = cv2.resize(image, dsize=(900, 600))
# cv2.imshow('image', image)
# cv2.waitKey(10000)
# cv2.destroyAllWindows()

#all Github imgs work
img = cv2.imread('codeFiles/roadPictures/homePhoto2.jpg')
img = cv2.GaussianBlur(img, (5, 5), 0)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 120, 200, apertureSize=3)
lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi/180, threshold=50, minLineLength=0, maxLineGap=50)

#theoretical perfect
midPointCoord = [int(img.shape[1]/2), int(img.shape[0]/2)+int(img.shape[0]/8), int(img.shape[1]/2), int(img.shape[0])]
refPointOne = [int(img.shape[1]/2)-int(img.shape[1]/25), int(img.shape[0]/2)+int(img.shape[0]/8), int(img.shape[1]/4), int(img.shape[0])]
refPointTwo = [int(img.shape[1]/2)+int(img.shape[1]/25), int(img.shape[0]/2)+int(img.shape[0]/8), int(img.shape[1]/4)*3, int(img.shape[0])]

def nearBy(x1, y1, x2, y2):
    #left
    if (abs(refPointOne[2] - x1) < 170 and abs(refPointOne[3] - y1) < 170) or (abs(refPointOne[2] - x2) < 170 and abs(refPointOne[3] - y2) < 170):
        #cv2.line(img, (x1, y1), (x2, y2), (0, 255, 255), 1) 
        nearTrueMid(x1, y1, x2, y2, refPointOne[0])
    
    #right
    if (abs(refPointTwo[2] - x1) < 170 and abs(refPointTwo[3] - y1) < 170) or (abs(refPointTwo[2] - x2) < 170 and abs(refPointTwo[3] - y2) < 170):
        #cv2.line(img, (x1, y1), (x2, y2), (0, 255, 255), 1) 
        nearTrueMid(x1, y1, x2, y2, refPointTwo[0])

def nearTrueMid(x1, y1, x2, y2, direction):
    if (abs(midPointCoord[0] - x1) < 50 and abs(midPointCoord[1] - y1) < 50) or (abs(midPointCoord[0] - x2) < 50 and abs(midPointCoord[1] - y2) < 50):
        if y1 < midPointCoord[1]:
            cv2.line(img, (direction, midPointCoord[1]), (x2, y2), (0, 0, 255), 2)
        elif y2 < midPointCoord[1]:
            cv2.line(img, (x1, y1), (direction, midPointCoord[1]), (0, 0, 255), 2) 
        else: 
            cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2) 


for line in lines:
    x1, y1, x2, y2 = line[0]
    nearBy(x1, y1, x2, y2)

#reference area
# cv2.line(img, (midPointCoord[0], midPointCoord[1]), (midPointCoord[2], midPointCoord[3]), (255, 0, 0), 1)
# cv2.line(img, (refPointOne[0], refPointOne[1]), (refPointOne[2], refPointOne[3]), (0, 255, 0), 1)
# cv2.line(img, (refPointTwo[0], refPointTwo[1]), (refPointTwo[2], refPointTwo[3]), (0, 255, 0), 1)

img = cv2.resize(img, dsize=(500,500))
cv2.imshow('Static Image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
