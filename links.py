#!/usr/bin/env python2
#-*- encoding: utf8 -*-

# Links app

import sys
import os
from datetime import datetime
from bson.objectid import ObjectId
import pymongo
from bottle import\
        run, \
        debug, \
        request, \
        static_file, \
        get, \
        post, \
        redirect, \
        HTTPError, \
        jinja2_template as template

# MongoDB db name
DBNAME="links"
# Absolute path to static files
STATIC_ROOT="/home/matael/workspace/learn/python/links/static"

#### Tools ####
def connect_db():
    db = pymongo.Connection()
    db = db[DBNAME]
    return db.links


#### Generic Views ####

@get('/static/<filename:path>')
def send_static(filename):
    return static_file(filename, root=STATIC_ROOT)

#### App Views ####

@get('/')
def home():
    """ Home page for a GET request """
    db = connect_db()
    result = db.find().sort('date', pymongo.DESCENDING)
    return template("templates/home.html", result=result)


@post("/new")
@get("/new")
def new_link_form():
    """ display the form for adding quote """
    if not request.POST:
        return template("templates/form.html")

    if request.POST.get("poster") and request.POST.get("url"):
        poster = unicode(request.POST.get("poster").strip(), 'utf8')
        url = unicode(request.POST.get("url").strip(), 'utf8')
        try:
            title = unicode(request.POST.get("title").strip(), 'utf8')
        except KeyError:
            title = url
        print("{}\n{}\n{}".format(poster, url, title))
        db = connect_db()
        db.insert({
            'url': url,
            'title': title,
            'poster': poster,
            'hits': 1,
            'date': datetime.now()
        })
        db.database.connection.disconnect()
        redirect('/')

@get("/goto/<id>")
def goto(id):
    """ Increments hits counter and redirect to the link """
    db = connect_db()
    db.update({"_id": ObjectId(id)}, {"$inc": {"hits": 1}})
    url = db.find_one({"_id": ObjectId(id)})['url']
    db.database.connection.disconnect()
    redirect(url)

debug(True)
run(reloader=True)