from flask import request, redirect, url_for, render_template, session, flash
from . import user_bp

CORRECT_USERNAME = "user1"
CORRECT_PASSWORD = "12345"

@user_bp.route("/hi/<string:name>")
def greetings(name):
    name = name.upper()
    age = request.args.get("age", None, type=int)

    return render_template("hi.html", name=name, age=age)

@user_bp.route("/admin")
def admin():
    to_url = url_for("users.greetings", 
                     name="administrator",
                     age=45,
                     _external=True
                     )
    print(to_url)
    return redirect(to_url)

@user_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == CORRECT_USERNAME and password == CORRECT_PASSWORD:
            session["username"] = username
            flash("Login successful!", "success")
            return redirect(url_for("users.profile"))
        else:
            flash("Wrong data! Try again!", "danger")
            return redirect(url_for("users.login"))

    return render_template("login.html")

@user_bp.route("/profile")
def profile():
    return render_template("profile.html", username="user1")
