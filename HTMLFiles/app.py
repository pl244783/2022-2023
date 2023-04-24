from flask import Flask, render_template, request, redirect, session, Response
import logging
import hashlib
import sqlite3
import cv2
import numpy as np
import math

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

class ExcludeFilter(logging.Filter):
    def filter(self, record):
        message = record.getMessage()
        return "GET /static/" not in message and "GET /video_feed" not in message and "GET /image?" not in message and "GET /imaging?" not in message
    
logger = logging.getLogger()
handler = logging.FileHandler('HTMLFiles/static/logFile.html', 'w')
handler.setLevel(logging.INFO)
handler.addFilter(ExcludeFilter())
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Initialize the database
def init_db():
    conn = sqlite3.connect('HTMLFiles/static/user_data.db')
    c = conn.cursor()

    # Create the users table if it doesn't exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')

    conn.commit()
    conn.close()

init_db()

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

        # Check if the username and password match
        conn = sqlite3.connect('HTMLFiles/static/user_data.db')
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username=? AND password=?', (hashlib.sha256(username.encode()).hexdigest(), hashlib.sha256(password.encode()).hexdigest()))
        result = c.fetchone()
        conn.close()

        if result:
            session['username'] = result[1]
            return redirect('/')
    
    return render_template('login.html')
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        validUsername = True

        # Check if the username is available
        conn = sqlite3.connect('HTMLFiles/static/user_data.db')
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username=?', (username,))
        result = c.fetchone()

        if result:
            validUsername = False
        else:
            # Insert the new user into the database
            c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (hashlib.sha256(username.encode()).hexdigest(), hashlib.sha256(password.encode()).hexdigest()))
            conn.commit()

        conn.close()

        if validUsername:
            return redirect('/login') 
        else: 
            return render_template('register.html')
    else: 
        return render_template('register.html')
    
def gen_frames():
    #I don't know why my program needs this function, but when I try to delete it, it doesn't work anymore
    def nearBy(x1, y1, x2, y2):
        #left
        if (abs(refPointOne[2] - x1) < frame.shape[0]/5 and abs(refPointOne[3] - y1) < frame.shape[0]/5) or (abs(refPointOne[2] - x2) < frame.shape[0]/5 and abs(refPointOne[3] - y2) < frame.shape[0]/5):
            return nearTrueMid(x1, y1, x2, y2, (0, 0, 255))
        
        #right
        elif (abs(refPointTwo[2] - x1) < frame.shape[0]/5 and abs(refPointTwo[3] - y1) < frame.shape[0]/5) or (abs(refPointTwo[2] - x2) < frame.shape[0]/5 and abs(refPointTwo[3] - y2) < frame.shape[0]/5):
            return nearTrueMid(x1, y1, x2, y2, (0, 0, 255))

    def nearTrueMid(x1, y1, x2, y2, colour):
        #cv2.line(frame, (x1, y1), (x2, y2), (255, 255, 255), 2)
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
        if math.isinf(round(abs(y1-y2)/abs(x1-x2), 2)):
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
    
    cap = cv2.VideoCapture('codeFiles/roadVideos/gitHubVideo1.mp4')
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            midPointCoord = [int(frame.shape[1]/2), int(frame.shape[0]/2)+int(frame.shape[0]/10), int(frame.shape[1]/2), int(frame.shape[0])]
            refPointOne = [int(frame.shape[1]/2)-int(frame.shape[1]/25), int(frame.shape[0]/2)+int(frame.shape[0]/10), int(frame.shape[1]/4), int(frame.shape[0])]
            refPointTwo = [int(frame.shape[1]/2)+int(frame.shape[1]/25), int(frame.shape[0]/2)+int(frame.shape[0]/10), int(frame.shape[1]/4)*3, int(frame.shape[0])]

            frame = cv2.GaussianBlur(frame, (7, 7), 0)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 120, 200, apertureSize=3)
            lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi/180, threshold=50, minLineLength=0, maxLineGap=frame.shape[1])

            frameArray = []

            for line in lines:
                x1, y1, x2, y2 = line[0]
                temp = tempCheck(nearBy(x1, y1, x2, y2))
                if temp is not None:
                    frameArray.append(temp)
                        
            x1, y1, x2, y2 = 0, 0, 0, 0
            for value in frameArray:
                x1, y1, x2, y2 = int(value[0]) + x1, int(value[1]) + y1, int(value[2]) + x2, int(value[3]) + y2
            if len(frameArray) == 2:
                x1, y1, x2, y2 = x1/len(frameArray), y1/len(frameArray), x2/len(frameArray), y2/len(frameArray)
                cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)

            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

#-----------------------------------------------------------------------------

def nonEdited(img):
    image = cv2.imread(img)
    _, buffer = cv2.imencode('.jpg', image)
    img = buffer.tobytes()
    yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n\r\n')

@app.route('/image')
def image():
    img = request.args.get('img', type=str)
    return Response(nonEdited(img), mimetype='multipart/x-mixed-replace; boundary=frame')

def edited(image):
    img = cv2.imread(image)
    img = cv2.GaussianBlur(img, (5, 5), 0)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 120, 200, apertureSize=3)
    lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi/180, threshold=50, minLineLength=0, maxLineGap=50)

    #theoretical perfect
    midPointCoord = [int(img.shape[1]/2), int(img.shape[0]/2)+int(img.shape[0]/8), int(img.shape[1]/2), int(img.shape[0])]
    refPointOne = [int(img.shape[1]/2)-int(img.shape[1]/25), int(img.shape[0]/2)+int(img.shape[0]/8), int(img.shape[1]/4), int(img.shape[0])]
    refPointTwo = [int(img.shape[1]/2)+int(img.shape[1]/25), int(img.shape[0]/2)+int(img.shape[0]/8), int(img.shape[1]/4)*3, int(img.shape[0])]

    def nearBy(x1, y1, x2, y2):
        #left
        if (abs(refPointOne[2] - x1) < 170 and abs(refPointOne[3] - y1) < 170) or (abs(refPointOne[2] - x2) < 170 and abs(refPointOne[3] - y2) < 170):
            #cv2.line(img, (x1, y1), (x2, y2), (0, 255, 255), 1) 
            nearTrueMid(x1, y1, x2, y2, refPointOne[0])
        
        #right
        if (abs(refPointTwo[2] - x1) < 170 and abs(refPointTwo[3] - y1) < 170) or (abs(refPointTwo[2] - x2) < 170 and abs(refPointTwo[3] - y2) < 170):
            #cv2.line(img, (x1, y1), (x2, y2), (0, 255, 255), 1) 
            nearTrueMid(x1, y1, x2, y2, refPointTwo[0])

    def nearTrueMid(x1, y1, x2, y2, direction):
        if (abs(midPointCoord[0] - x1) < 50 and abs(midPointCoord[1] - y1) < 50) or (abs(midPointCoord[0] - x2) < 50 and abs(midPointCoord[1] - y2) < 50):
            if y1 < midPointCoord[1]:
                cv2.line(img, (direction, midPointCoord[1]), (x2, y2), (0, 0, 255), 2)
            elif y2 < midPointCoord[1]:
                cv2.line(img, (x1, y1), (direction, midPointCoord[1]), (0, 0, 255), 2) 
            else: 
                cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2) 

    for line in lines:
        x1, y1, x2, y2 = line[0]
        nearBy(x1, y1, x2, y2)

    _, buffer = cv2.imencode('.jpg', img)
    img = buffer.tobytes()
    yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n\r\n')

@app.route('/imaging')
def imaging():
    image = request.args.get('image', type=str)
    return Response(edited(image), mimetype='multipart/x-mixed-replace; boundary=frame')

# ---------------------------------------------------------------------

if __name__=='__main__':
    app.run(host="0.0.0.0", port=8888, threaded=True, debug=True)
