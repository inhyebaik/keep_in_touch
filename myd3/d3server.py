"""Short Flask server to illustrate ajax post from lots of buttons"""


# helper functions
# a = ['Allian,jessica', 'Elsa,meggie', 'Leilani,lavinia', 'Florence,rachel', 'Celia,leslie', 'Alice,heather', 'Meg,lavinia', 'Rebekkah,meggie', 'Kara,rachel', 'Kaylie,leslie', 'Malika,leslie', 'Kristin,rachel', 'Chelsea,rachel', 'Melissa,meggie', 'Vianey,rachel', 'Emily,jessica', 'Marisha,lavinia', 'Anli,lavinia', 'Dori,heather', 'Tiffany,heather', 'Janet,leslie', 'Patricia,heather', 'Terri,heather', 'Shai,jessica', 'Shijie,ally', 'Katie,lavinia', 'Annie,leslie', 'Megan,ally', 'Chandrika,leslie', 'Shalini,heather', 'Alitsiya,lavinia', 'Doria,jessica', 'Amy,cynthia', 'Alena,ally', 'Erin,meggie', 'Emma,ally']
from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session,
                   jsonify)
# from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from model import User, Event, ContactEvent, Contact, Template, db, connect_to_db
import random
from werkzeug.security import generate_password_hash, check_password_hash
# from quotes import *

# Email sending
import os, time, json, datetime


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"
app.jinja_env.undefined = StrictUndefined # raise error if you use undefined variable in Jinja2


# D3 stuff #####################################

def make_d3_csv():
    """Takes data from DB to make data for d3."""

    user = User.query.get(1)

    nodes = []
    for contact in user.contacts:
        for event in contact.events:
            nodes.append({'contact':contact.name, 'event':{'name': event.name, 'date': event.date}})

    index_nodes = {}
    for idx,n in enumerate(nodes):
        index_nodes[n['event']] = (idx, n['contact'])
    print "index_nodes:"
    print index_nodes

    paths = []
    # for line in lines:
    #     paths.append({'source': })

def make_nodes_and_paths2(filename):


    user = User.query.get(1)

    nodes1 = []
    for contact in user.contacts:
        for event in contact.events:
            nodes1.append({'contact':contact.name, 'event':{'name': event.name, 'date': event.date}})

    index_nodes1 = {}
    for idx,n in enumerate(nodes1):
        index_nodes1[n['event']] = (idx, n['contact'])
    print "index_nodes1:"
    print index_nodes1


    file_obj = open(filename)
    contents = file_obj.read()
    lines = contents.split('\n')

    nodes = {}
    for pair in lines:
        split = pair.split(',')
        if split:
            for person in split:
                person = person.strip()
                if not nodes.get(person):
                    nodes[person] = split[1].strip()
    print nodes
    nodes = [{'name':person, 'adviser': nodes[person]} for person in nodes.keys()]
    print nodes

    index_nodes = {}
    for idx, n in enumerate(nodes):
        index_nodes[n['name']] = (idx, n['adviser'])

    paths = []
    for line in lines:
        slt = line.split(',')
        if len(slt) == 2:
            source, target = slt
            paths.append({'source': index_nodes[source][0], 'target': index_nodes[target][0]  })

    return nodes, paths


def make_nodes_and_paths(filename):

    file_obj = open(filename)
    contents = file_obj.read()
    lines = contents.split('\n')

    nodes = {}
    for pair in lines:
        split = pair.split(',')
        if split:
            for person in split:
                person = person.strip()
                if not nodes.get(person):
                    nodes[person] = split[1].strip()
    print nodes
    nodes = [{'name':person, 'adviser': nodes[person]} for person in nodes.keys()]
    print nodes

    index_nodes = {}
    for idx, n in enumerate(nodes):
        index_nodes[n['name']] = (idx, n['adviser'])

    paths = []
    for line in lines:
        slt = line.split(',')
        if len(slt) == 2:
            source, target = slt
            paths.append({'source': index_nodes[source][0], 'target': index_nodes[target][0]  })

    return nodes, paths


@app.route("/d3")
def index():
    """Return homepage."""
    return render_template("d3example.html")


@app.route('/d3advanced')
def index_advanced():
    """Return homepage."""
    return render_template("d3advanced.html")


@app.route("/data.json")
def get_graph_data():
    # call helper functions
    nodes, paths = make_nodes_and_paths2('data.csv')
    return jsonify({'nodes':nodes, 'paths':paths})


if __name__ == "__main__":
    app.run(debug=True)
