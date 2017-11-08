from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session,
                   jsonify)
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy

from model import (User, Event, ContactEvent, Contact, Template, db, connect_to_db)
import datetime
import random
from quotes import *

app = Flask(__name__)
# app.config['JSON_SORT_KEYS'] = False

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined

q = random_quote(QUOTES)
author = q[0]
quote = q[1]

@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html", author=author, quote=quote)


@app.route('/users')
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users, author=author, quote=quote)


@app.route('/register_login')
def register_form():
    """Prompts user to register/sign in"""

    return render_template("register_login_form.html", author=author, quote=quote)


@app.route('/register', methods=['POST'])
def register_process():
    """Adds new user to DB; adds to session"""
    # gets information from registration form
    email = request.form.get('email')
    password = request.form.get('password')
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    phone = request.form.get('phone')
    # fetch that user from DB as object
    db_user = User.query.filter(User.email == email).first()

    # if that user exists in DB:
    if db_user:
        # alert the email is already in use; prompt them to login instead
        flash("Email already exists in database -- Please try logging in")
        return redirect('/register_login')
    else:
        # register new user; add to DB; log them in; save user_id to session
        new_user = User(email=email, password=password, fname=fname, lname=lname, phone=phone)
        db.session.add(new_user)
        db.session.commit()
        flash("You're now added as a new user! Welcome!")
        session['user_id'] = new_user.id
        url = '/users/{}'.format(new_user.id)
        # redirect to the user's info page
        return redirect(url)


@app.route('/login', methods=['POST'])
def login_process():
    """Logs user in; adds to session"""
    # gets information from login input form
    email = request.form.get('login_email')
    password = request.form.get('login_password')
    # fetch that user from DB as object
    db_user = User.query.filter(User.email == email).first()
    # if that user exists in DB:
    if db_user:
        # verify password, redirect to their user info page;
        # add user_id to the session
        if db_user.password == password:
            session['user_id'] = db_user.id
            flash("You have successfully logged in!")
            url = '/users/{}'.format(db_user.id)
            return redirect(url)
        else:
            # if password doesn't match, redirect to register page
            flash("Wrong credentials -- Try again")
            return redirect('/register_login')
    else:
        # alert if email doesn't exist; prompt and redirect to register
        flash("Email does not exist in database: please register")
        return redirect('/register_login')


@app.route('/logout')
def log_out():
    """Logs a user out"""
    # clear out session; confirm log out; redirect to homepage
    del session['user_id']
    flash("You have successfully logged out!")
    return redirect("/")


@app.route('/users/<user_id>')
def user_profile(user_id):
    """Shows specific user's details
    Shows user's contacts list
    Shows user's events list
    """
    user = User.query.filter(User.id == user_id).one()
    return render_template("user_profile.html", user=user, author=author,  quote=quote)


@app.route('/add_event')
def add_event():
    """Let logged in users go to the new event form.""" 
    
    user_id = session.get("user_id")
    if user_id:
        user = User.query.filter(User.id == user_id).one()
        return render_template("event_form.html", user=user, author=author, quote=quote)
    else:
        flash("You must log in or register to add events")
        return redirect("/register_login")


@app.route('/add_event', methods=['POST'])
def handle_event_form():
    """Validates and adds new event and template to DB."""
    
    # Need to add the contact and template before creating an event 

    # add contact
    name = request.form.get('contact_name')
    email = request.form.get('contact_email')
    phone = request.form.get('contact_phone')
    user_id = session.get("user_id")
    new_contact = Contact(name=name, email=email, phone=phone, user_id=user_id)
    db.session.add(new_contact)
    db.session.commit()

    # add template
    template_name = request.form.get('template_name')
    template_text = request.form.get('template_text')
    new_template = Template(name=template_name, text=template_text)
    db.session.add(new_template)
    db.session.commit()

    # add event
    contact_id = new_contact.id
    date = request.form.get('date')
    new_event = Event(contact_id=contact_id, template_id=new_template.id, date=date)
    db.session.add(new_event)
    db.session.commit()

    # add ContactEvent association
    ce = ContactEvent(contact_id=contact_id, event_id=new_event.id)
    db.session.add(ce)
    db.session.commit()


    flash("You have successfully added a new event for {}!".format(name))
    url = '/edit_event/{}'.format(new_event.id)
    return redirect(url)


@app.route('/edit_event/<event_id>')
def show_event(event_id):
    """Show specific event to view or modify"""

    # make sure the user is logged in
    user_id = session.get("user_id")
    if user_id:
        user = User.query.filter(User.id == user_id).one()
        event = Event.query.filter(Event.id == event_id).first()
        return render_template("edit_event.html", event=event, user=user, author=author, quote=quote)
    else:
        flash("You must log in or register to modify events")
        return redirect("/register_login")


@app.route('/handle_edits', methods=['POST'])
def modify_db():
    """Allow user to change input fields that will go into DB."""

    # get user and event primary keys we are modifying for 
    user_id = session.get("user_id")
    event_id = int(request.form.get('event_id'))

    # get the user, event, and contact objects we are modifying for
    user = User.query.filter(User.id == user_id).one()
    event = Event.query.filter(Event.id == event_id).one()
    contact = Contact.query.filter(Contact.id == event.contact_id).one()

    # update contact, event, template objects in the DB
    contact.name = request.form.get('contact_name')
    event.template.text = request.form.get('template_text')
    contact.email = request.form.get('contact_email')
    contact.phone = request.form.get('contact_phone')
    event.date = request.form.get('date')
    db.session.commit()
    flash("Your event/contact has been modified successfully!")
    
    # redirect user to their profile
    url = '/users/{}'.format(user.id)
    return redirect(url)

@app.route('/remove_event', methods=['POST'])
def remove_event():
    """Delete record from DB."""

    event_id = request.form.get('event_id')
    ce = ContactEvent.query.filter(ContactEvent.event_id == event_id).delete()
    Event.query.filter(Event.id == event_id).delete()
    db.session.commit()

    user_id = session['user_id']
    flash("You have successfully deleted this event")
    url = '/users/{}'.format(user_id)
    return redirect(url)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
