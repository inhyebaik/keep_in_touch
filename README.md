# Keep in Touch

![alt text](https://github.com/inhyebaik/keep_in_touch/blob/master/static/readmepics/index.png "Keep in Touch index page")


Keep in Touch automates keeping in touch for you. Register through Facebook OAuth gives the app permissions for their friends list, automatically importing friends as contacts. On the user's profile, each contact card shows their scheduled messages (past events appear faded). Upcoming scheduled events appear in the Queued Messages section. 


![alt text](https://github.com/inhyebaik/keep_in_touch/blob/master/static/readmepics/profile.png "Keep in Touch User Profile")


Users can schedule messages for each contact, given their email and U.S. phone number. Messages can be customized or selected from a list of general-purpose messages (scraped from the web using Scrapy). Clicking the option for type of message returns a random message filled in the new message text area. 


![alt text](https://github.com/inhyebaik/keep_in_touch/blob/master/static/readmepics/neweventform.png "Keep in Touch new event form")


A separate schedule app threaded to the server queries the database for any events to be sent out that day. Keep in Touch will send out messages to contacts when the day comes.  


![alt text](https://github.com/inhyebaik/keep_in_touch/blob/master/static/readmepics/emailreceived.png "Keep in Touch contact inbox")


Keep in Touch will also send users a reminder email and text of upcoming events. By responding to reminder texts, users can update/edit messages directly updating the database given a unique event_id number at the end. The Twilio API is configured using ngrok to tunnel traffic to the local host. 


![alt text](https://github.com/inhyebaik/keep_in_touch/blob/master/static/readmepics/updatedbsms.png "Keep in Touch SMS update")



Keep in Touch is built using:
..*Python
..*JavaScript
..*PostgreSQL
..*Flask
..*SQLAlchemy
..*jQuery
..*Jinja
..*Masrony
..*Scrapy


APIs: 
..*[Twilio](https://github.com/twilio)
..*[SendGrid](https://github.com/sendgrid)
..*[Facebook OAuth](https://developers.facebook.com/docs/facebook-login/web). 