import cv2
import numpy as np
import math

cars_cascade = cv2.CascadeClassifier('HTMLFiles/static/haarcascade_car.xml')

def detect_cars_and_pedestrain(frame):
    cars = cars_cascade.detectMultiScale(frame, 1.15, 4)
    for (x, y, w, h) in cars:
        cv2.rectangle(frame, (x+1, y+1), (x+w,y+h), color=(255, 0, 0), thickness=2)
        cv2.rectangle(frame, (x, y), (x+w, y+h), color=(0, 255, 0), thickness=2)

    return frame

def nearBy(x1, y1, x2, y2, currentLineSlope):
    if currentLineSlope > 0.5 and currentLineSlope < 1.2:
        colour = (255, 255, 0)
        if y1 < midPointCoord[1] and x1 + int(abs(y1-midPointCoord[1])/currentLineSlope) > midPointCoord[0] and x2 + int(abs(y2-midPointCoord[3])/currentLineSlope) > midPointCoord[0]:
            slopeReset = slopeCheck(x1 + int(abs(y1-midPointCoord[1])/currentLineSlope), midPointCoord[1], x2 + int(abs(y2-midPointCoord[3])/currentLineSlope), midPointCoord[3])
            if slopeReset > 0.5 and slopeReset < 1.2:
                cv2.line(frame, (x1 + int(abs(y1-midPointCoord[1])/currentLineSlope), midPointCoord[1]), (x2 + int(abs(y2-midPointCoord[3])/currentLineSlope), midPointCoord[3]), colour, 2)
                return (x1 + int(abs(y1-midPointCoord[1])/currentLineSlope), midPointCoord[1], x2 + int(abs(y2-midPointCoord[3])/currentLineSlope), midPointCoord[3])

        #left
        elif y2 < midPointCoord[1] and x2 - int(abs(y2-midPointCoord[3])/currentLineSlope) < midPointCoord[0] and x2 - int(abs(y2-midPointCoord[1])/currentLineSlope) < midPointCoord[0]:
            slopeReset = slopeCheck(x2 - int(abs(y2-midPointCoord[3])/currentLineSlope), midPointCoord[3], x2 - int(abs(y2-midPointCoord[1])/currentLineSlope), midPointCoord[1])
            if slopeReset > 0.5 and slopeReset < 1.2: 
                cv2.line(frame, (x2 - int(abs(y2-midPointCoord[3])/currentLineSlope), midPointCoord[3]), (x2 - int(abs(y2-midPointCoord[1])/currentLineSlope), midPointCoord[1]), colour, 2) 
                return (x2 - int(abs(y2-midPointCoord[1])/currentLineSlope), midPointCoord[1], x2 - int(abs(y2-midPointCoord[3])/currentLineSlope), midPointCoord[3])
    return 0

def slopeCheck(x1, y1, x2, y2):
    if (x1-x2) == 0:
        return 10000000
    if math.isinf(round(abs(y1-y2)/abs(x1-x2), 2)):
        return 10000
    elif abs(round(abs(y1-y2)/abs(x1-x2), 2)) < 0.01:
        return 100
    else:
        return round(abs(y1-y2)/abs(x1-x2), 2)

def tempCheck(temp):
    real = True
    if temp is not None and len(frameArray) == 1:
        for value in range(0, len(frameArray)):
            if abs(frameArray[value][0] - temp[0]) > frame.shape[1]/20:
                pass
            else:
                real = False
        if real:
            return temp
    elif temp is not None and len(frameArray) == 0:
        return temp
    return 0

cap = cv2.VideoCapture('codeFiles/roadVideos/homeVideo6.mp4')
lock, totalFrames, savedValue = 0, 0, 'stop'

while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        frameCounted = False
        midPointCoord = [int(frame.shape[1]/2), int(frame.shape[0]/2)+int(frame.shape[0]/10), int(frame.shape[1]/2), int(frame.shape[0])]
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 250, apertureSize=3)
        lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi/180, threshold=90, minLineLength=0, maxLineGap=frame.shape[1])
        
        frameArray = []
        totalLines, smallestLine = 0, [5*frame.shape[1], 5*frame.shape[1]] 
        for line in lines:
            x1, y1, x2, y2 = line[0]
            currentLineSlope = slopeCheck(x1, y1, x2, y2)
            temp = nearBy(x1, y1, x2, y2, currentLineSlope)
            if temp != 0:
                totalLines += 1
                if tempCheck(temp) != 0:
                    frameArray.append(temp)

            if currentLineSlope == 100 and y1 > midPointCoord[1] and (x1 + x2) > frame.shape[1]/2:
                #cv2.line(frame, (x1, y1), (x2, y2), (255, 255, 255), 2)
                if x1 < smallestLine[0] and x2 < smallestLine[1]:
                    smallestLine[0], smallestLine[1] = x1, x2
                frameCounted = True
                
        if frameCounted:
            totalFrames += 1
        else:
            totalFrames = 0
        if totalFrames >= 5:
            lock = 5    

        if lock > 0:
            if totalLines > 1:
                lock -= 1
            elif lock > 0:
                lock = 5
            
            if smallestLine[0] < frame.shape[1] * 5 and len(savedValue) == 7:
                if smallestLine[0] < frame.shape[1] - smallestLine[1] :
                    savedValue = ('probably turning left')
                else:
                    savedValue = ('probably turning right')
        else:
            savedValue = 'forwards'
        
        frame = detect_cars_and_pedestrain(frame)
        frame = cv2.resize(frame, dsize = (900, 600))
        cv2.imshow("Road Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()