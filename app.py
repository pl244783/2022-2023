from flask import request, render_template
import flask
import time
#from robotLibrary import Robot

app = flask.Flask(__name__)
#robot = Robot()

#run flask run --host=0.0.0.0

@app.route('/')
def index():
    return render_template('index.html')
 
@app.route("/forward", methods = ['GET'])
def forward():
    speedL = int(request.args.get('speedL', default = 50))
    speedR = int(request.args.get('speedR', default = 64))
    timeMS = int(request.args.get('timeMS', default = 1000))
    #robot.motorForward(speedL, speedR, timeMS)
    print("forward")
    return "<p>forward</p>"


@app.route("/backward", methods = ['GET'])
def backward():
    speedL = int(request.args.get('speedL', default = 50))
    speedR = int(request.args.get('speedR', default = 66))
    timeMS = int(request.args.get('timeMS', default = 1000))
    #robot.motorBackward(speedL, speedR, timeMS)
    print("backward")
    return "<p>backward</p>"

@app.route("/left", methods = ['GET'])
def left():
    speedL = int(request.args.get('speedL', default = 50))
    speedR = int(request.args.get('speedR', default = 60))
    timeMS = int(request.args.get('timeMS', default = 850))
    print("left")
    #robot.motorLeft(speedL, speedR, timeMS)
    return "<p>left</p>"

@app.route("/right", methods = ['GET'])
def right():
    speedL = int(request.args.get('speedL', default = 50))
    speedR = int(request.args.get('speedR', default = 60))
    timeMS = int(request.args.get('timeMS', default = 850))
    #robot.motorRight(speedL, speedR, timeMS)
    print("right")
    return "<p>right</p>"

if __name__=='__main__':
    app.run(debug = True)
