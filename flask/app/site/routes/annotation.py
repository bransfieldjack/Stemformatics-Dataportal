import flask
import os
from smtplib import SMTP
from flask import Flask, session, Blueprint, render_template, request, Response, redirect, url_for, jsonify
from app.api.models import datasets, UserModel, _runSql
import pymongo
from pymongo import MongoClient
import flask_login
from bson.json_util import dumps

"""
The page that this route is rendering gets most of its functionality
(get/post requests) from the API, which is why there arent many methods required in this route. 
"""

module = Blueprint('annotation', __name__)
mongo_uri = os.environ["MONGO_URI"]


@module.route('/annotation')
def annotation():
    
    if session["loggedIn"] == True:
        user = session["user"]
        return render_template('/api/annotation.html', user=user)
    else:
        return redirect('/login_error')


@module.route("/summary_table_mongo", methods=['GET', 'POST'])
def summary_table_mongo():
    
    myclient = pymongo.MongoClient(mongo_uri) # Mongo container name is 'mongo'. # local mongodb server.   # Connects to the mongodb daabase and returns everything.
    database = myclient["dataportal_prod_meta"]
    collection = database["datasets"]
    result = collection.find()
    dict_list = []
    for item in result:
        obj = {
            "data": item
        }
        dict_list.append(obj)
    dict_list.pop(1)

    if session["loggedIn"] == True:
        return dumps(dict_list)
    else:
        return "Access Denied"

