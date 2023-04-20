from flask import Flask, render_template, request, redirect, session
import logging
import hashlib
import sqlite3

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

if __name__=='__main__':
    app.run(host="0.0.0.0", port=8888, threaded=True, debug=True)
