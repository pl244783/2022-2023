from flask import Flask, render_template, request, redirect, session
import logging
import hashlib

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

class ExcludeFilter(logging.Filter):
    def filter(self, record):
        return "GET /static/logFile.html" not in record.getMessage()

logger = logging.getLogger()
handler = logging.FileHandler('HTMLFiles/static/logFile.html', 'w')
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
                if username == line1.strip('\n') and hashlib.sha256(password.encode()).hexdigest() == line2.strip('\n'):
                    session['username'] = username
                    return redirect('/')
    
    return render_template('login.html')
    
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
                    if username == i.strip('\n'):
                        validUsername = False        
                counter += 1
        d.close()
            
        if validUsername:
            with open('static/userFiles.txt', 'a') as f:
                f.write(username + '\n' + hashlib.sha256(password.encode()).hexdigest() + '\n')
                return redirect('/login') 
        else: 
            return render_template('register.html')
    else: 
        return render_template('register.html')

if __name__=='__main__':
    app.run(host="0.0.0.0", port=8888, threaded=True, debug=True)
