from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session,
                   jsonify)
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy

from model import User, Event, ContactEvent, Contact, Template, db, connect_to_db
import random
from quotes import *

# for the email sending
import os, time, datetime
import schedule
import sendgrid
import json

# for texting
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

app = Flask(__name__)
# app.config['JSON_SORT_KEYS'] = False

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined #raise error if you use undefined variable in Jinja2

q = random_quote(QUOTES)
author = q[0]
quote = q[1]


# source secrets and create client
account = os.environ.get('TWILIO_TEST_ACCOUNT')
token = os.environ.get('TWILIO_TEST_TOKEN')
twilio_num = os.environ.get('TWILIO_NUMBER')
my_num = os.environ.get('MY_NUMBER')
client = Client(account, token)
app.config.from_object(__name__)


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
    phone = "+1"+request.form.get('phone')
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
        # verify password; redirect to their profile
        if db_user.password == password:
            session['user_id'] = db_user.id # add user_id to the session
            flash("You have successfully logged in!")
            url = '/users/{}'.format(db_user.id)
            return redirect(url)
        else:
            # if password doesn't match, redirect to register/login
            flash("Wrong credentials -- Try again")
            return redirect('/register_login')
    else:
        # alert if email doesn't exist; prompt and redirect to register/login
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
    """Shows specific user's info; all of their events and contacts."""
    user = User.query.get(user_id)
    return render_template("user_profile.html", user=user, author=author,  quote=quote)


@app.route('/add_event')
def add_event():
    """Let logged in users go to the new event form."""
   
    user_id = session.get("user_id")
    if user_id:
        user = User.query.get(user_id)
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
    phone = "+1" + request.form.get('contact_phone')
    user_id = session.get("user_id")
    new_contact = Contact(name=name, email=email, phone=phone, user_id=user_id)
    db.session.add(new_contact)
    db.session.commit()

    # get inputs from form for template text
    greet = request.form.get('greet')
    sign_off = request.form.get('sign_off')
    body = request.form.get('body')
    user_fname = User.query.get(user_id).fname
    template_text = "{} {}, \n{} \n{},\n{}".format(greet, name, body, sign_off, user_fname)

    # add template
    template_name = request.form.get('template_name')
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

    # redirect to edit_event page
    flash("You have successfully added a new event for {}!".format(name))
    url = '/edit_event/{}'.format(new_event.id)
    return redirect(url)


@app.route('/edit_event/<event_id>')
def show_event(event_id):
    """Show specific event to view or modify"""

    user_id = session.get("user_id") # make sure the user is logged in
    if user_id:
        user = User.query.get(user_id)
        event = Event.query.get(event_id)

        return render_template("edit_event.html", event=event, user=user, author=author, quote=quote)
    else:
        flash("You must log in or register to modify events")
        return redirect("/register_login")


@app.route('/handle_edits', methods=['POST'])
def modify_db():
    """Allow user to change event and template that will go into DB."""

    # get user and event primary keys we are modifying for
    user_id = session.get("user_id")
    event_id = int(request.form.get('event_id'))

    # get the user, event, and contact objects we are modifying for
    user = User.query.get(user_id)
    event = Event.query.get(event_id)
    contact = Contact.query.filter(Contact.id == event.contact_id).one()

    # update contact, event, template objects in the DB
    contact.name = request.form.get('contact_name')
    event.template.text = request.form.get('template_text')
    contact.email = request.form.get('contact_email')
    contact.phone = request.form.get('contact_phone')
    event.date = request.form.get('date')
    db.session.commit()
    flash("Your event/contact has been modified successfully! We'll remind you on {}".format(event.date))
    # redirect user to their profile
    url = '/users/{}'.format(user_id)
    return redirect(url)

@app.route('/remove_event', methods=['POST'])
def remove_event():
    """Delete event and template (but not the contact) from DB."""
 
    user_id = session.get("user_id")
    if user_id:
        # get event_id from hidden input;  
        event_id = request.form.get('event_id')
        template_id = Event.query.get(event_id).template_id
        # delete ContactEvent association table link 
        ContactEvent.query.filter(ContactEvent.event_id == event_id).delete()
        # and then delete the Event
        Event.query.filter(Event.id == event_id).delete()
        Template.query.filter(Template.id == template_id).delete()
        db.session.commit()
        flash("You have successfully deleted this event")
        url = '/users/{}'.format(user_id)
        return redirect(url)
    else:
        flash("You must log in or register to remove events")
        return redirect("/register_login")


@app.route('/remove_contact/<contact_id>')
def confirm(contact_id):
    """Confirmation page to delete contact (and their events and templates) from DB."""

    user_id = session.get("user_id")
    if user_id:
        contact = Contact.query.get(contact_id)
        return render_template('confirm_delete_contact.html', contact=contact, author=author, quote=quote)
    else:
        flash("You must log in or register to remove contacts")
        return redirect("/register_login")


    
@app.route('/remove_contact', methods=['POST'])
def remove_contact():
    """Delete contact (and their events, and templates) from DB."""
    
    user_id = session.get("user_id")
    contact_id = request.form.get('contact_id')

    if user_id: 
        # delete the ContactEvent association 
        ContactEvent.query.filter(ContactEvent.contact_id == contact_id).delete()
        
        #### delete their Events and their templates    
        events = Event.query.filter(Event.contact_id == contact_id).all()
        # get the template ids for all of the events for that one contact
        template_ids = []
        for event in events:
            template_ids.append(event.template_id)
        # delete the events
        Event.query.filter(Event.contact_id == contact_id).delete()
        db.session.commit()
        # delete the templates
        for template_id in template_ids:
            Template.query.filter(Template.id == template_id).delete()
            db.session.commit()

        # delete the contact
        Contact.query.filter(Contact.id == contact_id).delete()
        db.session.commit()

        flash("You have successfully deleted this contact")
        user_id = session.get('user_id')
        url = '/users/{}'.format(user_id)
        return redirect(url)
    else:
        flash("You must log in or register to remove contacts")
        return redirect("/register_login")


### TEXTING REMINDER WITH TWILIO ###
def text_reminder(event):
    """Text reminder to user of an event; asks if they want to update msg"""
    user_phone = event.contacts[0].user.phone
    user_fname = event.contacts[0].user.fname
    c_name = event.contacts[0].name

    # Send an SMS
    my_msg = "\n\n\nHello {}, your event's coming up tomorrow for {}.\n\n--------\n\nYour message \
currently is:\n'{}'\n\n--------\n\nIf you'd like to update this message, please \
reply with your new message (in one SMS response. Please add 'event_id={}' in your response)".format(user_fname, c_name, event.template.text, event.id)
    message = client.messages.create(to=user_phone, from_=twilio_num, body=my_msg)
    print "MESSAGE SENT to {}".format(user_phone)



##### TWILIO MESSAGING HANDLER, USING NGROK 5000 ########
@app.route("/sms", methods=['GET', 'POST'])
def handle_reminder_response():
    """Handle user response to reminder"""

    to_number = request.values.get('To') # Keep in Touch's phone
    from_number = request.values.get('From', None) # user's phone
    user_response = request.values.get('Body')

    # fetch user from DB to update event template text
    user = User.query.filter(User.phone == from_number).one()
    user_fname = user.fname
    event_id = None
    
    # get tomorrow's date to fetch the event
    t = datetime.datetime.now()
    today = datetime.datetime(t.year, t.month, t.day, 0, 0)
    tmrw = datetime.datetime(t.year, t.month, t.day+1, 0, 0)
    
    if "event_id" in user_response.lower():
        eindex = user_response.index("event_id")
        # get the event_id from incoming text...they were instructed to end reply with "event_id=XX"
        event_id = int(user_response[(eindex + len("event_id=")):])
        event = Event.query.get(event_id)
        new_text = user_response[:eindex].rstrip()
        # update database 
        event.template.text = new_text
        db.session.commit()
        # send confirmation text
        message = "Thanks, {}! Your new message will be updated in the database as: '{}'".format(user_fname, event.template.text)
        resp = MessagingResponse()
        resp.message(body=message)
        return str(resp)
    else:
        # text the user back prompting to add the "event_id" + same instructions.
        for contact in user.contacts:
            for event in contact.events:
                if event.date == tmrw:
                    my_msg = "You didn't add 'event_id={id}' in your response. Please text us the same message with the 'event_id={id}' at the end".format(id=event.id)
                    message = client.messages.create(to=from_number, from_=to_number, body=my_msg)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode
    connect_to_db(app)
    # Use the DebugToolbar
    DebugToolbarExtension(app)
    app.run(port=5000, host='0.0.0.0')

    # # add users to callers list
    # callers = {
    #     twilio_num: "Keep in Touch Team",
    #     # my_num: "Ada Hackbright",
    #     # "+14158675310": "Boots",
    #     # "+14158675311": "Virgil",
    # }
    # for user in User.query.all():
    #     callers[user.phone] = user.fname + " " +user.lname
