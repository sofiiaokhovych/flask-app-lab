import unittest
from datetime import datetime

from app import create_app, db
from app.posts.models import Post


class PostTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def create_post_in_db(self, title="Test post", content="Test content",
                          category="tech", is_active=True, posted=None):
        with self.app.app_context():
            post = Post(
                title=title,
                content=content,
                category=category,
                is_active=is_active,
                posted=posted or datetime.utcnow(),
            )
            db.session.add(post)
            db.session.commit()
            return post.id

    def valid_form_data(self, **kwargs):
        data = {
            "title": "My first post",
            "content": "This is TDD!",
            "is_active": "y",
            "publish_date": "2025-01-15T10:30",
            "category": "news",
        }
        data.update(kwargs)
        return data

    def test_create_post(self):
        response = self.client.post(
            "/post/create", data=self.valid_form_data(), follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Post added successfully", response.data)

        with self.app.app_context():
            post = db.session.scalar(db.select(Post).where(Post.title == "My first post"))
            self.assertIsNotNone(post)
            self.assertEqual(post.content, "This is TDD!")
            self.assertEqual(post.category, "news")

    def test_list_posts(self):
        self.create_post_in_db(title="Older post", posted=datetime(2025, 1, 1, 10, 0))
        self.create_post_in_db(title="Newer post", posted=datetime(2025, 2, 1, 10, 0))
        self.create_post_in_db(title="Hidden post", is_active=False)

        response = self.client.get("/post")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Older post", response.data)
        self.assertIn(b"Newer post", response.data)
        self.assertNotIn(b"Hidden post", response.data)
        self.assertLess(response.data.find(b"Newer post"),
                        response.data.find(b"Older post"))

    def test_add_post_form_page(self):
        response = self.client.get("/post/create")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Create a New Post", response.data)

    def test_create_post_author_anonymous(self):
        self.client.post("/post/create", data=self.valid_form_data())
        with self.app.app_context():
            post = db.session.scalar(db.select(Post))
            self.assertEqual(post.author, "Anonymous")

    def test_create_post_author_from_session(self):
        with self.client.session_transaction() as sess:
            sess["username"] = "user1"
        self.client.post("/post/create", data=self.valid_form_data())
        with self.app.app_context():
            post = db.session.scalar(db.select(Post))
            self.assertEqual(post.author, "user1")

    def test_create_post_invalid_data(self):
        response = self.client.post(
            "/post/create", data=self.valid_form_data(title="a")  # занадто короткий
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Enter the correct data in the form!", response.data)
        with self.app.app_context():
            self.assertEqual(db.session.scalars(db.select(Post)).all(), [])
    
    def test_view_post_detail(self):
        post_id = self.create_post_in_db(title="Detail title", content="Detail content")

        response = self.client.get(f"/post/{post_id}")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Detail title", response.data)
        self.assertIn(b"Detail content", response.data)
        self.assertIn(b"tech", response.data)

    def test_update_post(self):
        post_id = self.create_post_in_db(
            title="Old title", posted=datetime(2025, 1, 15, 10, 30)
        )

        response = self.client.get(f"/post/{post_id}/update")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Old title", response.data)
        self.assertIn(b"2025-01-15T10:30", response.data)

        response = self.client.post(
            f"/post/{post_id}/update",
            data=self.valid_form_data(title="New title", publish_date="2025-03-01T12:00"),
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Post updated successfully", response.data)

        with self.app.app_context():
            post = db.session.get(Post, post_id)
            self.assertEqual(post.title, "New title")
            self.assertEqual(post.posted, datetime(2025, 3, 1, 12, 0))

    def test_delete_post(self):
        post_id = self.create_post_in_db(title="To be deleted")

        response = self.client.get(f"/post/{post_id}/delete")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"To be deleted", response.data)

        response = self.client.post(f"/post/{post_id}/delete", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Post deleted successfully", response.data)

        with self.app.app_context():
            self.assertIsNone(db.session.get(Post, post_id))

    def test_404_not_found(self):
        for url in ("/post/9999", "/post/9999/update", "/post/9999/delete",
                    "/nonexistent-page"):
            response = self.client.get(url)
            self.assertEqual(response.status_code, 404, msg=url)
            self.assertIn(b"Page Not Found", response.data)

            
if __name__ == "__main__":
    unittest.main()