from flask import request, redirect, url_for, render_template, session, flash, make_response
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
    username = session.get("username")

    if username is None:
        flash("Please log in first!", "danger")
        return redirect(url_for("users.login"))

    cookies = request.cookies
    return render_template("profile.html", username=username, cookies=cookies)

@user_bp.route("/logout", methods=["POST"])
def logout():
    session.pop("username", None)
    return redirect(url_for("users.login"))

@user_bp.route("/add-cookie", methods=["POST"])
def add_cookie():
    if "username" not in session:
        flash("Please log in first!", "danger")
        return redirect(url_for("users.login"))

    key = request.form.get("key", "").strip()
    value = request.form.get("value", "")
    max_age = request.form.get("max_age", type=int)

    if not key or max_age is None or max_age <= 0:
        flash("Введіть ключ і правильний термін дії!", "danger")
        return redirect(url_for("users.profile"))

    if key == "session":
        flash("Не можна змінювати службове кукі session!", "danger")
        return redirect(url_for("users.profile"))

    response = make_response(redirect(url_for("users.profile")))
    response.set_cookie(key, value, max_age=max_age)

    flash("Кукі успішно додано!", "success")
    return response

@user_bp.route("/delete-cookie", methods=["POST"])
def delete_cookie():
    if "username" not in session:
        flash("Please log in first!", "danger")
        return redirect(url_for("users.login"))

    key = request.form.get("key", "").strip()

    if not key:
        flash("Введіть ключ кукі!", "danger")
        return redirect(url_for("users.profile"))

    if key == "session":
        flash("Не можна видалити службове кукі session окремо!", "danger")
        return redirect(url_for("users.profile"))

    response = make_response(redirect(url_for("users.profile")))
    response.delete_cookie(key)

    flash("Кукі успішно видалено!", "success")
    return response

@user_bp.route("/delete-all-cookies", methods=["POST"])
def delete_all_cookies():
    if "username" not in session:
        flash("Please log in first!", "danger")
        return redirect(url_for("users.login"))

    response = make_response(redirect(url_for("users.profile")))

    for key in request.cookies:
        if key != "session":
            response.delete_cookie(key)

    flash("Усі користувацькі кукі успішно видалено!", "success")
    return response
