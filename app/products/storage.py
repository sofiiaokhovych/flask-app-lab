from pathlib import Path
from tinydb import TinyDB
from datetime import datetime
from uuid import uuid4

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = DATA_DIR / "products.json"

db = TinyDB(DB_PATH, ensure_ascii=False, indent=4)

products_table = db.table("products")

def add_product(name, content, price, category, quantity, image_path=""):
    product = {
        "id": uuid4().hex,
        "name": name,
        "content": content,
        "price": round(float(price), 2),
        "category": category,
        "quantity": quantity,
        "image": str(image_path),
        "created_at": datetime.now().astimezone().isoformat(timespec="seconds")
    }

    products_table.insert(product)
    return product
