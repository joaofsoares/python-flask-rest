import functools
from flask import json
import ast

from werkzeug.security import check_password_hash, generate_password_hash

from flask import(
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash

from rest.db import get_db

bp = Blueprint("api", __name__, url_prefix="/api")


@bp.route("/users", methods=["GET"])
def get_users():
    if request.method == "GET":
        db = get_db()
        select_list = db.execute("SELECT username FROM user").fetchall()
        user_list = list(map(lambda u: u[0], select_list))

        if user_list is None:
            return "User not found."
        else:
            return "usernames:\n" + "\n".join(user_list)


@bp.route("/user/<username>", methods=["GET"])
def get_user(username):
    if request.method == "GET":
        db = get_db()

        if db.execute("SELECT username FROM user WHERE username = ?", (username,)).fetchone() is not None:
            return "User registered."
        else:
            return "User not found."


@bp.route("/user/add", methods=["POST"])
def add_user():
    if request.method == "POST":
        python_map = ast.literal_eval(json.dumps(request.json))
        username = python_map["username"]
        password = python_map["password"]

        if username and password:
            db = get_db()
            db.execute("INSERT INTO user (username, password) VALUES (?,?)",
                       (username, generate_password_hash(password)))
            db.commit()
            return "User registered."

        return "Invalid Information."
