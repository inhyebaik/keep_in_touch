from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session,
                   jsonify)
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy

from model import (User, Event, ContactEvent, Contact, Template, TemplateInput,
                   Input, db, connect_to_db)
import datetime


app = Flask(__name__)
# app.config['JSON_SORT_KEYS'] = False

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route('/users')
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)


@app.route('/register_login')
def register_form():
    """Prompts user to register/sign in"""

    return render_template("register_login_form.html")


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
            return redirect('/register')
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
    return render_template("user_profile.html", user=user)


@app.route('/edit_event/<event_id>')
def show_event(event_id):
    """Show specific event to view or modify"""
    event = Event.query.filter(Event.id == event_id).one()
    return render_template("edit_event.html", event=event)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
