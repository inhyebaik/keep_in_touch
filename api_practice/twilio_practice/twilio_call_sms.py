import os
from flask import Flask, request, redirect, session
from twilio.rest import Client

account = os.environ.get('TWILIO_TEST_ACCOUNT')
token = os.environ.get('TWILIO_TEST_TOKEN')
twilio_num = os.environ.get('TWILIO_NUMBER')
my_num = os.environ.get('MY_NUMBER')

client = Client(account, token)

my_msg = "hello"

# Make a Call
call = client.calls.create(to=my_num,
                           from_=twilio_num,
                           url="http://twimlets.com/holdmusic?Bucket=com.twilio.music.ambient")
print(call.sid)


# Send an SMS
message = client.messages.create(to=my_num, from_=twilio_num, body=my_msg)