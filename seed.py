from sqlalchemy import func
from model import User, Event, ContactEvent, Contact, Template, db, connect_to_db
import datetime

def example_data():
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
    fup = Template(name='follow up', text='hello there')
    ty = Template(name='thank you', text='thank you for meeting!')
    ty2 = Template(name='thank you', text='thank you for meeting!')
    fup2 = Template(name='follow up', text='hello there')
    db.session.add_all([ty, ty2, fup, fup2])
    db.session.commit()
    # ADD EVENTS
    e1 = Event(contact_id=ivw.id, date=datetime.datetime(2017, 12, 30), template_id=fup.id)
    e2 = Event(contact_id=rec.id, template_id=ty.id)
    e3 = Event(contact_id=ivw.id, template_id=ty2.id)
    e4 = Event(contact_id=sec.id, date=datetime.datetime(2018, 1, 1), template_id=fup2.id)
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
    # np = [ ["greet", "Hello"],
    #         ["body", "Thank you for meeting with me"],  
    #         ["sign_off", "Sincerely"] ]
    # greet = Input(name=np[0][0], text=np[0][1])
    # body = Input(name=np[1][0], text=np[1][1])
    # sign_off = Input(name=np[2][0], text=np[2][1])
    # db.session.add_all([greet, body, sign_off])
    # db.session.commit()
    # # Need to add each in association table item in order to be able to call 
    # # .templates on an input instance, and vice versa. 
    # # Is there a way to automatically do so? (same for ContactEvent instances)
    # # ADD TEMPLATEINPUT ASSOCIATIONS
    # ti1 = TemplateInput(template_id=ty.id, input_id=greet.id)
    # ti2 = TemplateInput(template_id=ty.id, input_id=body.id)
    # ti3 = TemplateInput(template_id=ty.id, input_id=sign_off.id)
    # # t2 is not a thankyou so no thank input.name
    # ti10 = TemplateInput(template_id=fup.id, input_id=greet.id)
    # ti20 = TemplateInput(template_id=fup.id, input_id=body.id)
    # ti30 = TemplateInput(template_id=fup.id, input_id=sign_off.id)
    # db.session.add_all([ti1, ti2, ti3, ti10, ti20, ti30])
    # db.session.commit()

if __name__ == "__main__":

    from server import app
    connect_to_db(app)
    db.create_all()
    example_data()