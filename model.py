"""Models and database functions for project."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime
import time, datetime
import schedule


db = SQLAlchemy()

##############################################################################
# Model definitions

class User(db.Model):
    """User of website."""

    __tablename__ = "users"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    fname = db.Column(db.String(20)) # make nullable=False after testing, for more refined log in/register page
    lname = db.Column(db.String(20)) # make nullable=False after testing, for more refined log in/register page
    phone = db.Column(db.String(15))


    def __repr__(self):
        """Provide better representation."""
        return "<User id={} fname={} email={}>".format(self.id, self.fname, self.email)



class Contact(db.Model):
    """User has many contacts."""

    __tablename__ = "contacts"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(64), nullable=False)  # not fname/lname in case it's "Mom"
    email = db.Column(db.String(64), nullable=False)
    phone = db.Column(db.String(15))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # A contact belongs to a user
    user = db.relationship("User", backref=db.backref("contacts", order_by=id))

    def __repr__(self):
        """Provide better representation."""
        return "<Contact id={} name={}>".format(self.id, self.name)



class Event(db.Model):
    """Events table."""

    __tablename__ = "events"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    contact_id = db.Column(db.Integer, db.ForeignKey('contacts.id'), nullable=False)
    template_id = db.Column(db.Integer, db.ForeignKey('templates.id'), nullable=False)
    #default date is tomorrow
    date = db.Column(db.DateTime, default=(datetime.datetime.today() + datetime.timedelta(days=1)), nullable=False)
    # an event has one contact, and a contact can have multiple events
    contacts = db.relationship("Contact", secondary="contactsevents", backref="events")
    template = db.relationship("Template", backref=db.backref("event"))



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
    """ 
    A template belongs to an event 
    """

    __tablename__ = "templates"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    text = db.Column(db.Text, nullable=False)
    
    def __repr__(self):
        """Provide better representation."""
        return "<Template id={} name={} text={}>".format(self.id, self.name, self.text)


# class Input(db.Model):
#     """A template can have many inputs (will go into the text field of template).
#     An input can belong to many templates.

#     name = 'memory', 
#            'how_you_met', 
#            'greeting', 
#            'body', 
#            'sign_off'

#     text = 'how did you meet?', 
#              'how do you want to greet?', 
#              'how do you want to sign off?', 
#              'what do you want to follow up on?'

#     """

#     __tablename__ = "inputs"

#     id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#         # greet, body, sign_off
#     name = db.Column(db.String(64), nullable=False)
#     text = db.Column(db.String(500), nullable=False)

#     templates = db.relationship("Template", secondary="templatesinputs", backref="inputs")

#     def __repr__(self):
#         """Provide better representation."""
#         return "<Input id={} name={} text={}>".format(self.id, self.name, self.text)



# class TemplateInput(db.Model):
#     """Association table between Templates and Inputs tables"""

#     __tablename__ = "templatesinputs"

#     id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     template_id = db.Column(db.Integer, db.ForeignKey('templates.id'), nullable=False)
#     input_id = db.Column(db.Integer, db.ForeignKey('inputs.id'), nullable=False)

    
##############################################################################
# Helper functions


def connect_to_db(app, uri='postgresql:///project'):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    # from server import app
    app = Flask(__name__)
    connect_to_db(app)
    print "Connected to DB."
    db.create_all()
