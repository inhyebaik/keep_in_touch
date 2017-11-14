import os
import time, datetime

from flask import Flask, request, redirect, session
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

# source secrets and create client
account = os.environ.get('TWILIO_TEST_ACCOUNT')
token = os.environ.get('TWILIO_TEST_TOKEN')
twilio_num = os.environ.get('TWILIO_NUMBER')
my_num = os.environ.get('MY_NUMBER')
client = Client(account, token)


# The session object makes use of a secret key.
SECRET_KEY = 'a secret key'
app = Flask(__name__)
app.config.from_object(__name__)


callers = {
    twilio_num: "Keep in Touch",
    my_num: "Ada Hackbright",
    # "+14158675310": "Boots",
    # "+14158675311": "Virgil",
}


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


app.route("/sms", methods=['GET', 'POST'])
def handle_reminder_response():
    """Handle user response to reminder"""
    
    t = datetime.datetime.now()
    today = datetime.datetime(t.year, t.month, t.day, 0, 0)

    to_number = request.values.get('To')
    name = callers[from_number] if from_number in callers else "Cool User"
    from_number = request.values.get('From', None)
    user_response = request.values.get('Body', "meow")
    print user_response

    # fetch user from DB to update message
    user = User.query.filter(User.phone == to_number).one()
    
    # unwieldy looping to find the event object...find a better way to do this!
    for contact in user.contacts:
        for event in contact.events:
            if event.date == today:
                event.template.text = user_response

    message = "Thanks, {}! Your new message will be updated as: {}".format(name, user_response)

    resp = MessagingResponse()
    resp.message(body=message)
    return str(resp)



if __name__ == "__main__":
    app.run(debug=True)