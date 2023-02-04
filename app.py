from flask import Flask, request, render_template
#from robotLibrary import Robot
import logging
from time import sleep

app = Flask(__name__)
#robot = Robot()

#run flask run --host=0.0.0.0

logging.basicConfig(filename='static/logFile.html', level=logging.DEBUG, filemode = 'w')
 
logging.debug('Debug message')
logging.info('info message')
logging.warning('Warning message')

@app.route('/')
def index():
    return render_template('index.html')
 
@app.route("/forward", methods = ['GET'])
def forward():
    speedL = int(request.args.get('speedL', default = 50))
    speedR = int(request.args.get('speedR', default = 64))
    timeMS = int(request.args.get('timeMS', default = 1000))
    #robot.motorForward(speedL, speedR, timeMS)
    return "<p>forward</p>"

@app.route("/backward", methods = ['GET'])
def backward():
    speedL = int(request.args.get('speedL', default = 50))
    speedR = int(request.args.get('speedR', default = 66))
    timeMS = int(request.args.get('timeMS', default = 1000))
    #robot.motorBackward(speedL, speedR, timeMS)
    return "<p>backward</p>"

@app.route("/left", methods = ['GET'])
def left():
    speedL = int(request.args.get('speedL', default = 50))
    speedR = int(request.args.get('speedR', default = 60))
    timeMS = int(request.args.get('timeMS', default = 850))
    #robot.motorLeft(speedL, speedR, timeMS)
    return "<p>left</p>"

@app.route("/right", methods = ['GET'])
def right():
    speedL = int(request.args.get('speedL', default = 50))
    speedR = int(request.args.get('speedR', default = 60))
    timeMS = int(request.args.get('timeMS', default = 850))
    #robot.motorRight(speedL, speedR, timeMS)
    return "<p>right</p>"

if __name__=='__main__':
    app.run(host="0.0.0.0", port=8888, threaded=True, debug=True)