import unittest
from app import create_app, db, bcrypt
from app.models import User


class UserTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            hashed = bcrypt.generate_password_hash("secret123").decode("utf-8")
            user = User(username="testuser", email="test@example.com", password=hashed)
            db.session.add(user)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def login(self, email="test@example.com", password="secret123"):
        return self.client.post("/users/login", data={"email": email, "password": password}, follow_redirects=True)


    def test_register_page_loads(self):
        response = self.client.get("/users/register")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Register", response.data)

    def test_login_page_loads(self):
        response = self.client.get("/users/login")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Login", response.data)


    def test_register_saves_user_in_db(self):
        response = self.client.post(
            "/users/register",
            data={
                "username": "newuser",
                "email": "new@example.com",
                "password": "password123",
                "confirm_password": "password123",
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Account created for newuser", response.data)

        with self.app.app_context():
            user = db.session.scalar(db.select(User).where(User.email == "new@example.com"))
            self.assertIsNotNone(user)
            self.assertEqual(user.username, "newuser")
            self.assertNotEqual(user.password, "password123")
            self.assertTrue(bcrypt.check_password_hash(user.password, "password123"))


    def test_login_success(self):
        response = self.login()
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Welcome, testuser!", response.data)

    def test_login_wrong_password(self):
        response = self.login(password="wrongpass")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Error: Invalid email or password.", response.data)

    def test_logout(self):
        self.login()
        response = self.client.get("/users/logout", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"You have successfully logged out.", response.data)
        response = self.client.get("/users/account")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/users/login", response.headers["Location"])


if __name__ == "__main__":
    unittest.main()