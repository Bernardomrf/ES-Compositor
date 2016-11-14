
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
from flask import request, render_template, redirect, make_response, url_for
from flask import jsonify
from flask import Blueprint

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from settings import *

gateway = Blueprint('gateway', __name__)
logging.basicConfig(stream=sys.stderr)
logging.getLogger().setLevel(logging.DEBUG)
log = logging.getLogger()

@gateway.route("/", methods = ['GET'])
def home():
    token = request.cookies.get('Access-Token')

    if valid_user(token) == True:
        response = redirect(DASHBOARD_URL, code=302)
        response.headers['Access-Control-Allow-Origin'] = '*'

        return response

    headers = {"API-Token": IAM_CLIENT_SECRET}
    response = requests.get(IAM_USERS_COUNT, headers=headers)
    user_count = response.json()["data"]

    response = requests.get(TRANSACTIONS_STATS)
    number_transactions = response.json()["number_of_transactions"]
    total_amount = response.json()["total_value"]["price__sum"]
    log.debug(number_transactions)
    log.debug(number_transactions-response.json()["number_of_refunded"])
    log.debug(float((number_transactions-response.json()["number_of_refunded"]))

    success_rate = int(float((number_transactions-response.json()["number_of_refunded"])/number_transactions)*100)
    return render_template('login.html', users=user_count, transactions=number_transactions, amount=total_amount, success_rate=success_rate)

def valid_user(token):

    # ---validate user---
    headers = {"Access-Token": token, "API-Token" : IAM_CLIENT_SECRET}
    response = requests.post(IAM_VALIDATE, headers=headers)

    if response.status_code != 200:
        return False

    return True
