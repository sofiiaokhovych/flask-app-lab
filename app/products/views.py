from pathlib import Path
from uuid import uuid4
from flask import render_template, redirect, url_for, flash, request, current_app, abort
from PIL import Image, UnidentifiedImageError
from werkzeug.utils import secure_filename
from . import products_bp
from .forms import ProductForm, DeleteProductForm
from .storage import add_product as save_product, get_products, get_product, update_product, delete_product

UPLOAD_FOLDER = Path(__file__).resolve().parent / "static" / "uploads" / "products"
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)


def save_image(image):
    if not image or not image.filename:
        return ""

    try:
        image.stream.seek(0)
        with Image.open(image.stream) as img:
            img.verify()
        image.stream.seek(0)
    except (UnidentifiedImageError, OSError, ValueError):
        raise ValueError("Файл не є правильним зображенням.")

    filename = secure_filename(image.filename)
    extension = filename.rsplit(".", 1)[-1].lower()

    if extension not in ["jpg", "jpeg", "png"]:
        raise ValueError("Недозволений формат зображення.")

    new_filename = f"{uuid4().hex}.{extension}"
    image.save(UPLOAD_FOLDER / new_filename)

    return f"uploads/products/{new_filename}"

@products_bp.route("/")
@products_bp.route("")
def all_products():
    products = get_products()
    return render_template("products.html", products=products)


@products_bp.route("/add", methods=["GET", "POST"])
def add_product():
    form = ProductForm()

    if form.validate_on_submit():
        try:
            image_path = save_image(form.image.data)

            save_product(
                name=form.name.data,
                content=form.content.data,
                price=form.price.data,
                category=form.category.data,
                quantity=form.quantity.data,
                image=image_path
            )

            flash("Товар успішно додано!", "success")
            return redirect(url_for("products.all_products"))

        except (OSError, ValueError) as error:
            flash(f"Помилка: {error}", "danger")

    elif request.method == "POST":
        flash("Перевірте правильність заповнення форми.", "danger")

    return render_template("product_form.html", form=form, title="Додавання товару")


@products_bp.route("/<int:id>")
def product_detail(id):
    product = get_product(id)

    if product is None:
        abort(404)

    return render_template("detail_product.html", product=product, delete_form=DeleteProductForm())


@products_bp.route("/<int:id>/edit", methods=["GET", "POST"])
def edit_product(id):
    product = get_product(id)

    if product is None:
        abort(404)

    form = ProductForm()

    if form.validate_on_submit():
        try:
            image_path = product["image"]

            if form.image.data and form.image.data.filename:
                image_path = save_image(form.image.data)

            updated_data = {
                "name": form.name.data,
                "content": form.content.data,
                "price": float(form.price.data),
                "category": form.category.data,
                "quantity": form.quantity.data,
                "image": image_path
            }

            update_product(id, updated_data)

            flash("Товар успішно оновлено!", "success")
            return redirect(url_for("products.product_detail", id=id))

        except (OSError, ValueError) as error:
            flash(f"Помилка: {error}", "danger")

    elif request.method == "GET":
        form.name.data = product["name"]
        form.content.data = product["content"]
        form.price.data = product["price"]
        form.category.data = product["category"]
        form.quantity.data = product["quantity"]

    return render_template(
        "product_form.html",
        form=form,
        title="Редагування товару",
        product=product
    )


@products_bp.route("/<int:id>/delete", methods=["POST"])
def remove_product(id):
    product = get_product(id)

    if product is None:
        abort(404)

    form = DeleteProductForm()

    if not form.validate_on_submit():
        flash("Не вдалося підтвердити видалення.", "danger")
        return redirect(url_for("products.product_detail", id=id))

    delete_product(id)

    flash("Товар успішно видалено!", "success")
    return redirect(url_for("products.all_products"))
