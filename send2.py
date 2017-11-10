import sendgrid
import json
import os
import time, datetime


# Don't forget to $ source secrets.sh
sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))

event = Event.query.get(event_id)

def convert_to_unix(timeobject):
    """ Takes a datetime object and returns a unix timestamp"""
    
    return time.mktime(timeobject.timetuple()) 


def scheduled_events():
    """ If the day is today, we set the email"""

    today = datetime.datetime.now()

    if [event.date.day, event.date.month, event.date.year] == [today.day, today.month, today.year]:
        send_at_time = convert_to_unix(event.date)

        
def send_email(event):

    to_email = event.contacts[0].email
    to_name = event.contacts[0].name

    from_name = event.contacts[0].fname + event.contacts[0].lname
    from_email = event.contacts[0].email

    subject = event.template.name
    message_text = event.template.text

    data = {
      "send_at": send_at_time, 

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
