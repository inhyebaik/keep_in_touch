import unittest 
from model import User, Event, ContactEvent, Contact, Template, db, connect_to_db
from server import app
from seed import example_data
import datetime

# Method                Checks that
# assertEqual(a, b)   a == b
# assertNotEqual(a, b)    a != b
# assertTrue(x)   bool(x) is True
# assertFalse(x)  bool(x) is False
# assertIs(a, b)  a is b
# assertIsNot(a, b)   a is not b
# assertIsNone(x) x is None
# assertIsNotNone(x)  x is not None
# assertIn(a, b)  a in b
# assertNotIn(a, b)   a not in b
# assertIsInstance(a, b)  isinstance(a, b)
# assertNotIsInstance(a, b)   not isinstance(a, b)


# basically try to have a test for each non-post route
class NotLoggedInTests(unittest.TestCase):
    """Tests for a non-user."""

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


    def test_homepage(self):
        result = self.client.get("/")
        self.assertIn('Keep in Touch lets you automate keeping in touch', result.data)


    def test_users(self):
        result = self.client.get("/users")
        self.assertIn('Jane Hacks', result.data)


    def test_register_login(self):
        result = self.client.get('/register_login')
        self.assertIn('Register', result.data)
        self.assertIn('Log in', result.data)
        self.assertIn('Email', result.data)
        self.assertIn('Password', result.data)
        self.assertIn('Phone: +1', result.data)
        self.assertIn('First name', result.data)
        self.assertIn('Last name', result.data)


    def test_register(self):
        """Tests registering a new user."""
        result = self.client.post("/register",
                                  data={'email': "ada@gmail.com", 
                                        'password': "a",
                                        'fname': "Ada", 
                                        'lname':"Hackbright",
                                        'phone': "1234567890"}, 
                                  follow_redirects=True)
        self.assertIn("now added as a new user! Welcome!", result.data)
        self.assertIn('Log Out', result.data)
        self.assertIn('People Ada Will Keep in Touch With', result.data)
        self.assertIn('Add a new contact', result.data)


    def test_login(self):
        """Tests logging in a new user."""
        result = self.client.post("/login",
                                  data={'login_email': 'j@gmail.com', 
                                        'login_password': 'a'}, 
                                  follow_redirects=True)
        self.assertIn('Log Out', result.data)
        self.assertNotIn('Log In', result.data)
        self.assertIn('Jane Will Keep in Touch With', result.data)
        self.assertIn('Add a new contact', result.data)
        self.assertIn('Add a new event for', result.data)
        self.assertIn('Delete', result.data)
        

    def test_hompage_nl(self):
        result = self.client.get("/")
        self.assertIn("Log In or Register", result.data)
        self.assertNotIn("Log Out", result.data)


    def test_profile_nl(self):
        result = self.client.get("/users/1")
        self.assertIn("Log In or Register", result.data)
        self.assertNotIn("Log Out", result.data)
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
        self.assertIn("You must log in or register", result.data)


    def test_remove_contact_nl(self):
        # should redirect to /register_login 
        result = self.client.get('/remove_contact/1', follow_redirects=True)
        self.assertIn('Register', result.data)
        self.assertIn('Log in', result.data)
        self.assertIn('Email', result.data)
        self.assertIn('Password', result.data)
        # On /register_login, should see flashed error msg
        self.assertIn("You must log in or register to remove contacts", result.data)

    def test_add_event_nl(self):
        # should redirect to /register_login 
        result = self.client.get('/add_event/1', follow_redirects=True)
        self.assertIn('Register', result.data)
        self.assertIn('Log in', result.data)
        self.assertIn('Email', result.data)
        self.assertIn('Password', result.data)
        # On /register_login, should see flashed error msg
        self.assertIn("You must log in or register", result.data)

    def test_edit_profile_nl(self):
        # should redirect to /register_login 
        result = self.client.get('/edit_profile', follow_redirects=True)
        self.assertIn('Register', result.data)
        self.assertIn('Log in', result.data)
        self.assertIn('Email', result.data)
        self.assertIn('Password', result.data)
        # On /register_login, should see flashed error msg
        self.assertIn("You must log in or register to edit your profile", result.data)


####### when user is newly registered ########
class NewUserTests(unittest.TestCase):
    """Tests for logged-in users."""

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
        result = self.client.post("/register",
                                  data={'email': "ada@gmail.com", 
                                        'password': "a",
                                        'fname': "Ada", 
                                        'lname':"Hackbright",
                                        'phone': "1234567890"}, 
                                  follow_redirects=True)


    def tearDown(self):
        """Do at end of every test."""
        db.session.close()
        db.drop_all()


    def test_profile_nu(self):
        """Tests profile of new user."""
        result = self.client.get('/users/3')
        self.assertIn("Edit my info", result.data)
        self.assertIn("Ada", result.data)
        self.assertIn("Log Out", result.data)
        self.assertIn("Add a new contact/event", result.data)
        # should not have any events/contacts
        self.assertNotIn("Edit contact info", result.data)
        self.assertNotIn("Add a new event for", result.data)
        self.assertNotIn("Delete", result.data)


    def test_logout_nu(self):
        result = self.client.get('/logout', follow_redirects=True)
        self.assertIn("You have successfully logged out!", result.data)
        self.assertIn("Log In", result.data)


    def test_add_event_nu(self):
        # Get tomorrow's date to fetch the events, formatted to match DB date fields
        t = datetime.datetime.now()
        today = datetime.datetime(t.year, t.month, t.day, 0, 0)
        tmrw = datetime.datetime(t.year, t.month, t.day+1, 0, 0)
        formatted_date = "{}/{}/{}".format(tmrw.month, tmrw.day, tmrw.year)

        result = self.client.post('/add_event', data={'contact_name':'Grace', 
                                                      'contact_email':'grace@gmail.com', 
                                                      'contact_phone':'2223334444',
                                                      'user_id':3,
                                                      'greet':'Hello', 'sign_off':'Sincerely', 
                                                      'template_name':'Happy birthday',
                                                      'date': tmrw }, 
                                                follow_redirects=True)
        self.assertIn("You have successfully added a new event for Grace", result.data)
        # should redirect to /edit_event and render edit_event.html
        self.assertIn("Edit Event Details", result.data)


####### when user is logged in ########

class UserTests(unittest.TestCase):
    """Tests for logged-in users."""

### JANE: her profile shows John Recuitor as contact; 
### when attempted to edit that event for that contact, it is prefilled with
### Ian Interviewer's event (WHYYYYY)

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
        result = self.client.post("/login", data={'login_email': 'j@gmail.com', 
                                                  'login_password': 'a'},
                                            follow_redirects=True)

    def tearDown(self):
        """Do at end of every test."""
        db.session.close()
        db.drop_all()


    def test_profile_lu(self):
        result = self.client.get('/users/1')
        self.assertIn("Log Out", result.data)
        self.assertIn("Jane Hacks\'s profile", result.data)
        self.assertIn("Edit my info", result.data)
        self.assertNotIn("Add a new contact/event", result.data)


    def test_logout_lu(self):
        result = self.client.get('/logout', follow_redirects=True)
        self.assertIn("You have successfully logged out!", result.data)
        self.assertIn("Log In", result.data)


    def test_event_for_contact(self):
        result = self.client.get('/edit_event/1', follow_redirects=True)
        # should have contact.name and contact.template.text already there
        self.assertIn("Ian Interviewer", result.data)
        self.assertIn("hello there", result.data)
        self.assertIn("Remove Event", result.data)
        self.assertIn("Log Out", result.data)


    def test_handle_edits(self):
        """Test editing an existing event."""

        t = datetime.datetime.now()
        today = datetime.datetime(t.year, t.month, t.day, 0, 0)
        tmrw = datetime.datetime(t.year, t.month, t.day+1, 0, 0)
        formatted_date = "{}/{}/{}".format(tmrw.month, tmrw.day, tmrw.year)
        day_before="{}/{}/{}".format(tmrw.month, tmrw.day-1, tmrw.year)

        result = self.client.post('/handle_edits', data={'user_id':1, 'event_id':1, 
                                                        'contact_name':'K Interviewer',
                                                        'template_text': "Hi thanks", 
                                                        'contact_email': "ii@gmail.com", 
                                                        'contact_phone':"+10009998888",
                                                        'date':tmrw}, 
                                                 follow_redirects=True)
        # test flash messages
        self.assertIn("Your message for K Interviewer has been modified successfully", result.data)
        self.assertIn("send it to K Interviewer on {}".format(tmrw), result.data)
        self.assertIn("remind you the day before (on {})".format(day_before), result.data)
        # should redirect to user's profile 
        self.assertNotIn("Jane Hacks\'s profile", result.data)


    def test_remove_event(self):
        result = self.client.post('/remove_event', data={"user_id":1, 
                                                         "event_id":1},
                                                  follow_redirects=True)
        self.assertIn("You have successfully deleted this event", result.data)
        # should redirect to user's profile 
        self.assertIn("Jane Hacks\'s profile", result.data)
        # should not see the event anymore 



    def test_logout_lu(self):
        result = self.client.get('/logout', follow_redirects=True)
        self.assertIn("You have successfully logged out!", result.data)
        self.assertIn("Log In", result.data)





if __name__ == "__main__":
    unittest.main()