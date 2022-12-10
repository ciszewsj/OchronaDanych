from flask import Flask, render_template, request, make_response, redirect
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import markdown
from collections import deque
from passlib.hash import sha256_crypt
import sqlite3

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)

app.secret_key = "206363ef77d567cc511df5098695d2b85058952afd5e2b1eecd5aed981805e60"

DATABASE = "./sqlite3.db"


class User(UserMixin):
    pass


@login_manager.user_loader
def user_loader(username):
    if username is None:
        return None

    db = sqlite3.connect(DATABASE)
    sql = db.cursor()
    ds = f"SELECT username, password FROM user WHERE username = '{username}'" #NOT_SAFE
    # ds = "SELECT username, password FROM user WHERE username = ?"
    print(ds)
    # sql.execute(ds)#NOT_SAFE
    # sql.execute(ds, [username])
    sql.execute(ds)

    row = sql.fetchone()
    try:
        username, password = row
    except:
        return None
    print("znaleziono : " + username + " " + password)

    user = User()
    user.id = username
    user.password = password
    return user


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = user_loader(username)
    return user


recent_users = deque(maxlen=3)


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("index.html")
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        print("Wprowadzono : " + username + " " + password)
        user = user_loader(username)
        print(user)
        if user is None:
            print("!@#?")
            return "Nieprawidłowy login lub hasło", 401
        if sha256_crypt.verify(password, user.password):
            print("PASSWORDS : " + password + " " + user.password)
            login_user(user)
            return redirect('/hello')
        else:
            print("TUTAJ>!@#?")
            return "Nieprawidłowy login lub hasło", 401


@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")


@app.route("/hello", methods=['GET'])
@login_required
def hello():
    if request.method == 'GET':
        print(current_user.id)
        username = current_user.id

        db = sqlite3.connect(DATABASE)
        sql = db.cursor()
        # sql.execute(f"SELECT id FROM notes WHERE username == '{username}'") - NOT_SAFE
        sql.execute("SELECT id FROM notes WHERE username == ?", [username])
        notes = sql.fetchall()

        return render_template("hello.html", username=username, notes=notes)


@app.route("/render", methods=['POST'])
@login_required
def render():
    md = request.form.get("markdown", "")
    rendered = markdown.markdown(md)
    # rendered = md
    username = current_user.id
    print("user_id" + username)
    db = sqlite3.connect(DATABASE)
    sql = db.cursor()
    ds = f"INSERT INTO notes (username, note) VALUES ('{username}', '{rendered}')"
    # ds = "INSERT INTO notes (username, note) VALUES (?, ?)"
    print(ds)
    # sql.execute(ds, [username, rendered])
    sql.execute(ds)
    db.commit()
    return render_template("markdown.html", rendered=rendered)


@app.route("/render/<rendered_id>")
@login_required
def render_old(rendered_id):
    db = sqlite3.connect(DATABASE)
    sql = db.cursor()
    # sql.execute(f"SELECT username, note FROM notes WHERE id == {rendered_id}")
    sql.execute("SELECT username, note FROM notes WHERE id == ?", [rendered_id])

    try:
        username, rendered = sql.fetchone()
        if username != current_user.id:
            return "Access to note forbidden", 403
        return render_template("markdown.html", rendered=rendered)
    except:
        return "Note not found", 404


if __name__ == "__main__":
    print("[*] Init database!")
    db = sqlite3.connect(DATABASE)
    sql = db.cursor()
    sql.execute("DROP TABLE IF EXISTS user;")
    sql.execute("CREATE TABLE user (username VARCHAR(32), password VARCHAR(128));")
    sql.execute("DELETE FROM user;")
    sql.execute(
        "INSERT INTO user (username, password) VALUES ('bach', '$5$rounds=535000$ZJ4umOqZwQkWULPh$LwyaABcGgVyOvJwualNZ5/qM4XcxxPpkm9TKh4Zm4w4');")
    sql.execute(
        "INSERT INTO user (username, password) VALUES ('john', '$5$rounds=535000$AO6WA6YC49CefLFE$dsxygCJDnLn5QNH/V8OBr1/aEjj22ls5zel8gUh4fw9');")
    sql.execute(
        "INSERT INTO user (username, password) VALUES ('bob', '$5$rounds=535000$.ROSR8G85oGIbzaj$u653w8l1TjlIj4nQkkt3sMYRF7NAhUJ/ZMTdSPyH737');")

    sql.execute("DROP TABLE IF EXISTS notes;")
    sql.execute("CREATE TABLE notes (id INTEGER PRIMARY KEY, username VARCHAR(32), note VARCHAR(256));")
    sql.execute("DELETE FROM notes;")
    sql.execute("INSERT INTO notes (username, note, id) VALUES ('bob', 'To jest sekret!', 1);")
    db.commit()

    app.run("0.0.0.0", 5000)
