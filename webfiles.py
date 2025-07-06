from flask import Flask, send_from_directory, request, redirect, url_for, session, abort
import os

app = Flask(__name__)
app.secret_key = 'SEGREDO-SIMPLES-TROCAR'

# Ler users e passwords do ficheiro
def load_users():
    users = {}
    users_file = os.path.join(os.path.dirname(__file__), 'users.txt')
    with open(users_file) as f:
        for line in f:
            if ':' in line:
                u, p = line.strip().split(':', 1)
                users[u] = p
    return users

USERS = load_users()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if USERS.get(username) == password:
            session['user'] = username
            return redirect(url_for('myfiles'))
        return "Login inválido!", 403
    return '''
    <h2>Login</h2>
    <form method="post">
      Username: <input name="username"><br>
      Password: <input type="password" name="password"><br>
      <input type="submit" value="Entrar">
    </form>
    '''

@app.route('/myfiles')
def myfiles():
    if 'user' not in session:
        return redirect(url_for('login'))
    user = session['user']
    home = f'/users_homes/{user}'
    links = []
    for folder in ['cheatsheets', 'flashcards', 'resumos', 'quizzes']:
        dirpath = os.path.join(home, folder)
        if os.path.isdir(dirpath):
            for fname in os.listdir(dirpath):
                fpath = os.path.join(dirpath, fname)
                if os.path.isfile(fpath):
                    relpath = f"{folder}/{fname}"
                    links.append((folder, fname, relpath))
    html = "<h2>Os seus ficheiros:</h2><ul>"
    for folder, fname, relpath in links:
        html += f"<li>{folder}: <a href='/download/{folder}/{fname}'>{fname}</a></li>"
    html += "</ul><a href='/logout'>Logout</a>"
    return html

@app.route('/download/<folder>/<fname>')
def download(folder, fname):
    if 'user' not in session:
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
    app.run(host='0.0.0.0', port=8080)
