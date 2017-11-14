import os
from flask import Flask, request, redirect, session
from twilio.twiml.messaging_response import MessagingResponse


# The session object makes use of a secret key.
SECRET_KEY = 'a secret key'
app = Flask(__name__)
app.config.from_object(__name__)

# source secrets
account = os.environ.get('TWILIO_TEST_ACCOUNT')
token = os.environ.get('TWILIO_TEST_TOKEN')
twilio_num = os.environ.get('TWILIO_NUMBER')
my_num = os.environ.get('MY_NUMBER')



callers = {
    twilio_num: "Keep in Touch",
    my_num: "Ada Hackbright",
    # "+14158675310": "Boots",
    # "+14158675311": "Virgil",
}


# @app.route("/sms", methods=['GET', 'POST'])
# def sms_reply():
#     resp = MessagingResponse()
#     resp.message("Hello, this is testing inbound SMS")
#     return str(resp)


# @app.route("/sms", methods=['GET', 'POST'])
# def respond_by_name():
#     """Respond and greet the caller by name."""

#     from_number = request.values.get('From', None)
#     name = callers[from_number] if from_number in callers else "Monkey"

#     resp = MessagingResponse()
#     resp.message("{}, thanks for the message!".format(name))
#     return str(resp)


@app.route("/sms", methods=['GET', 'POST'])
def hello_monkey():
    """Respond with the number of text messages sent between two parties."""

    counter = session.get('counter', 0)

    # increment the counter
    counter += 1

    # Save the new counter value in the session
    session['counter'] = counter

    to_number = request.values.get('To')
    from_number = request.values.get('From', None)
    body = request.values.get('Body', "meow")
    print body
    name = callers[from_number] if from_number in callers else "Monkey"

    message = "{} has messaged {} {} times".format(name, to_number, counter)

    resp = MessagingResponse()
    resp.message(body=message)
    return str(resp)



if __name__ == "__main__":
    app.run(debug=True)