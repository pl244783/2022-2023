import cv2
import numpy as np
import math

# #I don't know why my program needs this function, but when I try to delete it, it doesn't work anymore
def nearBy(x1, y1, x2, y2):
    #left
    if (abs(refPointOne[2] - x1) < frame.shape[1]/5 and abs(refPointOne[3] - y1) < frame.shape[0]/5) or (abs(refPointOne[2] - x2) < frame.shape[1]/5 and abs(refPointOne[3] - y2) < frame.shape[0]/5):
        return nearTrueMid(x1, y1, x2, y2, (0, 0, 255))
    
    #right
    elif (abs(refPointTwo[2] - x1) < frame.shape[1]/5 and abs(refPointTwo[3] - y1) < frame.shape[0]/5) or (abs(refPointTwo[2] - x2) < frame.shape[1]/5 and abs(refPointTwo[3] - y2) < frame.shape[0]/5):
        return nearTrueMid(x1, y1, x2, y2, (255, 0, 0))

def slopeCheck(x1, y1, x2, y2):
    if abs(x1-x2) < 0.001 or math.isinf(round(abs(y1-y2)/abs(x1-x2), 2)) or abs(round(abs(y1-y2)/abs(x1-x2), 2)) < 0.001 :
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

def nearTrueMid(x1, y1, x2, y2, colour):
    #cv2.line(frame, (midPointCoord[0], midPointCoord[1]), (int(midPointCoord[0] + frame.shape[1]/8), int(midPointCoord[1]+frame.shape[0]/8)), (255, 0, 0), 2)
    if (abs(midPointCoord[0] - x1) < frame.shape[1]/6 and abs(midPointCoord[1] - y1) < frame.shape[0]/6) or (abs(midPointCoord[0] - x2) < frame.shape[1]/6 and abs(midPointCoord[1] - y2) < frame.shape[1]/6):
        currentLineSlope = slopeCheck(x1, y1, x2, y2)
        #right
        if y1 < midPointCoord[1]:
            if currentLineSlope > 0.5 and currentLineSlope < 1:
                cv2.line(frame, (x1 + int(abs(y1-midPointCoord[1])/currentLineSlope), midPointCoord[1]), (x2 + int(abs(y2-midPointCoord[3])/currentLineSlope), midPointCoord[3]), colour, 2)
                return(x1 + int(abs(y1-midPointCoord[1])/currentLineSlope), midPointCoord[1], x2 + int(abs(y2-midPointCoord[3])/currentLineSlope), midPointCoord[3])

        #left
        elif y2 < midPointCoord[1]:
            if currentLineSlope > 0.5 and currentLineSlope < 1:
                cv2.line(frame, (x2 - int(abs(y2-midPointCoord[3])/currentLineSlope), midPointCoord[3]), (x2 - int(abs(y2-midPointCoord[1])/currentLineSlope), midPointCoord[1]), colour, 2) 
                return (x2 - int(abs(y2-midPointCoord[1])/currentLineSlope), midPointCoord[1], x2 - int(abs(y2-midPointCoord[3])/currentLineSlope), midPointCoord[3])
            

cap = cv2.VideoCapture('codeFiles/roadVideos/homeVideo6.mp4')

while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        #theoretical perfect
        midPointCoord = [int(frame.shape[1]/2), int(frame.shape[0]/2)+int(frame.shape[0]/10), int(frame.shape[1]/2), int(frame.shape[0])]
        refPointOne = [int(frame.shape[1]/2)-int(frame.shape[1]/20), int(frame.shape[0]/2)+int(frame.shape[0]/10), int(frame.shape[1]/4), int(frame.shape[0])]
        refPointTwo = [int(frame.shape[1]/2)+int(frame.shape[1]/20), int(frame.shape[0]/2)+int(frame.shape[0]/10), int(frame.shape[1]/4)*3, int(frame.shape[0])]

        #frame = cv2.GaussianBlur(frame, (3, 3), 0)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 250, apertureSize=3, L2gradient = True)
        lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi/180, threshold=50, minLineLength=0, maxLineGap=frame.shape[1])

        frameArray = []
        totalLines = 0 
        for line in lines:
            x1, y1, x2, y2 = line[0]
            if slopeCheck(x1, y1, x2, y2) > 0.5 and slopeCheck(x1, y1, x2, y2) < 1.5:
                #cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 255), 2)
                colour = (255, 255, 0)
                currentLineSlope = slopeCheck(x1, y1, x2, y2)
                if y1 < midPointCoord[1]:
                    cv2.line(frame, (x1 + int(abs(y1-midPointCoord[1])/currentLineSlope), midPointCoord[1]), (x2 + int(abs(y2-midPointCoord[3])/currentLineSlope), midPointCoord[3]), colour, 2)
                    totalLines += 1
                    #print(currentLineSlope)

                #left
                elif y2 < midPointCoord[1]:
                    cv2.line(frame, (x2 - int(abs(y2-midPointCoord[3])/currentLineSlope), midPointCoord[3]), (x2 - int(abs(y2-midPointCoord[1])/currentLineSlope), midPointCoord[1]), colour, 2) 
                    totalLines += 1
                    #print(currentLineSlope)


            # #______________________________________________________________-------------------------------------------------------______
            temp = tempCheck(nearBy(x1, y1, x2, y2))
            if temp is not None:
                frameArray.append(temp)
                    
        x1, y1, x2, y2 = 0, 0, 0, 0
        for value in frameArray:
            x1, y1, x2, y2 = int(value[0]) + x1, int(value[1]) + y1, int(value[2]) + x2, int(value[3]) + y2
        if len(frameArray) == 2:
            x1, y1, x2, y2 = x1/len(frameArray), y1/len(frameArray), x2/len(frameArray), y2/len(frameArray)
            cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)

        #------------------------------------------------------------------------------------------------------------------------------

        if totalLines > 3:
            print('going forwards')
            #has to cross 5 to
        else:
            height, width, channels = frame.shape
            half_width = width // 2
            leftHalf = frame[:, :half_width]
            rightHalf = frame[:, half_width:]

            # Calculate the noise level of each bottom quarter
            left_noise = cv2.meanStdDev(cv2.cvtColor(leftHalf, cv2.COLOR_BGR2GRAY))[1][0][0]
            right_noise = cv2.meanStdDev(cv2.cvtColor(rightHalf, cv2.COLOR_BGR2GRAY))[1][0][0]

            # Print the side with less noise
            if left_noise < right_noise:
                print("LEFT LFT LFT LFT LEFTTTT")
            else:
                print("Right")
            #get line detector working and then I just draw a line from my corner to th enext end 
            #or go from everything to the left of the detected lane and to the right of the other one


        # if len(frameArray) > 0:
        #     #print(frameArray, '\t', (x1, y1, x2, y2))
        #     print('forwards')
        #     pass
        # else:
        #     print('not forwards')

        # #reference area
        # cv2.line(frame, (midPointCoord[0], midPointCoord[1]), (midPointCoord[2], midPointCoord[3]), (255, 0, 0), 1)
        # cv2.line(frame, (refPointOne[0], refPointOne[1]), (refPointOne[2], refPointOne[3]), (0, 255, 0), 1)
        # cv2.line(frame, (refPointTwo[0], refPointTwo[1]), (refPointTwo[2], refPointTwo[3]), (0, 255, 0), 1)

        #frame = cv2.resize(frame, dsize = (1200, 800))
        frame = cv2.resize(frame, dsize = (900, 600))
        cv2.imshow("Road Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()