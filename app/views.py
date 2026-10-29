from flask import request, redirect, url_for, render_template, abort, flash
from app import app
from app.forms import ContactForm


@app.route("/")
def resume():
    return render_template("index.html", title='Резюме')


@app.route("/homepage")
def home():
    agent = request.user_agent
    return render_template("homepage.html", agent=agent)

@app.route("/contacts", methods=["GET", "POST"])
def contacts():
    form = ContactForm()

    if form.validate_on_submit():
        try:
            with open("contact_messages.txt", "a", encoding="utf-8") as file:
                file.write(f"Ім'я: {form.name.data}\n")
                file.write(f"Email: {form.email.data}\n")
                file.write(f"Телефон: {form.phone.data}\n")
                file.write(f"Тема: {form.subject.data}\n")
                file.write(f"Повідомлення: {form.message.data}\n")
                file.write("------------------------\n")

            flash("Повідомлення успішно надіслано!", "success")
            return redirect(url_for("contacts"))

        except OSError:
            flash("Помилка під час збереження повідомлення.", "danger")

    elif request.method == "POST":
        flash("Перевірте правильність заповнення форми.", "danger")

    return render_template("contacts.html", form=form)
