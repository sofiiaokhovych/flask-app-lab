from flask import request, redirect, url_for, render_template, session, flash, make_response
from . import user_bp
from app import db, bcrypt
from app.models import User
from .forms import RegistrationForm, LoginForm
from flask_login import login_user, login_required, current_user, logout_user

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
    if current_user.is_authenticated:
        return redirect(url_for('users.account'))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = db.session.execute(
            db.select(User).filter_by(email=email)
        ).scalar_one_or_none()

        if user and user.check_password(password):
            login_user(user, remember=form.remember.data)
            flash('You logged in successfully!', 'success')
            return redirect(url_for('users.account'))

        flash("Error: Invalid email or password.", "danger")

    return render_template("login.html", form=form, title="Login")

@user_bp.route("/profile")
def profile():
    username = session.get("username")

    if username is None:
        flash("Please log in first!", "danger")
        return redirect(url_for("users.login"))

    cookies = request.cookies
    theme = request.cookies.get("profile_theme", "light")

    if theme not in ["light", "dark"]:
        theme = "light"

    return render_template("profile.html", username=username, cookies=cookies, theme=theme)

@user_bp.route('/logout', methods=["GET", "POST"])
def logout():
    logout_user()
    flash("You have successfully logged out.", "info")
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

@user_bp.route("/change-theme/<theme>")
def change_theme(theme):
    if "username" not in session:
        flash("Please log in first!", "danger")
        return redirect(url_for("users.login"))

    if theme not in ["light", "dark"]:
        flash("Невідома тема!", "danger")
        return redirect(url_for("users.profile"))

    response = make_response(redirect(url_for("users.profile")))
    response.set_cookie("profile_theme", theme, max_age=60 * 60 * 24 * 30)

    return response

@user_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', category='success')
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form, title='Register')

@user_bp.route("/account")
@login_required
def account():
    return render_template("account.html", user=current_user, title="Account")

@user_bp.route("/list")
@login_required
def users_list():
    users = db.session.scalars(db.select(User)).all()
    return render_template("users_list.html", users=users, title="Users List")