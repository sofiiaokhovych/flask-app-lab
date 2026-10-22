import unittest
from app import app


class ProductBlueprintTestCase(unittest.TestCase):
    def setUp(self):
        """Налаштування клієнта тестування."""
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_products_page(self):
        """Перевірка сторінки зі списком товарів."""
        response = self.client.get("/products/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Laptop", response.data)
        self.assertIn(b"Phone", response.data)
        self.assertIn(b"PC", response.data)

    def test_laptop_details(self):
        """Перевірка детальної інформації про ноутбук."""
        response = self.client.get("/products/1")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Laptop", response.data)
        self.assertIn(b"1200", response.data)
        self.assertIn(b"Intel Core i7", response.data)

    def test_phone_details(self):
        """Перевірка детальної інформації про смартфон."""
        response = self.client.get("/products/2")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Phone", response.data)
        self.assertIn(b"800", response.data)

    def test_product_not_found(self):
        """Перевірка відсутності товару з невідомим ID."""
        response = self.client.get("/products/99")

        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
