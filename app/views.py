from flask import request, redirect, url_for, render_template, abort
from app import app


@app.route("/")
def resume():
    return render_template("index.html", title='Резюме')


@app.route("/homepage")
def home():
    agent = request.user_agent
    return render_template("homepage.html", agent=agent)

@app.route('/contacts')
def contacts():
    return render_template('contacts.html', title='Контакти')
