# testing reminders
# test incoming replies on server.py with handle_reminder_response()

# testing reminders
# test incoming replies on server.py with handle_reminder_response()

# Models and database functions
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from model import User, Event, ContactEvent, Contact, Template, connect_to_db

# SendGrid / email sending
import time, datetime, json, os, schedule, sendgrid
from sendgrid.helpers.mail import *

# Twilio / texting
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client


app = Flask(__name__)

# Source secrets and create client
account = os.environ.get('TWILIO_TEST_ACCOUNT')
token = os.environ.get('TWILIO_TEST_TOKEN')
twilio_num = os.environ.get('TWILIO_NUMBER')
my_num = os.environ.get('MY_NUMBER')
my_email = os.environ.get('MY_EMAIL')
client = Client(account, token)


def return_todays_events():
    """Checks if there are any events today."""
    t = datetime.datetime.now()
    # Get today's date -- YYYY, MM, DD only to match DB format
    today = datetime.datetime(t.year, t.month, t.day, 0, 0)
    todays_events = Event.query.filter(Event.date == today).all()
    if todays_events == []:
        return "No events!"
    else:
        return todays_events


def return_tmrws_events():
    """Checks if there are any events today."""
    t = datetime.datetime.now()
    # Get tomorrow's date -- YYYY, MM, DD only to match DB format
    tmrw = datetime.datetime(t.year, t.month, t.day + 1, 0, 0)
    # Fetch tomorrow's events
    events = Event.query.filter(Event.date == tmrw).all()
    if events == []:
        return "No events!"
    else:
        return events


def send_all_emails(events):
    """ Takes a list of today's events (Event objects) and emails contacts"""
    if events == [] or events == "No events!":
        return "No events today"
    for event in events:
        send_email(event)


def remind_all_users(events):
    """ Takes a list of tomorrow's events (Event objects): texts & emails users 
        reminders
    """
    if events == [] or events == "No events!":
        return "No events today"
    for event in events:
        text_reminder(event)
        remind_user(event)


def text_reminder(event):
    """Text reminder to user of an event; asks if they want to update msg"""
    user_phone = event.contacts[0].user.phone
    user_fname = event.contacts[0].user.fname
    contact_name = event.contacts[0].name
    # Send an SMS
    my_msg = "\n\n\nHello {}, your event's coming up tomorrow for {}.\n\n--------\n\nYour message \
currently is:\n'{}'\n\n--------\n\nIf you'd like to update this message, please \
reply with your new message (in one SMS response. Please add 'event_id={}' in your response)".format(user_fname, contact_name, event.template.text, event.id)
    message = client.messages.create(to=user_phone, from_=twilio_num, body=my_msg)
    print "MESSAGE SENT to {}".format(user_phone)


def send_email(event):
    """Email contact on day of event on behalf of the user."""
    message = Mail()
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    # Create from_email object from event object arg (the user)
    from_address = event.contacts[0].email
    from_name = event.contacts[0].user.fname
    from_email = Email(from_address, from_name)
    # Create to_email object from event object arg (the user's contact)
    to_address = event.contacts[0].email
    to_name = event.contacts[0].name
    to_email = Email(to_address, to_name)
    # Create mail object from event object arg
    email_body = event.template.text
    subject = event.template.name
    content = Content("text/plain", email_body)
    mail = Mail(from_email, subject, to_email, content)
    # Send email, print confirmation/status
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)


def remind_user(event):
    """Email user of event coming up."""
    message = Mail()
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY')) 
    # Create from_email object from event object arg
    from_email = Email(my_email, "Keep in Touch Team")
    # Create to email property from event object arg (the user)
    to_address = event.contacts[0].user.email
    to_name = event.contacts[0].user.fname
    to_email = Email(to_address, to_name)
    # Create mail to be sent (reminder email)
    subject = "Remember to Keep in Touch"
    email_body = "Just wanted to remind you that {} is coming up and we will send a {} message for {} soon!".format(event.date, event.template.name, event.contacts[0].name)
    content = Content("text/plain", email_body)
    mail = Mail(from_email, subject, to_email, content)
    # Send reminder email and print confirmation/status
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)


## for the real app, use today ##
##################################
def job():
    """Schedule job instance"""
    today_events = return_todays_events()
    send_all_emails(today_events)
    tmrw_events = return_tmrws_events()
    remind_all_users(tmrw_events)

# schedule.every().day.at("00:00").do(job)

schedule.every(2).seconds.do(job)


if __name__ == "__main__":
    # from server import app
    app = Flask(__name__)
    connect_to_db(app)
    print "Connected to DB."
    print datetime.datetime.now() # check what time it is in vagrant
    # for scheduling emails 
    while True:
        schedule.run_pending()
