import cv2

cars_cascade = cv2.CascadeClassifier('codeFiles/codeReference/haarcascade_car.xml')

def detect_cars_and_pedestrain(frame):
    cars = cars_cascade.detectMultiScale(frame, 1.15, 4)
    for (x, y, w, h) in cars:
        cv2.rectangle(frame, (x+1, y+1), (x+w,y+h), color=(255, 0, 0), thickness=2)
        cv2.rectangle(frame, (x, y), (x+w, y+h), color=(0, 255, 0), thickness=2)
    
    return frame

def Simulator():
    CarVideo = cv2.VideoCapture('roadVideos/gitHubVideo1.mp4')
    while CarVideo.isOpened():
        ret, frame = CarVideo.read()
        controlkey = cv2.waitKey(1)
        if ret:        
            cars_frame = detect_cars_and_pedestrain(frame)
            cv2.imshow('frame', cars_frame)
        else:
            break
        if controlkey == ord('q'):
            break

    CarVideo.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    Simulator()