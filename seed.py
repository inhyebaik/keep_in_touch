from sqlalchemy import func
from model import User, Event, ContactEvent, Contact, Template, db, connect_to_db
import datetime
import os


def example_data():
    phone = os.environ.get('MY_NUMBER')
    email = os.environ.get('MY_EMAIL')
    fb_at = os.environ.get('FB_AT')
    fb_uid = os.environ.get('FB_UID')

# ADD USERS
    jane = User(email='j@gmail.com', password='a', fname='Jane', lname='Hacks', phone='+11234567890')
    bob = User(email='h@gmail.com', password='a', fname='Bob', lname='Baller', phone='+10987654321')
    # inny = User(email=email, password='a', fname='Inny', lname='HB', phone=phone, fb_uid=fb_uid, fb_at=fb_at)
    db.session.add_all([jane, bob])
    # db.session.add(inny)
    db.session.commit()
    # ADD CONTACTS
    john = Contact(name='John Recruitor', email='jr@gmail.com', user_id=jane.id)
    sally = Contact(name='Sally Secretary', email='ss@gmail.com', user_id=bob.id)
    ian = Contact(name='Ian Interviewer', email='i@gmail.com', user_id=bob.id)
    db.session.add_all([john, sally, ian])
    db.session.commit()
    # ADD TEMPLATES
    fup = Template(name='follow up', text='hello there')
    ty = Template(name='thank you', text='thank you for meeting!')
    ty2 = Template(name='thank you', text='thank you for meeting!')
    fup2 = Template(name='follow up', text='hello there')
    db.session.add_all([ty, ty2, fup, fup2])
    db.session.commit()
    # ADD EVENTS
    e1 = Event(contact_id=ian.id, date=datetime.datetime(2017, 12, 30), template_id=fup.id)
    e2 = Event(contact_id=john.id, template_id=ty.id)
    e3 = Event(contact_id=ian.id, template_id=ty2.id)
    e4 = Event(contact_id=sally.id, date=datetime.datetime(2018, 1, 1), template_id=fup2.id)
    db.session.add_all([e1, e2, e3, e4])
    db.session.commit()
    # ADD CONTACTEVENT ASSOCIATIONS
    ce1 = ContactEvent(contact_id=e1.contact_id, event_id=e1.id)
    ce2 = ContactEvent(contact_id=e2.contact_id, event_id=e2.id)
    ce3 = ContactEvent(contact_id=e3.contact_id, event_id=e3.id)
    ce4 = ContactEvent(contact_id=e4.contact_id, event_id=e4.id)
    db.session.add_all([ce1, ce2, ce3, ce4])
    db.session.commit()
    

if __name__ == "__main__":

    from server import app
    connect_to_db(app)
    db.create_all()
    example_data()