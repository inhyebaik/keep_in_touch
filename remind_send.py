import time, datetime
import schedule

import sendgrid
import json
import os

"""Models and database functions for project."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

"""For texting."""
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client


db = SQLAlchemy()
app = Flask(__name__)


# source secrets and create client
account = os.environ.get('TWILIO_TEST_ACCOUNT')
token = os.environ.get('TWILIO_TEST_TOKEN')
twilio_num = os.environ.get('TWILIO_NUMBER')
my_num = os.environ.get('MY_NUMBER')
client = Client(account, token)


##############################################################################
## for sending emails ##
##############################################################################

def return_todays_events():
    """Checks if there are any events today."""
    t = datetime.datetime.now()
    today = datetime.datetime(t.year, t.month, t.day, 0, 0)
    todays_events = Event.query.filter(Event.date == today).all()
    if todays_events == []:
        return "No events!"
    else:
        return todays_events


def return_tmrws_events():
    """Checks if there are any events today."""
    t = datetime.datetime.now()
    tmrw = datetime.datetime(t.year, t.month, t.day + 1, 0, 0)
    events = Event.query.filter(Event.date == tmrw).all()
    if events == []:
        return "No events!"
    else:
        return events


# def return_events(date):
#     """Checks if there are any events today."""
#     todays_events = Event.query.filter(Event.date == date).all()
#     if todays_events == []:
#         return "No events!"
#     else:
#         return todays_events


def send_all_emails(events):
    """ Takes a list of today's events (EVENT OBJECTS) and sends out emails
        to the contacts
    """
    if events == []:
        return "No events today"
 
    for event in events:
        send_email(event)


def remind_all_users(events):
    """ Takes a list of tomorrow's events (EVENT OBJECTS): texts & emails reminders
        to the user
    """
    if events == []:
        return "No events today"

    for event in events:
        text_reminder(event)
        remind_user(event)


### TEXTING REMINDER WITH TWILIO ###
def text_reminder(event):
    """Text reminder to user of an event; asks if they want to update msg"""

    user_phone = event.contacts[0].user.phone
    user_fname = event.contacts[0].user.fname
    c_name = event.contacts[0].name

    # Send an SMS
    my_msg = "Hello {}, your event coming up on {} for {}.\nYour message\
              currently is: '{}'\nIf you'd like to update this message, please \
              reply with your new message (in one SMS response)".format(user_fname,
                                                                        event.date,
                                                                        c_name)
    message = client.messages.create(to=user_phone, from_=twilio_num, body=my_msg)


def send_email(event):
    """Send template text to contacts."""
    
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    to_email = event.contacts[0].email
    to_name = event.contacts[0].name

    from_name = event.contacts[0].user.fname
    from_email = event.contacts[0].email

    subject = event.template.name
    message_text = event.template.text
    print message_text

    data = {
      # "send_at": send_at_time,

      "from": {
        "email": from_email,
        "name": from_name
      },

      "personalizations": [
        {
          "to": [
            {
              "email": to_email,
              "name": to_name,
            }, 
            # {
            #   "email": email2,
            #   "name": name2
            # }
          ],
          "subject": subject
        }
      ],

      "content": [
        {
          "type": "text/plain",
          "value": message_text
        }
      ]

    }

    response = sg.client.mail.send.post(request_body=data)
    print(response.status_code)
    print(response.body)
    print(response.headers)

# remind you via email to contact someone

def remind_user(event):
    """Email user of event coming up."""

    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    to_email = event.contacts[0].user.email
    to_name = event.contacts[0].user.fname
    from_name = "Keep in Touch Team"
    from_email = "inb125@mail.harvard.edu"
    subject = "Reminder to Keep in Touch with {}".format(event.contacts[0].name)
    message_text = "Just wanted to remind you that {} is coming up and we will send a {} message for {} soon!".format(event.date, event.template.name, event.contacts[0].name)
    data = {
      # "send_at": send_at_time,
      "from": {
        "email": from_email,
        "name": from_name
      },

      "personalizations": [
        {
          "to": [
            {
              "email": to_email,
              "name": to_name,
            }, 
            # {
            #   "email": email2,
            #   "name": name2
            # }
          ],
          "subject": subject
        }
      ],

      "content": [
        {
          "type": "text/plain",
          "value": message_text
        }
      ]

    }
    response = sg.client.mail.send.post(request_body=data)
    print(response.status_code)
    print(response.body)
    print(response.headers)


def convert_to_unix(timeobject):
    """ Takes a datetime object; returns a unix timestamp"""
    return time.mktime(timeobject.timetuple())


# def job():
#     """Schedule job instance"""
#     # for testing
#     e = datetime.datetime(2017, 11, 13, 0, 0)
#     events = return_events(e)
#     remind_all_users(events)
#     send_all_emails(events)

## for the real app, use today ##
##################################
def job():
    """Schedule job instance"""

    tmrw_events = return_tmrws_events()
    today_events = return_todays_events()
    remind_all_users(tmrw_events)
    send_all_emails(today_events)

# schedule.every().day.at("00:00").do(job)
schedule.every(20).seconds.do(job)






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
    # for scheduling emails 
    print datetime.datetime.now() # check what time it is in vagrant
    while True:
        schedule.run_pending()