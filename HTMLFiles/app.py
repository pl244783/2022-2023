from flask import Flask, render_template, request, redirect, session, Response, jsonify
import logging
import sqlite3, hashlib, base64
import cv2, math, numpy as np

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
    
def gen_frames(alternative):
    #I don't know why my program needs this function, but when I try to delete it, it doesn't work anymore
    def nearBy(x1, y1, x2, y2, currentLineSlope):
        if currentLineSlope > 0.5 and currentLineSlope < 1.2:
            #cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 255), 2)
            colour = (255, 255, 0)
            #right
            if y1 < midPointCoord[1] and x1 + int(abs(y1-midPointCoord[1])/currentLineSlope) > midPointCoord[0] and x2 + int(abs(y2-midPointCoord[3])/currentLineSlope) > midPointCoord[0]:
                slopeReset = slopeCheck(x1 + int(abs(y1-midPointCoord[1])/currentLineSlope), midPointCoord[1], x2 + int(abs(y2-midPointCoord[3])/currentLineSlope), midPointCoord[3])
                if slopeReset > 0.5 and slopeReset < 1.2:
                    cv2.line(frame, (x1 + int(abs(y1-midPointCoord[1])/currentLineSlope), midPointCoord[1]), (x2 + int(abs(y2-midPointCoord[3])/currentLineSlope), midPointCoord[3]), colour, 2)
                    return (x1 + int(abs(y1-midPointCoord[1])/currentLineSlope), midPointCoord[1], x2 + int(abs(y2-midPointCoord[3])/currentLineSlope), midPointCoord[3])
                    #print(currentLineSlope)

            #left
            elif y2 < midPointCoord[1] and x2 - int(abs(y2-midPointCoord[3])/currentLineSlope) < midPointCoord[0] and x2 - int(abs(y2-midPointCoord[1])/currentLineSlope) < midPointCoord[0]:
                slopeReset = slopeCheck(x2 - int(abs(y2-midPointCoord[3])/currentLineSlope), midPointCoord[3], x2 - int(abs(y2-midPointCoord[1])/currentLineSlope), midPointCoord[1])
                if slopeReset > 0.5 and slopeReset < 1.2: 
                    cv2.line(frame, (x2 - int(abs(y2-midPointCoord[3])/currentLineSlope), midPointCoord[3]), (x2 - int(abs(y2-midPointCoord[1])/currentLineSlope), midPointCoord[1]), colour, 2) 
                    return (x2 - int(abs(y2-midPointCoord[1])/currentLineSlope), midPointCoord[1], x2 - int(abs(y2-midPointCoord[3])/currentLineSlope), midPointCoord[3])
                #print(currentLineSlope)
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
            #theoretical perfect
            midPointCoord = [int(frame.shape[1]/2), int(frame.shape[0]/2)+int(frame.shape[0]/10), int(frame.shape[1]/2), int(frame.shape[0])]

            #frame = cv2.GaussianBlur(frame, (3, 3), 0)
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

            x1, y1, x2, y2 = 0, 0, 0, 0
            for value in frameArray:
                x1, y1, x2, y2 = int(value[0]) + x1, int(value[1]) + y1, int(value[2]) + x2, int(value[3]) + y2
            if len(frameArray) > 1:
                x1, y1, x2, y2 = x1/len(frameArray), y1/len(frameArray), x2/len(frameArray), y2/len(frameArray)
                cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)

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
                        savedValue = ('left')
                    else:
                        savedValue = ('right')
                print(savedValue)
            else:
                savedValue = 'forward'
                print(savedValue)

            if alternative == 0:
                #maybe frame
                frame = base64.b64encode(frame).decode('utf-8')
                data = {'frames': frame,
                    'direction': savedValue}
                yield data

            if alternative == 1:
                _, buffer = cv2.imencode('.jpg', frame)  
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                
            elif alternative == 2:
                yield (savedValue)

@app.route('/data_feed')
def data_feed():
    response = jsonify(next(gen_frames(0)))
    print(response)
    return response

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(1), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/prediction_feed')
def prediction_feed():
    return Response(gen_frames(2), mimetype='text/event-stream')

@app.route('/test_route')
def test_route():
    return render_template('test.html')


#------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------

if __name__=='__main__':
    app.run(host="0.0.0.0", port=8888, threaded=True, debug=True)
