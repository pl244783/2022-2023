import cv2
import numpy as np

def nearBy(x1, y1, x2, y2):
    #left
    if (abs(refPointOne[2] - x1) < 100 and abs(refPointOne[3] - y1) < 150) or (abs(refPointOne[2] - x2) < 100 and abs(refPointOne[3] - y2) < 150):
        nearTrueMid(x1, y1, x2, y2, refPointOne[0])
    
    #right
    elif (abs(refPointTwo[2] - x1) < 100 and abs(refPointTwo[3] - y1) < 150) or (abs(refPointTwo[2] - x2) < 100 and abs(refPointTwo[3] - y2) < 150):
        nearTrueMid(x1, y1, x2, y2, refPointTwo[0])
        
def nearTrueMid(x1, y1, x2, y2, direction):
    cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 255), 3)
    if (abs(midPointCoord[0] - x1) < 50 and abs(midPointCoord[1] - y1) < 50) or (abs(midPointCoord[0] - x2) < 50 and abs(midPointCoord[1] - y2) < 50):
        if y1 < midPointCoord[1]:
            cv2.line(frame, (direction, midPointCoord[1]), (x2, y2), (0, 0, 255), 2)
        elif y2 < midPointCoord[1]:
            cv2.line(frame, (x1, y1), (direction, midPointCoord[1]), (0, 0, 255), 2) 
        else: 
            cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 2) 
 

#1 sucks, 2 is tentative, 3 is trash
cap = cv2.VideoCapture('codeFiles/roadVideos/homeVideo5.mp4')

while cap.isOpened():
    ret, frame = cap.read()

    if ret:
        #theoretical perfect
        midPointCoord = [int(frame.shape[1]/2), int(frame.shape[0]/2)+int(frame.shape[0]/8), int(frame.shape[1]/2), int(frame.shape[0])]
        refPointOne = [int(frame.shape[1]/2)-int(frame.shape[1]/25), int(frame.shape[0]/2)+int(frame.shape[0]/8), int(frame.shape[1]/4), int(frame.shape[0])]
        refPointTwo = [int(frame.shape[1]/2)+int(frame.shape[1]/25), int(frame.shape[0]/2)+int(frame.shape[0]/8), int(frame.shape[1]/4)*3, int(frame.shape[0])]

        frame = cv2.GaussianBlur(frame, (7, 7), 0)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 120, 200, apertureSize=3)
        lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi/180, threshold=50, minLineLength=0, maxLineGap=1500)

        for line in lines:
            x1, y1, x2, y2 = line[0]
            nearBy(x1, y1, x2, y2)
            print(x1, x2, y1, y2)
        
        #reference area
        cv2.line(frame, (midPointCoord[0], midPointCoord[1]), (midPointCoord[2], midPointCoord[3]), (255, 0, 0), 1)
        cv2.line(frame, (refPointOne[0], refPointOne[1]), (refPointOne[2], refPointOne[3]), (0, 255, 0), 1)
        cv2.line(frame, (refPointTwo[0], refPointTwo[1]), (refPointTwo[2], refPointTwo[3]), (0, 255, 0), 1)

        frame = cv2.resize(frame, dsize = (500, 500))
        cv2.imshow("Road Detection", frame)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()