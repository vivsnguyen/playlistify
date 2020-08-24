import unittest
import setlist_api
from server import app
from model import connect_to_db, db

def setUp(self):
    """Setup to do before every test."""

    # Get the Flask test client
    self.client = app.test_client()
    app.config['TESTING'] = True

    # Connect to test database
    connect_to_db(app, "postgresql:///testdb")

    # Create tables and add sample data
    db.create_all()
    example_data()


class FlaskSetlistFMTests(unittest.TestCase):
    """Setlist.fm API tests."""

    def test_add_artist_to_db(self):
        """Test add artist to db."""

        self.assertEqual(setlist_api.add_artist_to_db("Jonas Brothers"), '<Artist artist_name=Jonas Brothers>')

    def test_load_setlists_from_artist(self):
        """Test for when artist not found."""

        vivi = setlist_api.add_artist_to_db("vivivivivivivivivi")

        self.assertEqual(setlist_api.load_setlists_from_artist(vivi), '[]')


if __name__ == '__main__':


    unittest.main()
