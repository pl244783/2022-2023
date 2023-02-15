from flask import Flask, request, render_template
# from robotLibrary import Robot
import logging
#from camera import CameraStream
#import cv2
import time


app = Flask(__name__)
# robot = Robot()

# run flask run --host=0.0.0.0

logging.basicConfig(filename='static/logFile.html', level=logging.INFO, filemode = 'w')
log = logging.getLogger('"GET /static/logFile.html HTTP/1.1" 200')
log.setLevel(logging.ERROR)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/forward", methods=['GET'])
def forward():
    speedL = int(request.args.get('speedL', default=50))
    speedR = int(request.args.get('speedR', default=64))
    timeMS = int(request.args.get('timeMS', default=1000))
    # robot.motorForward(speedL, speedR, timeMS)

    return "<p>forward</p>"

@app.route("/backward", methods=['GET'])
def backward():
    speedL = int(request.args.get('speedL', default=50))
    speedR = int(request.args.get('speedR', default=66))
    timeMS = int(request.args.get('timeMS', default=1000))
    # robot.motorBackward(speedL, speedR, timeMS)
    return "<p>backward</p>"


@app.route("/left", methods=['GET'])
def left():
    speedL = int(request.args.get('speedL', default=50))
    speedR = int(request.args.get('speedR', default=60))
    timeMS = int(request.args.get('timeMS', default=850))
    # robot.motorLeft(speedL, speedR, timeMS)
    return "<p>left</p>"

@app.route("/right", methods=['GET'])
def right():
    speedL = int(request.args.get('speedL', default=50))
    speedR = int(request.args.get('speedR', default=60))
    timeMS = int(request.args.get('timeMS', default=850))
    # robot.motorRight(speedL, speedR, timeMS)
    return "<p>right</p>"

def gen_frame():
    while cap:
        frame = cap.read() #calls class read method
        convert = cv2.imencode('.jpg', frame)[1].tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + convert + b'\r\n')

@app.route('/video_feed') #endpoint where raw video feed is streamed
def video_feed():
    return Response(gen_frame(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8888, threaded=True, debug=True)
