
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

tracking = Blueprint('tracking', __name__)
logging.basicConfig(stream=sys.stderr)
logging.getLogger().setLevel(logging.DEBUG)
log = logging.getLogger()

@tracking.route("/", methods = ['GET'])
def home():
    trans_id = request.args.get('id')

    token = request.cookies.get('Access-Token')

    if token == None:
        return redirect(LOGIN_PAGE_URL, code=302)

    # ---validate user---
    valid_user(token)

    # ---get user mail---
    headers = {"Access-Token": token, "API-Token" : IAM_CLIENT_SECRET}
    response = requests.get(IAM_USER, headers=headers)

    if response.status_code != 200:
        return "Invalid Access Token", 400

    user = response.json()['data']['email']
    name = response.json()['data']['name']
    image = response.json()['data']['picture_url']

    return render_template('tracking.html', user=user, name=name, image=image, id=trans_id)

@tracking.route("/submit", methods = ['POST'])
def submit():
    trans_id = request.args.get('id')

    token = request.cookies.get('Access-Token')

    if token == None:
        return redirect(LOGIN_PAGE_URL, code=302)

    tracking = request.form['tracking']

    # ---validate user---
    valid_user(token)

    # ---add track number---

    data = {'transaction_id': trans_id,
            'tracking_code': tracking}

    response = requests.post(TRANSACTIONS_TRACKING, data=data)

    if response.status_code != 200:
        return "Error creating transaction", 400

    response = redirect(TRANSACTIONS_URL, code=302)
    response.headers['Access-Control-Allow-Origin'] = '*'

    return response

def valid_user(token):

    # ---validate user---
    headers = {"Access-Token": token, "API-Token" : IAM_CLIENT_SECRET}
    response = requests.post(IAM_VALIDATE, headers=headers)

    if response.status_code != 200:
        return redirect(LOGIN_PAGE_URL, code=302)
