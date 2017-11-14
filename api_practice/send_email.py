import os
from sendgrid.helpers.mail import *
import sendgrid

message = Mail()

# $source secrets.sh
sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY')) 

from_email = Email("inb125@mail.harvard.edu")
to_email = Email("inb125@mail.harvard.edu")
subject = "Remember to Keep in Touch"

email_body = "hello hello hello"

content = Content("text/plain", email_body)
mail = Mail(from_email, subject, to_email, content)

response = sg.client.mail.send.post(request_body=mail.get())
print(response.status_code)
print(response.body)
print(response.headers)