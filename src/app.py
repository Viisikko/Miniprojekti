from flask import redirect, render_template, request, jsonify, flash, url_for, g, session
from config import app, test_env, user
from functools import wraps

def require_login():
    def login_wrapper(f):
        @wraps(f)
        def decorated_f(*args, **kwargs):
            if session:
                if session["user"] != None:
                    return f(*args, **kwargs)
            return redirect(url_for('login'), 302)
        return decorated_f
    return login_wrapper

@app.route("/")
@require_login()
def index():
    return render_template("index.html")

@app.route("/", methods=["POST"])
def login_post():
    if ("username" in request.form) and ("password" in request.form):
        if (request.form["username"] == user[0]) and (request.form["password"] == user[1]):
            session["user"] = user[0]
            return redirect(url_for("index"), 302)
    return "Väärä käyttäjätunnus tai salasana", 403

@app.route("/login")
def login():
    return render_template("login.html")
