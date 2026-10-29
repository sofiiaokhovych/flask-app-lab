from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp


class ContactForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[
            DataRequired(message="Введіть ім'я."),
            Length(min=4, max=10, message="Ім'я має містити від 4 до 10 символів.")
        ]
    )

    email = StringField(
        "Email",
        validators=[
            DataRequired(message="Введіть email."),
            Email(message="Введіть правильну електронну адресу.")
        ]
    )

    phone = StringField(
        "Phone",
        validators=[
            DataRequired(message="Введіть номер телефону."),
            Regexp(
                r"^\+380\d{9}$",
                message="Формат телефону: +380XXXXXXXXX."
            )
        ]
    )

    subject = SelectField(
        "Subject",
        choices=[
            ("", "Оберіть тему"),
            ("question", "Запитання"),
            ("cooperation", "Співпраця"),
            ("feedback", "Відгук")
        ],
        validators=[
            DataRequired(message="Оберіть тему повідомлення.")
        ]
    )

    message = TextAreaField(
        "Message",
        validators=[
            DataRequired(message="Введіть повідомлення."),
            Length(max=500, message="Повідомлення має містити не більше 500 символів.")
        ]
    )

    submit = SubmitField("Send Message")
