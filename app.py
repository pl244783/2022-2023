from flask import Flask, render_template, request, redirect, session
#from robotLibrary import Robot
import logging
from time import sleep

app = Flask(__name__)
#robot = Robot()
app.secret_key = 'your-secret-key-here'

#run flask run --host=0.0.0.0

class ExcludeFilter(logging.Filter):
    def filter(self, record):
        return "GET /static/logFile.html" not in record.getMessage()

logger = logging.getLogger()
handler = logging.FileHandler('static/logFile.html', 'w')
handler.setLevel(logging.INFO)
handler.addFilter(ExcludeFilter())
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
 
@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html')
    else:
        return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with open('static/userFiles.txt', 'r') as f:
            for line1, line2 in zip(f, f):
                if username == line1.strip('\n') and password == line2.strip('\n'):
                    session['username'] = username
                    return redirect('/')
    
    return render_template('login.html')
    
# new registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        validUsername = True

        with open('static/userFiles.txt', 'r') as d:
            counter = 1
            for i in d:
                if counter%2 == 1:
                    print(i)
                    print(username)
                    if username == i.strip('\n'):
                        validUsername = False        
                counter += 1
        d.close()
            
        if validUsername:
            with open('static/userFiles.txt', 'a') as f:
                f.write(username + '\n' + password + '\n')

                return redirect('/login') 
        else: 
            return render_template('register.html')
    else: 
        return render_template('register.html')
 
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