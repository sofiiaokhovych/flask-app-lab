from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Regexp

from app import db
from app.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=4, max=14, message="Username має бути довжиною від 4 до 14 символів."),
        Regexp(r'^[A-Za-z][A-Za-z0-9_.]*$', message="Username має починатися з літери та містити лише літери, цифри, крапки або підкреслення.")])

    email = StringField('Email', validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6, message="Пароль має містити щонайменше 6 символів.")
    ])

    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message="Паролі не збігаються.")
    ])

    submit = SubmitField('Register')

    def validate_username(self, username):
        user = db.session.execute(
            db.select(User).filter_by(username=username.data)
        ).scalar_one_or_none()
        if user:
            raise ValidationError('Користувач з таким username вже існує.')

    def validate_email(self, email):
        user = db.session.execute(
            db.select(User).filter_by(email=email.data)
        ).scalar_one_or_none()
        if user:
            raise ValidationError('Користувач з таким email вже існує.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')