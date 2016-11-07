import sys
import os
import urllib
import uuid
import logging
import requests
import datetime
import json
import base64
from flask_restful import reqparse, abort, Api, Resource
from flask import request, render_template, redirect, make_response
from flask import jsonify
from flask import Blueprint

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from settings import *

dashboard = Blueprint('dashboard', __name__)
logging.basicConfig(stream=sys.stderr)
logging.getLogger().setLevel(logging.DEBUG)

log = logging.getLogger()


@dashboard.route("/", methods=['GET'])
def home():
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

    name = response.json()['data']['name']
    user_id = response.json()['data']['uid']
    image = response.json()['data']['picture_url']

    response = requests.get(TRANSACTIONS_LIST.format(user_id))
    info = response.json()

    total_trans = len(info['to_uuid']) + len(info['from_uuid'])

    pending = 0
    for trans in info['to_uuid']:
        if (trans['state'] != "COMPLETED"):
            pending += 1
    for trans in info['from_uuid']:
        if (trans['state'] != "COMPLETED"):
            pending += 1

    return render_template('index.html', name=name, total_trans=total_trans, pending=pending, image=image)


def valid_user(token):
    # ---validate user---
    headers = {"Access-Token": token, "API-Token" : IAM_CLIENT_SECRET}
    response = requests.post(IAM_VALIDATE, headers=headers)

    if response.status_code != 200:
        return redirect(LOGIN_PAGE_URL, code=302)
