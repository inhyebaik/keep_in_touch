from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session,
                   jsonify)
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy

from model import (User, Event, ContactEvent, Contact, Template, TemplateInput,
                   Input, db, connect_to_db)
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
    """Let logged in users add new event.""" 
    user_id = session.get("user_id")
    if user_id:
        user = User.query.filter(User.id == user_id).one()
        return render_template("event_form.html", user=user, author=author, quote=quote)
    else:
        flash("You must log in or register to add events")
        return redirect("/register_login")


@app.route('/add_event', methods=['POST'])
def handle_event_form():
    """Validates and adds new event to DB."""
    
    # first add the contact and template before adding event 
    name = request.form.get('contact_name')
    email = request.form.get('contact_email')
    phone = request.form.get('contact_phone')
    user_id = session.get("user_id")
    new_contact = Contact(name=name, email=email, phone=phone, user_id=user_id)
    db.session.add(new_contact)
    db.session.commit()

    template_id = int(request.form.get('template_id'))

    # add event
    contact_id = new_contact.id
    date = request.form.get('date')
    new_event = Event(contact_id=contact_id, template_id=template_id, date=date)
    db.session.add(new_event)
    db.session.commit()

    # add ContactEvent association
    ce = ContactEvent(contact_id=contact_id, event_id=new_event.id)
    db.session.add(ce)
    db.session.commit()

    # get inputs from form
    greet_val = request.form.get('greet')
    body_val = request.form.get('body')
    sign_off_val = request.form.get('sign_off')

    # instantiate new inputs; add inputs to session
    igreet = Input(name='greet', text=greet_val)
    ibody = Input(name='body', text=body_val)
    isign_off = Input(name='sign_off', text=sign_off_val)
    db.session.add_all([igreet, ibody, isign_off])
    db.session.commit()

    # add TemplateInput association
    ti1 = TemplateInput(template_id=template_id, input_id=igreet.id)
    ti2 = TemplateInput(template_id=template_id, input_id=ibody.id)
    ti3 = TemplateInput(template_id=template_id, input_id=isign_off.id)
    db.session.add_all([ti1, ti2, ti3])
    db.session.commit()

    flash("You have successfully added a new event for {}!".format(name))
    url = '/edit_event/{}'.format(new_event.id)
    # redirect them to add inputs to the message
    return redirect(url)


# @app.route('/handle_inputs', methods=['POST'])
# def handle_inputs():
#     """Adds inputs to database."""

#     template_id = request.form.get('template_id')
#     greet = request.form.get('greet')
#     body = request.form.get('template_text')
#     sign_off = request.form.get('sign_off')

#     new_input = Input(greet=greet, body=body, sign_off=sign_off)
#     db.session.add(new_input)
#     db.session.commit()

#     new_ti = TemplateInput(input_id=new_input.id, template_id=template_id)
#     db.session.add(new_ti)
#     db.session.commit()


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


@app.route('/edit_event', methods=['POST'])
def modify_db():
    """Allow user to change input fields that will go into DB."""
    
    user_id = session.get("user_id")
    event_id = request.form.get(event_id)
    contact_id = request.form.get(contact_id)

    user = User.query.filter(User.id == user_id).one()
    event = Event.query.filter(Event.id == event_id).one()
    contact = Contact.query.filter(Contact.id == contact_id).one()

    # modify table attributes with form inputs
    event.template.id = request.form('template_id')
    contact.name = request.form.get('contact_name')
    event.template.text = request.form.get('template_text')
    contact.email = request.form.get('contact_email')
    contact.phone = request.form.get('contact_phone')
    event.date = request.form.get('date')
    
    db.session.commit()
    flash("Your event/contact has been modified")
    
    # redirect to the user's info page
    url = '/users/{}'.format(new_user.id)
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
