import cv2
import numpy as np

def nearBy(x1, y1, x2, y2):
    #left
    if (abs(refPointOne[2] - x1) < 150 and abs(refPointOne[3] - y1) < 150) or (abs(refPointOne[2] - x2) < 150 and abs(refPointOne[3] - y2) < 150):
        #cv2.line(img, (x1, y1), (x2, y2), (0, 255, 255), 1) 
        nearTrueMid(x1, y1, x2, y2)
    
    #right
    elif (abs(refPointTwo[2] - x1) < 150 and abs(refPointTwo[3] - y1) < 150) or (abs(refPointTwo[2] - x2) < 150 and abs(refPointTwo[3] - y2) < 150):
        #cv2.line(img, (x1, y1), (x2, y2), (0, 255, 255), 1) 
        nearTrueMid(x1, y1, x2, y2)
    
def nearTrueMid(x1, y1, x2, y2):
    if (abs(midPointCoord[0] - x1) < 50 and abs(midPointCoord[1] - y1) < 50) or (abs(midPointCoord[0] - x2) < 50 and abs(midPointCoord[1] - y2) < 50):
        cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 3) 

cap = cv2.VideoCapture('roadVideos/gitHubVideo1.mp4')

while cap.isOpened():
    ret, frame = cap.read()

    #theoretical perfect
    midPointCoord = [int(frame.shape[1]/2), int(frame.shape[0]/2), int(frame.shape[1]/2), int(frame.shape[0])]
    refPointOne = [int(frame.shape[1]/2)-10, int(frame.shape[0]/2), int(frame.shape[1]/4), int(frame.shape[0])]
    refPointTwo = [int(frame.shape[1]/2)+10, int(frame.shape[0]/2), int(frame.shape[1]/4)*3, int(frame.shape[0])]
    
    if ret:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 120, 200, apertureSize=3, L2gradient = True)
        lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi/180, threshold=50, minLineLength=7, maxLineGap=100)

        for line in lines:
            x1, y1, x2, y2 = line[0]
            nearBy(x1, y1, x2, y2)
            print(x1, x2, y1, y2)

        cv2.imshow("Circle Detection", frame)

        if cv2.waitKey(100) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()