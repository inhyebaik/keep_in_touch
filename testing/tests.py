import unittest 
from model import User, Event, ContactEvent, Contact, Template, db, connect_to_db
from server2 import app

class ProjectTests(unittest.TestCase):
    """Tests for Keep in Touch."""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True 

    def test_homepage(self):
        result = self.client.get("/")
        self.assertIn('Keep in Touch lets you automate keeping in touch.', result.data)

####### when not logged in (nl) ##########

    def test_hompage_nl(self):
        result = self.client.get("/")
        self.assertIn("Log In or Register", result.data)
        self.assertNotIn("Log Out", result.data)


    def test_profile_nl(self):
        result = self.client.get("/users/1")
        self.assertIn("Log In or Register", result.data)
        self.assertIn("Log Out", result.data)
        self.assertNotIn("Edit my info", result.data)
        self.assertNotIn("Add a new contact/event", result.data)


    def test_add_event_nl(self):
        # should redirect to /register_login 
        result = self.client.get('/add_event', follow_redirects=True)
        self.assertIn('Register', result.data)
        self.assertIn('Log in', result.data)
        self.assertIn('Email', result.data)
        self.assertIn('Password', result.data)

        # On /register_login, should see flashed error msg
        self.assertIn("You must log in or register to add events", result.data)

    def test_edit_event_nl(self):
        # should redirect to /register_login 
        result = self.client.get('/edit_event/1', follow_redirects=True)
        self.assertIn('Register', result.data)
        self.assertIn('Log in', result.data)
        self.assertIn('Email', result.data)
        self.assertIn('Password', result.data)

        # On /register_login, should see flashed error msg
        self.assertIn("You must log in or register to add events", result.data)


####### when logged in #######

    def test_profile(self):
        result = self.client.post("/login",
                                  data={'email': "j@gmail.com", 'login_password': "a"},
                                  follow_redirects=True)
        self.assertIn("Edit my info", result.data)
        self.assertIn("Jane Hacks", result.data)
        self.assertIn("Log Out", result.data)
        self.assertNotIn("Add a new contact/event", result.data)




class ProjectDatabase(unittest.TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///project")

        # Create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_games(self):
        """Test departments page."""

        result = self.client.get("/users")
        self.assertIn("Jane Hacks", result.data)


if __name__ == "__main__":
    unittest.main()