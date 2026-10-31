import unittest
from unittest.mock import patch
from tinydb import TinyDB
from tinydb.storages import MemoryStorage
from app.products import storage


class ProductTestCase(unittest.TestCase):
    def setUp(self):
        self.db = TinyDB(storage=MemoryStorage)
        self.table = self.db.table("products")

        self.patcher = patch.object(storage, "products_table", self.table)
        self.patcher.start()

        self.product = storage.add_product("Ноутбук", "Ноутбук для навчання", 25000.00, "laptop", 5)

    def tearDown(self):
        self.patcher.stop()
        self.db.close()

    def test_add_product(self):
        products = storage.get_products()

        self.assertEqual(len(products), 1)
        self.assertEqual(products[0]["name"], "Ноутбук")
        self.assertEqual(products[0]["price"], 25000.00)
        self.assertEqual(products[0]["quantity"], 5)
        self.assertEqual(products[0]["id"], 1)
        self.assertIn("created_at", products[0])

    def test_get_products(self):
        products = storage.get_products()

        self.assertEqual(len(products), 1)
        self.assertEqual(products[0]["name"], "Ноутбук")

    def test_get_product(self):
        product = storage.get_product(self.product["id"])

        self.assertIsNotNone(product)
        self.assertEqual(product["name"], "Ноутбук")

    def test_update_product(self):
        storage.update_product(self.product["id"], {"name": "Новий ноутбук", "price": 27000.00})
        product = storage.get_product(self.product["id"])

        self.assertEqual(product["name"], "Новий ноутбук")
        self.assertEqual(product["price"], 27000.00)
        self.assertEqual(product["id"], self.product["id"])
        self.assertEqual(product["created_at"], self.product["created_at"])

    def test_delete_product(self):
        storage.delete_product(self.product["id"])

        product = storage.get_product(self.product["id"])

        self.assertIsNone(product)
        self.assertEqual(len(storage.get_products()), 0)


if __name__ == "__main__":
    unittest.main()
