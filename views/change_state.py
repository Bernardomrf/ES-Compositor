
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

change_state = Blueprint('change_state', __name__)
logging.basicConfig(stream=sys.stderr)
logging.getLogger().setLevel(logging.DEBUG)
log = logging.getLogger()

@change_state.route("/", methods = ['GET'])
def home():

    transaction_id = request.args.get('id')
    state = request.args.get('state')

    token = request.cookies.get('Access-Token')

    if token == None:
        return "No token", 400

    # ---validate user---
    if valid_user(token) == False:
        return "Not logged in", 400

    data = {'transaction_id': transaction_id,
            'state': state}
    response = requests.post(TRANSACTIONS_UPDATE, data=data)

    if response.status_code != 200:
        return "Error changing transaction state", 400

    response = redirect(TRANSACTIONS_URL, code=302)
    response.headers['Access-Control-Allow-Origin'] = '*'

    return response

def valid_user(token):

    # ---validate user---
    headers = {"Access-Token": token}
    response = requests.post(IAM_VALIDATE, headers=headers)

    if response.status_code != 200:
        return False

    return True
