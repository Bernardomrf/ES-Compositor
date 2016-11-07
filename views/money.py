
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

money = Blueprint('money', __name__)
logging.basicConfig(stream=sys.stderr)
logging.getLogger().setLevel(logging.DEBUG)
log = logging.getLogger()

@money.route("/", methods = ['GET'])
def home():

    token = request.cookies.get('Access-Token')

    if token == None:
        return redirect(LOGIN_PAGE_URL, code=302)

    # ---validate user---
    valid_user(token)

    headers = {"Access-Token": token, "API-Token" : IAM_CLIENT_SECRET}
    response = requests.get(IAM_USER, headers=headers)

    if response.status_code != 200:
        return "Invalid Access Token", 400

    user = response.json()['data']['email']
    user_id = response.json()['data']['uid']
    name = response.json()['data']['name']
    image = response.json()['data']['picture_url']
    url = PAY_SERVICE_MYCARDS+user_id
    pay_url = PAY_SERVICE_CREATE_CARD

    return render_template('money.html', url=url, user = user, user_id=user_id, pay_url=pay_url, name=name, image=image)

@money.route("/list", methods = ['GET'])
def list():
    token = request.cookies.get('Access-Token')
    if token == None:
        return redirect(LOGIN_PAGE_URL, code=302)
    # ---validate user---
    valid_user(token)

    # ---get user id---
    headers = {"Access-Token": token, "API-Token" : IAM_CLIENT_SECRET}
    response = requests.get(IAM_USER, headers=headers)

    if response.status_code != 200:
        return "Invalid Access Token", 400

    user_id = response.json()['data']['uid']
    headers = {'Accept': 'application/json'}

    response = requests.get(PAY_SERVICE_MYCARDS+user_id, headers=headers)
    info = response.json()

    response = []
    for card in info:

        response.append({'number': str(card['number']),
                        'date' : str(card['expire_month']) + '/' + str(card['expire_year'])
                        })

    return jsonify(response)


def valid_user(token):

    # ---validate user---
    headers = {"Access-Token": token, "API-Token" : IAM_CLIENT_SECRET}
    response = requests.post(IAM_VALIDATE, headers=headers)

    if response.status_code != 200:
        return redirect(LOGIN_PAGE_URL, code=302)
