
import sys
import os
import requests
import logging
import json
from datetime import datetime, timedelta
from flask_restful import reqparse, abort, Api, Resource
from flask import request
from flask import jsonify, make_response, redirect, render_template, url_for
from flask import Blueprint

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from settings import *

add_transaction = Blueprint('add_transaction', __name__)
logging.basicConfig(stream=sys.stderr)
logging.getLogger().setLevel(logging.DEBUG)
log = logging.getLogger()

@add_transaction.route("/", methods = ['GET'])
def home():

    token = request.cookies.get('Access-Token')
    log.debug(token)
    if token == None:
        return "No token", 400

    # ---validate user---
    if valid_user(token) == False:
        return "Not logged in", 400

    # ---get user mail---
    headers = {"Access-Token": token}
    response = requests.get(IAM_USER, headers=headers)
    log.debug(response.text)
    if response.status_code != 200:
        return "Invalid Access Token", 400

    user = response.json()['data']['email']
    name = response.json()['data']['name']    
    image = response.json()['data']['picture_url']

    return render_template('add_transaction.html', user=user, name=name, image=image)

def valid_user(token):

    # ---validate user---
    headers = {"Access-Token": token}
    response = requests.post(IAM_VALIDATE, headers=headers)
    log.debug(token)
    log.debug(response.text)

    if response.status_code != 200:
        return False

    return True