"""Models and database functions for project."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import time, datetime
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()

##############################################################################
# Model definitions

class User(db.Model):
    """User of website."""

    __tablename__ = "users"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.Text, nullable=False)
    fname = db.Column(db.String(20)) # make nullable=False after testing, for more refined log in/register page
    lname = db.Column(db.String(20)) # make nullable=False after testing, for more refined log in/register page
    phone = db.Column(db.String(15))
    fb_uid = db.Column(db.Text)
    fb_at = db.Column(db.Text)
    # picture from FB
    pic_url = db.Column(db.Text)


    def __init__(self, email, password, fname, lname, phone='', fb_uid='', fb_at='', pic_url=''):
        self.email = email
        self.password = generate_password_hash(password)
        self.fname = fname
        self.lname = lname
        self.phone = phone
        self.fb_uid = fb_uid
        self.fb_at = fb_at
        self.pic_url=pic_url
        

    def __repr__(self):
        """Provide better representation."""
        return "<User id={} fname={} email={}>".format(self.id, self.fname, self.email)



class Contact(db.Model):
    """User has many contacts."""

    __tablename__ = "contacts"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(64), nullable=False)  # not fname/lname in case it's "Mom"
    email = db.Column(db.String(64))
    phone = db.Column(db.String(15))
    # address information
    address = db.Column(db.Text)
    # picture from FB
    pic_url = db.Column(db.Text, default="/static/defaultpic.jpg")
    # A contact belongs to a user
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship("User", backref=db.backref("contacts", order_by=id))


    def __repr__(self):
        """Provide better representation."""
        return "<Contact id={} name={}>".format(self.id, self.name.encode('utf-8'))



class Event(db.Model):
    """Events table."""

    __tablename__ = "events"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    contact_id = db.Column(db.Integer, db.ForeignKey('contacts.id'), nullable=False)
    template_id = db.Column(db.Integer, db.ForeignKey('templates.id'), nullable=False)
    #default date is tomorrow
    date = db.Column(db.DateTime, default=(datetime.datetime.today() + datetime.timedelta(days=1)), nullable=False)
    # if reminder is sent
    reminder_sent = db.Column(db.Boolean, default=False)
    job_done = db.Column(db.Boolean, default=False)
    # an event has one contact, and a contact can have multiple events
    contacts = db.relationship("Contact", secondary="contactsevents", backref="events")
    template = db.relationship("Template", backref=db.backref("event"))
    # add this relationship because I'm querying often for a user's events
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship("User", backref=db.backref("events"))


    def __repr__(self):
        """Provide better representation."""
        return "<Event id={} date={}>".format(self.id, self.date)


class ContactEvent(db.Model):
    """Association table between contacts and events."""

    __tablename__ = "contactsevents"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    contact_id = db.Column(db.Integer, db.ForeignKey('contacts.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)


class Template(db.Model):
    """A template belongs to an event"""

    __tablename__ = "templates"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    text = db.Column(db.Text, nullable=False)
    
    def __repr__(self):
        """Provide better representation."""
        return "<Template id={} name={} text={}>".format(self.id, self.name, self.text)



def connect_to_db(app, uri='postgresql:///project'):
    """Connect the database to our Flask app."""
    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # from server import app
    app = Flask(__name__)
    connect_to_db(app)
    print "Connected to DB."
    db.create_all()
