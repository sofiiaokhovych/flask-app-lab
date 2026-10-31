from pathlib import Path
from tinydb import TinyDB, Query
from datetime import datetime


DATA_FOLDER = Path(__file__).resolve().parent.parent.parent / "data"
DATA_FOLDER.mkdir(exist_ok=True)

db = TinyDB(DATA_FOLDER / "products.json")
products_table = db.table("products")

Product = Query()


def add_product(name, content, price, category, quantity, image=""):
    products = products_table.all()
    new_id = max((p["id"] for p in products), default=0) + 1

    product = {
        "id": new_id,
        "name": name,
        "content": content,
        "price": float(price),
        "category": category,
        "quantity": quantity,
        "image": image,
        "created_at": datetime.now().astimezone().isoformat(timespec="seconds")
    }

    products_table.insert(product)
    return product


def get_products():
    return products_table.all()


def get_product(product_id):
    return products_table.get(Product.id == product_id)


def update_product(product_id, data):
    products_table.update(data, Product.id == product_id)


def delete_product(product_id):
    products_table.remove(Product.id == product_id)
