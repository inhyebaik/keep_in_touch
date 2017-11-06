from model import User, Event, ContactEvent, Contact, Template, TemplateInput, Input, db
import datetime


# ADD USERS
jane = User(email='j@gmail.com', password='a', fname='Jane', lname='Hacks')
bob = User(email='h@gmail.com', password='a', fname='Bob', lname='Baller')
db.session.add_all([jane, bob])
db.session.commit()
# ADD CONTACTS
rec = Contact(name='John Recruitor', email='jr@gmail.com', user_id=jane.id)
sec = Contact(name='Sally Secretary', email='ss@gmail.com', user_id=bob.id)
ivw = Contact(name='Ian Interviewer', email='i@gmail.com', user_id=bob.id)
db.session.add_all([rec, sec, ivw])
db.session.commit()
# ADD TEMPLATES
ty = Template(name='thank you', text='thank you for meeting!')
fup = Template(name='follow up', text='hello there')
db.session.add_all([ty, fup])
db.session.commit()
# ADD EVENTS
e1 = Event(contact_id=ivw.id, date=datetime.datetime(2017, 12, 30), template_id=fup.id)
e2 = Event(contact_id=rec.id, template_id=ty.id)
e3 = Event(contact_id=ivw.id, template_id=ty.id)
e4 = Event(contact_id=sec.id, date=datetime.datetime(2018, 1, 1), template_id=fup.id)
db.session.add_all([e1, e2, e3, e4])
db.session.commit()
# ADD CONTACTEVENT ASSOCIATIONS
ce1 = ContactEvent(contact_id=e1.contact_id, event_id=e1.id)
ce2 = ContactEvent(contact_id=e2.contact_id, event_id=e2.id)
ce3 = ContactEvent(contact_id=e3.contact_id, event_id=e3.id)
ce4 = ContactEvent(contact_id=e4.contact_id, event_id=e4.id)
db.session.add_all([ce1, ce2, ce3, ce4])
db.session.commit()
# ADD INPUTS
np = [ ["greeting", "how do you want to greet?"],
        ["thanks", "What do you want to thank them for?"],  
        ["memory", "what memory did you want to mention?"],
        ["sign_off", "how do you want to sign off?"] ]
igreet = Input(name=np[0][0], prompt=np[0][1])
ithank = Input(name=np[1][0], prompt=np[1][1])
imemory = Input(name=np[2][0], prompt=np[2][1])
isignoff = Input(name=np[3][0], prompt=np[3][1])
db.session.add_all([igreet, ithank, imemory, isignoff])
db.session.commit()
# Need to add each in association table item in order to be able to call 
# .templates on an input instance, and vice versa. 
# Is there a way to automatically do so? (same for ContactEvent instances)
# ADD TEMPLATEINPUT ASSOCIATIONS
ti1 = TemplateInput(template_id=ty.id, input_id=igreet.id)
ti2 = TemplateInput(template_id=ty.id, input_id=ithank.id)
ti3 = TemplateInput(template_id=ty.id, input_id=imemory.id)
ti4 = TemplateInput(template_id=ty.id, input_id=isignoff.id)
# t2 is not a thankyou so no thank input.name
ti10 = TemplateInput(template_id=fup.id, input_id=igreet.id)
ti30 = TemplateInput(template_id=fup.id, input_id=imemory.id)
ti40 = TemplateInput(template_id=fup.id, input_id=isignoff.id)
db.session.add_all([ti1, ti2, ti3, ti4, ti10, ti30, ti40])
db.session.commit()

