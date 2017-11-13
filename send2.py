import sendgrid
import json
import os
import time, datetime
import schedule


def job():
    """Checks if there are any events today."""
    today = datetime.datetime.now()
    todays_events = Event.query.filter(Event.date == today).all()
    if todays_events == []:
        return "No events!"
    else:
        return todays_events


schedule.every(5).seconds.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
# schedule.every().day.at("00:00").do(return_todays_events)
# schedule.every(3).seconds.do(return_todays_events)

def return_todays_events():
    """Checks if there are any events today."""
    # Query for events for dates for today 
    today = datetime.datetime.now()
    todays_events = Event.query.filter(Event.date == today).all()
    if todays_events == []:
        return "No events!"
    else:
        return todays_events


def remind_all_users(events):
    """ Takes a list of today's events (Event objects) and sends out emails
        to the user 
    """ 
    for event in events:
        remind_user(event)


def send_all_emails(events):
    """ Takes a list of today's events (Event objects) and sends out emails 
        to the contact
    """ 
    for event in events:
        send_email(event)


def send_email(event):

    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    to_email = event.contacts[0].email
    to_name = event.contacts[0].name

    from_name = event.contacts[0].fname + event.contacts[0].lname
    from_email = event.contacts[0].email

    subject = event.template.name
    message_text = event.template.text

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
            {
              "email": email2,
              "name": name2
            }
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



def remind_user(event):

    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    to_email = event.contacts[0].user.email
    to_name = event.contacts[0].user.fname

    from_name = "Keep in Touch Team"
    from_email = "inb125@mail.harvard.edu"

    subject = "Reminder to Keep in Touch with {}".format(event.contacts[0].name)
    message_text = "Just wanted to remind you that {} is coming up and we will send a {} for {} soon!".format(event.date, event.template.name, event.contacts[0].name)

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
            {
              "email": email2,
              "name": name2
            }
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
    """ Takes a datetime object and returns a unix timestamp"""
    return time.mktime(timeobject.timetuple()) 










# SendGrid stuff 


def convert_to_unix():
    """ Takes a datetime object and returns a unix timestamp in 3 seconds later"""
    now = datetime.datetime.now()
    # five seconds later
    f = now + datetime.timedelta(seconds=5)
    return time.mktime(f.timetuple()) 


def scheduled_events():
    """ If the day is today, we set the email"""

    today = datetime.datetime.now()

    if [event.date.day, event.date.month, event.date.year] == [today.day, today.month, today.year]:
        send_at_time = convert_to_unix(event.date)

        




