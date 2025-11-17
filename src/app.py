from flask import redirect, render_template, request, jsonify, flash
from config import app, test_env

@app.route("/")
def index():
    return render_template("index.html")
