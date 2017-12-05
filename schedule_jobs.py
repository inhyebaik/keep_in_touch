from model import User, Event, ContactEvent, Contact, Template, db, connect_to_db
from flask import Flask

# SendGrid Emailing
import os, time, json, datetime, schedule, sendgrid
from sendgrid.helpers.mail import *

# Twilio Texting
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

# Source secrets and create client
account = os.environ.get('TWILIO_TEST_ACCOUNT')
token = os.environ.get('TWILIO_TEST_TOKEN')
twilio_num = os.environ.get('TWILIO_NUMBER')
my_num = os.environ.get('MY_NUMBER')
my_email = os.environ.get('MY_EMAIL')
kit_email = os.environ.get('KIT_EMAIL')
client = Client(account, token)

app = Flask(__name__)

##### SCHEDULING ######

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
    if t.month == 11 and t.day+1 == 31:
        tmrw = datetime.datetime(t.year, 12, 1, 0, 0)
    else:
    # Get tomorrow's date -- YYYY, MM, DD only to match DB format
        tmrw = datetime.datetime(t.year, t.month, t.day + 1, 0, 0)
    # Fetch tomorrow's events
    events = Event.query.filter(Event.date == tmrw).all()
    if events == []:
        return "No events!"
    else:
        return events


def send_all_emails(events):
    """ Takes a list of today's events (Event objects); emails contacts"""
    if events == [] or events == "No events!":
        return "No events today"
    for event in events:
        if event.job_done == False:
            send_email(event)
            text_contact(event)
            # change job_done to True
            event.job_done = True
            db.session.commit()


def remind_all_users(events):
    """ Takes a list of tomorrow's events (Event objects); texts & emails users
        reminders
    """
    if events == [] or events == "No events!":
        return "No events today"
    for event in events:
        if event.reminder_sent == False:
            text_reminder(event)
            remind_user(event)
            # change reminder_sent to True
            if text_reminder(event) and remind_user(event):
                event.reminder_sent = True
                db.session.commit()


def text_reminder(event):
    """Text reminder to user of an event; asks if they want to update msg"""
    user_phone = event.contacts[0].user.phone
    user_fname = event.contacts[0].user.fname
    contact_name = event.contacts[0].name
    # Send an SMS
    my_msg = "\n\n\nHello {}, your event's coming up tomorrow for: {}. "\
            "\n\n--------\n\nYour message currently is:\n\n\n'{}'\n\n--------\n\n "\
            "If you'd like to update this message, please reply with your new message "\
            "(in one SMS response, with 'event_id={}' at the end)".format(user_fname, contact_name.encode('utf-8'), event.template.text.encode('utf-8'), event.id)
    print user_phone
    message = client.messages.create(to=user_phone, from_=twilio_num, body=my_msg)
    print "TEXTED REMINDER TO USER: {}".format(user_phone)
    return True



def text_contact(event):
    """Text reminder to user of an event; asks if they want to update msg"""
    contact_phone = event.contacts[0].phone
    contact_name = event.contacts[0].name
    template_text = event.template.text
    # Send an SMS
    my_msg = template_text
    message = client.messages.create(to=contact_phone, from_=twilio_num, body=my_msg)
    print "TEXTED CONTACT: {}".format(contact_phone)



def send_email(event):
    """Email contact on day of event on behalf of the user."""
    message = Mail()
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    # Create from_email object from event object arg (the user)
    from_address = event.contacts[0].user.email
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
    print "CONTACT EMAILED"
    print(response.status_code)
    print(response.body)
    print(response.headers)


def remind_user(event):
    """Email user of event coming up."""
    message = Mail()
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    # Create from_email object from event object arg
    from_email = Email(kit_email, "Keep in Touch Team")
    # Create to email property from event object arg (the user)
    to_address = event.contacts[0].user.email
    to_name = event.contacts[0].user.fname
    to_email = Email(to_address, to_name)
    # Create mail to be sent (reminder email)
    subject = '{} MESSAGE -- DOUBLE CHECK'.format(event.template.name)
    email_body = "Just wanted to remind you that we'll send this out soon. Let us if you want to make edits: {}".format(event.template.text)
    content = Content("text/plain", email_body)
    mail = Mail(from_email, subject, to_email, content)
    # Send reminder email and print confirmation/status
    response = sg.client.mail.send.post(request_body=mail.get())
    print "REMINDER EMAIL SENT TO USER"
    print(response.status_code)
    print(response.body)
    print(response.headers)
    return True

# Set the schedule's job list
def job():
    """Schedule job instance"""
    today_events = return_todays_events()
    send_all_emails(today_events)
    tmrw_events = return_tmrws_events()
    remind_all_users(tmrw_events)

def schedule1():
    # schedule.every().day.at("00:00").do(job) # Check every day at midnight (for real app)
    schedule.every(2).seconds.do(job)  # Testing/demo purposes
    while True:
        schedule.run_pending()


if __name__ == "__main__": 
    connect_to_db(app)
    print datetime.datetime.now() # check what time it is in vagrant
    schedule1()
