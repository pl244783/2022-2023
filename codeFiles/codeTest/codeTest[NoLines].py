import cv2
import numpy as np
import math

#I don't know why my program needs this function, but when I try to delete it, it doesn't work anymore
def nearBy(x1, y1, x2, y2):
    #left
    if (abs(refPointOne[2] - x1) < frame.shape[0]/4 and abs(refPointOne[3] - y1) < frame.shape[0]/5) or (abs(refPointOne[2] - x2) < frame.shape[0]/4 and abs(refPointOne[3] - y2) < frame.shape[0]/5):
        return nearTrueMid(x1, y1, x2, y2, (0, 0, 255))
    
    #right
    elif (abs(refPointTwo[2] - x1) < frame.shape[0]/4 and abs(refPointTwo[3] - y1) < frame.shape[0]/5) or (abs(refPointTwo[2] - x2) < frame.shape[0]/4 and abs(refPointTwo[3] - y2) < frame.shape[0]/5):
        return nearTrueMid(x1, y1, x2, y2, (0, 0, 255))

def nearTrueMid(x1, y1, x2, y2, colour):
    #cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
    if (abs(midPointCoord[0] - x1) < frame.shape[0]/5 and abs(midPointCoord[1] - y1) < frame.shape[0]/5)or (abs(midPointCoord[0] - x2) < frame.shape[0]/5 and abs(midPointCoord[1] - y2) < frame.shape[0]/5):
        currentLineSlope = slopeCheck(x1, y1, x2, y2)
        #right
        if y1 < midPointCoord[1]:
            if slopeCheck(x1 + int(abs(y1-midPointCoord[1])/currentLineSlope), midPointCoord[1], x2, y2) > 0.5:
                cv2.line(frame, (x1 + int(abs(y1-midPointCoord[1])/currentLineSlope), midPointCoord[1]), (x2 + int(abs(y2-midPointCoord[3])/currentLineSlope), midPointCoord[3]), colour, 2)
                return(x1 + int(abs(y1-midPointCoord[1])/currentLineSlope), midPointCoord[1], x2 + int(abs(y2-midPointCoord[3])/currentLineSlope), midPointCoord[3])

        #left
        elif y2 < midPointCoord[1]:
            if slopeCheck(x1, y1, x2 - int(abs(y2-midPointCoord[1])/currentLineSlope), midPointCoord[1]) > 0.5:
                cv2.line(frame, (x2 - int(abs(y2-midPointCoord[3])/currentLineSlope), midPointCoord[3]), (x2 - int(abs(y2-midPointCoord[1])/currentLineSlope), midPointCoord[1]), colour, 2) 
                return (x2 - int(abs(y2-midPointCoord[1])/currentLineSlope), midPointCoord[1], x2 - int(abs(y2-midPointCoord[3])/currentLineSlope), midPointCoord[3])

def slopeCheck(x1, y1, x2, y2):
    if math.isinf(round(abs(y1-y2)/abs(x1-x2), 2)) or abs(round(abs(y1-y2)/abs(x1-x2), 2)) < 0.001 :
        return 10000
    else:
        return round(abs(y1-y2)/abs(x1-x2), 2)

def tempCheck(temp):
    real = True
    if temp is not None and len(frameArray) == 1:
        for value in range(0, len(frameArray), 2):
            if abs(int(frameArray[0][value]) - int(temp[value])) > frame.shape[1]/50:
                pass
            else:
                real = False
        if real:
            return temp
    elif temp is not None and len(frameArray) == 0:
        return temp

#1 pog, 2 is tentative, 3 is trash - github
#4 home
cap = cv2.VideoCapture('codeFiles/roadVideos/gitHubVideo1.mp4')

while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        #theoretical perfect
        midPointCoord = [int(frame.shape[1]/2), int(frame.shape[0]/2)+int(frame.shape[0]/10), int(frame.shape[1]/2), int(frame.shape[0])]
        refPointOne = [int(frame.shape[1]/2)-int(frame.shape[1]/20), int(frame.shape[0]/2)+int(frame.shape[0]/10), int(frame.shape[1]/4), int(frame.shape[0])]
        refPointTwo = [int(frame.shape[1]/2)+int(frame.shape[1]/20), int(frame.shape[0]/2)+int(frame.shape[0]/10), int(frame.shape[1]/4)*3, int(frame.shape[0])]

        #frame = cv2.GaussianBlur(frame, (7, 7), 0)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 250, apertureSize=3)
        lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi/180, threshold=50, minLineLength=0, maxLineGap=frame.shape[1])

        frameArray = []

        for line in lines:
            x1, y1, x2, y2 = line[0]
            if y1 - int(frame.shape[0]/2)-int(frame.shape[0]/10) < 50 and y2 - int(frame.shape[0]/2)-int(frame.shape[0]/10) < 50:
                pass
            else:
                if slopeCheck(x1, y1, x2, y2) > 0.5 and slopeCheck(x1, y1, x2, y2) < 1.5:
                    cv2.line(frame, (x1, y1), (x2, y2), (255, 255, 255), 2)
                pass
            temp = tempCheck(nearBy(x1, y1, x2, y2))
            if temp is not None:
                frameArray.append(temp)
                    
        # x1, y1, x2, y2 = 0, 0, 0, 0
        # for value in frameArray:
        #     x1, y1, x2, y2 = int(value[0]) + x1, int(value[1]) + y1, int(value[2]) + x2, int(value[3]) + y2
        # if len(frameArray) == 2:
        #     x1, y1, x2, y2 = x1/len(frameArray), y1/len(frameArray), x2/len(frameArray), y2/len(frameArray)
        #     cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)

        if len(frameArray) > 0:
            #print(frameArray, '\t', (x1, y1, x2, y2))
            print('forwards')
            pass
        else:
            print('not forwards')

        #reference area
        cv2.line(frame, (midPointCoord[0], midPointCoord[1]), (midPointCoord[2], midPointCoord[3]), (255, 0, 0), 1)
        cv2.line(frame, (refPointOne[0], refPointOne[1]), (refPointOne[2], refPointOne[3]), (0, 255, 0), 1)
        cv2.line(frame, (refPointTwo[0], refPointTwo[1]), (refPointTwo[2], refPointTwo[3]), (0, 255, 0), 1)

        frame = cv2.resize(frame, dsize = (1200, 800))
        #frame = cv2.resize(frame, dsize = (900, 600))
        cv2.imshow("Road Detection", frame)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()