from flask import request, redirect, url_for, render_template, flash
from app import app
from app.forms import ContactForm
import logging
from pathlib import Path


@app.route("/")
def resume():
    return render_template("index.html", title='Резюме')


@app.route("/homepage")
def home():
    agent = request.user_agent
    return render_template("homepage.html", agent=agent)

data_folder = Path(__file__).resolve().parent / "data"
data_folder.mkdir(exist_ok=True)

contact_logger = logging.getLogger("contact_logger")
contact_logger.setLevel(logging.INFO)

if not contact_logger.handlers:
    handler = logging.FileHandler(data_folder / "contact_messages.log", encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
    contact_logger.addHandler(handler)

@app.route("/contacts", methods=["GET", "POST"])
def contacts():
    form = ContactForm()

    if form.validate_on_submit():
        try:
            contact_logger.info(
                "Ім'я: %s | Email: %s | Телефон: %s | Тема: %s | Повідомлення: %s",
                form.name.data,
                form.email.data,
                form.phone.data,
                form.subject.data,
                form.message.data
            )

            flash("Повідомлення успішно надіслано!", "success")
            return redirect(url_for("contacts"))

        except OSError:
            flash("Помилка під час збереження повідомлення.", "danger")

    elif request.method == "POST":
        flash("Перевірте правильність заповнення форми.", "danger")

    return render_template("contacts.html", form=form)
