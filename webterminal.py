import os
from flask import Flask, render_template, session, redirect, url_for, request, jsonify, send_from_directory, abort
from flask_socketio import SocketIO, emit
import pexpect

app = Flask(__name__)
app.secret_key = 'SEGREDO-TROCAR'
socketio = SocketIO(app)

def load_users():
    users = {}
    users_file = os.path.join(os.path.dirname(__file__), 'users.txt')
    with open(users_file) as f:
        for line in f:
            if ':' in line:
                user, pwd = line.strip().split(':', 1)
                users[user] = pwd
    return users

USERS = load_users()
user_processes = {}

# LOGIN agora é a root /
@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']
        if USERS.get(u) == p:
            session['user'] = u
            return redirect(url_for('terminal'))
        else:
            error = "Login inválido! Verifique o username e a password."
    return render_template('login.html', error=error)

# TERMINAL em /terminal
@app.route('/terminal')
def terminal():
    if not session.get('user'):
        return redirect(url_for('login'))
    return render_template('terminal.html', username=session.get('user'))

@socketio.on('connect')
def connect():
    user = session.get('user')
    if not user:
        return False  
    if user not in user_processes:
        cmd = f"sudo -u {user} HOME=/users_homes/{user} python3 /app/main.py"
        proc = pexpect.spawn(cmd, encoding='utf-8', timeout=None)
        user_processes[user] = proc

@socketio.on('input')
def handle_input(data):
    user = session.get('user')
    if user in user_processes:
        proc = user_processes[user]
        proc.sendline(data['input'])

@socketio.on('get_output')
def handle_output():
    user = session.get('user')
    if user in user_processes:
        proc = user_processes[user]
        try:
            output = proc.read_nonblocking(size=1024, timeout=0.1)
            emit('output', {'output': output})
        except Exception:
            pass

@socketio.on('disconnect')
def disconnect():
    user = session.get('user')
    if user in user_processes:
        proc = user_processes[user]
        proc.terminate(force=True)
        del user_processes[user]

@app.route('/files')
def list_files():
    if not session.get('user'):
        return jsonify({"files": []})
    user = session['user']
    files = []
    base = f'/users_homes/{user}'
    for folder in ['cheatsheets', 'flashcards', 'resumos', 'quizzes']:
        dirpath = os.path.join(base, folder)
        if os.path.isdir(dirpath):
            for fname in os.listdir(dirpath):
                fpath = os.path.join(dirpath, fname)
                if os.path.isfile(fpath):
                    files.append({"folder": folder, "fname": fname})
    return jsonify({"files": files})

@app.route('/download/<folder>/<fname>')
def download_file(folder, fname):
    if not session.get('user'):
        return redirect(url_for('login'))
    user = session['user']
    allowed = ['cheatsheets', 'flashcards', 'resumos', 'quizzes']
    if folder not in allowed:
        abort(403)
    dirpath = os.path.join('/users_homes', user, folder)
    return send_from_directory(dirpath, fname, as_attachment=True)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=8081)
