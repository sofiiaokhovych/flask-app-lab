from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DecimalField, SelectField, IntegerField, FileField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, InputRequired
from decimal import Decimal
from flask_wtf.file import FileAllowed


class ProductForm(FlaskForm):
    name = StringField(
        "Назва товару",
        validators=[
            DataRequired(message="Введіть назву товару."),
            Length(min=3, message="Назва повинна містити мінімум 3 символи.")
        ]
    )

    content = TextAreaField(
        "Опис товару",
        render_kw={"rows": 5, "cols": 40},
        validators=[
            DataRequired(message="Введіть опис товару.")
        ]
    )

    price = DecimalField(
        "Ціна",
        places=2,
        validators=[
            InputRequired(message="Введіть ціну."),
            NumberRange(min=Decimal("0.01"), message="Ціна повинна бути більшою за 0.")
        ]
    )

    category = SelectField(
        "Категорія",
        choices=[
            ("laptop", "Ноутбук"),
            ("phone", "Телефон"),
            ("tablet", "Планшет"),
            ("other", "Інше")
        ],
        validators=[
            DataRequired(message="Оберіть категорію.")
        ]
    )

    quantity = IntegerField(
        "Кількість",
        validators=[
            InputRequired(message="Введіть кількість."),
            NumberRange(min=0, message="Кількість не може бути від'ємною.")
        ]
    )

    image = FileField(
        "Зображення",
        validators=[
            FileAllowed(["jpg", "jpeg", "png"], message="Дозволені лише JPG, PNG або JPEG.")
        ]
    )

    submit = SubmitField("Зберегти товар")

class DeleteProductForm(FlaskForm):
    submit = SubmitField("Видалити")
