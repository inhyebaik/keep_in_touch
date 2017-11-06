from model import User, Event, ContactEvent, Contact, Template, TemplateInput, Input, db
import datetime

np = [ ["greeting", "how do you want to greet?"],
        ["thank", "What do you want to thank them for?"],  
        ["memory", "what memory did you want to mention?"],
        ["sign_off", "how do you want to sign off?"] ]

# ADD USERS
jane = User(email='j@gmail.com', password='a', fname='Jane', lname='Hacks')
bob = User(email='h@gmail.com', password='a', fname='Bob', lname='Baller')
db.session.add_all([jane, bob])
db.session.commit()

# ADD CONTACTS
c1 = Contact(name='John Recruitor', email='jr@gmail.com', user_id=jane.id)
c2 = Contact(name='Sally Secretary', email='ss@gmail.com', user_id=bob.id)
db.session.add_all([c1, c2])
db.session.commit()

# ADD TEMPLATES 
t1 = Template(name='thank you', text='thank you for meeting!')
t2 = Template(name='follow up', text='hello there')
db.session.add_all([t1, t2])
db.session.commit()

# ADD EVENTS
e1 = Event(contact_id=c1.id, date=datetime.datetime(2017, 12, 30), template_id=t1.id)
e2 = Event(contact_id=c1.id, template_id=t2.id)
e3 = Event(contact_id=c2.id, date=datetime.datetime(2018, 1, 1), template_id=t1.id)
db.session.add_all([e1, e2, e3])
db.session.commit()

# ADD CONTACTEVENT ASSOCIATIONS
ce1 = ContactEvent(contact_id=e1.contact_id, event_id=e1.id)
ce2 = ContactEvent(contact_id=e2.contact_id, event_id=e2.id)
ce3 = ContactEvent(contact_id=e3.contact_id, event_id=e3.id)
db.session.add_all([ce1, ce2, ce3])
db.session.commit()

# ADD INPUTS
i1 = Input(name=np[0][0], prompt=np[0][1])
i2 = Input(name=np[1][0], prompt=np[1][1])
i3 = Input(name=np[2][0], prompt=np[2][1])
i4 = Input(name=np[3][0], prompt=np[3][1])
db.session.add_all([i1, i2, i3, i4])
db.session.commit()

# Need to add each in association table item in order to be able to call 
# .templates on an input instance, and vice versa. 
# Is there a way to automatically do so? (same for ContactEvent instances)

# ADD TEMPLATEINPUT ASSOCIATIONS
ti1 = TemplateInput(template_id=t1.id, input_id=i1.id)
ti2 = TemplateInput(template_id=t1.id, input_id=i2.id)
ti3 = TemplateInput(template_id=t1.id, input_id=i3.id)
ti4 = TemplateInput(template_id=t1.id, input_id=i4.id)
# t2 is not a thankyou so no thank input.name
ti10 = TemplateInput(template_id=t2.id, input_id=i1.id)
ti30 = TemplateInput(template_id=t2.id, input_id=i3.id)
ti40 = TemplateInput(template_id=t2.id, input_id=i4.id)
db.session.add_all([ti1, ti2, ti3, ti4, ti10, ti30, ti40])
db.session.commit()


    # u1c2 = Contact(name='John Recruitor', email='r@gmail.com', user_id=u1.id)

    

    # u2 = User(email='a@gmail.com', password='a', fname='An', lname='Smith')
    # u2c1 = Contact(name='Carl', email='c@gmail.com', user_id=u2.id)


    # db.session.add_all([u1, u2, u3, m1, m2, m3, g1, g2, g3])
    # db.session.commit()
    # db.session.add_all([r1, r2, r3, r4, r5, r6, r7, r8, mg1, mg2, mg3, mg4, mg5])
    # db.session.commit()
