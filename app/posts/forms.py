from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField, SubmitField
from wtforms.fields import DateTimeLocalField
from wtforms.validators import DataRequired, Length
from app import db
from app.models import User

CATEGORIES = [
    ("news", "News"),
    ("publication", "Publication"),
    ("tech", "Tech"),
    ("other", "Other"),
]


class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(min=2, max=150)])
    content = TextAreaField(
        "Content",
        render_kw={"rows": 5, "cols": 40},
        validators=[DataRequired()],
    )
    is_active = BooleanField("Active Post", default=True)
    publish_date = DateTimeLocalField(
        "Publish Date",
        format="%Y-%m-%dT%H:%M",
        default=datetime.now,
        validators=[DataRequired()],
    )
    category = SelectField("Category", choices=CATEGORIES, validators=[DataRequired()])
    author_id = SelectField("Author", coerce=int)
    submit = SubmitField("Submit")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        users = db.session.scalars(db.select(User).order_by(User.id)).all()
        self.author_id.choices = [(u.id, u.username) for u in users]