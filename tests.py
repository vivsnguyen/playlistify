from unittest import TestCase
from server import app
from model import connect_to_db, db, example_data
from flask import session

class FlaskTestsBasic(TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

    def test_index(self):
        """Test homepage page."""

        result = self.client.get("/")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"Listen to your playlists here", result.data)

    def test_login(self):
        """Test login page."""
    
        result = self.client.post("/log-in",
                                  data={'email':'vivi@vivi.com', 'password':'hello'},
                                  follow_redirects=True)
        self.assertIn(b"Welcome", result.data)
    # HASHED password causing key error


class FlaskTestsDatabase(TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        db.session.remove()
        db.drop_all()
        db.engine.dispose()

    # def test(self):

    #     result = self.client.get("/departments")
    #     self.assertIn(b"Legal", result.data)

    #
    # def test_departments_details(self):
    #     """Test departments page."""
    #
    #     result = self.client.get("/department/fin")
    #     self.assertIn(b"Phone: 555-1000", result.data)

if __name__ == "__main__":
    import unittest

    unittest.main()
