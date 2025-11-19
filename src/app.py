from flask import redirect, render_template, request, jsonify, flash, url_for, g, session
from config import app, test_env, user
from functools import wraps
import references

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
    references_list = references.get_all_references()
    return render_template("index.html", references=references_list)

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

@app.route("/add_reference")
@require_login()
def add_reference():
    return render_template("add_reference.html")

@app.route("/create_reference", methods=["POST"])
@require_login()
def create_reference():
    title = request.form.get("title", "").strip()
    type_ = request.form.get("type", "").strip()
    year_raw = request.form.get("year", "").strip()
    author = request.form.get("author", "").strip()

    if not title or len(title) > 64:
        return "Error: Title must be between 1 and 64 characters.<br> <a href='/add_reference'>Return to reference creation</a>"

    if not type_ or type_ != "book":
        return "Error: Invalid type.<br> <a href='/add_reference'>Return to reference creation</a>"

    if not year_raw:
        return "Error: Year is required.<br> <a href='/add_reference'>Return to reference creation</a>"

    try:
        year = int(year_raw)
    except ValueError:
        return "Error: Year must be a number.<br> <a href='/add_reference'>Return to reference creation</a>"

    if year < 868 or year > 2099:
        return "Error: Year cannot be under 868 or too much in the future.<br> <a href='/add_reference'>Return to reference creation</a>"
    
    if not author or len(author)<3:
        return "Error: Author must be at least 3 characters long.<br> <a href='/add_reference'>Return to reference creation</a>"
    
    reference_id=references.add_reference(title, type_, year, author)

    if not reference_id:
        return "Error: Could not create reference", 500
    
    return redirect("/")
