import sendgrid
import os




# $source secrets.sh
sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))

data = {
  "personalizations": [ { "to": [ {"email": "inb125@mail.harvard.edu"},{"email": "akkoreasummer1@gmail.com"} ],
                          
                          "subject": "No_helper success" 

                          } ], 

  "from": { "email": "inb125@mail.harvard.edu" },
  
  "content": [ { "type": "text/plain", 
                 "value": "wooooooo" } ]

}




response = sg.client.mail.send.post(request_body=data)
print(response.status_code)
print(response.body)
print(response.headers)