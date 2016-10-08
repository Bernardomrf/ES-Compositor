
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

transaction = Blueprint('transaction', __name__)
logging.basicConfig(stream=sys.stderr)
logging.getLogger().setLevel(logging.DEBUG)
log = logging.getLogger()

@transaction.route("/", methods = ['GET'])
def home():
    return render_template('transaction.html')



@transaction.route("/new", methods = ['POST'])
def new_transaction():
    token = request.cookies.get('Access-Token')
    price = request.form['price']
    seller_email = request.form['seller_email']
    description = request.form['description']
    url = request.form['url']

    # ---validate user---
    if valid_user(token) == False
        return "Not logged in", 400

    # ---get user id---
    headers = {"Access-Token": token}
    response = requests.get(IAM_USER, headers=headers)

    if response.status_code != 200:
        return "Invalid Access Token", 400

    info = response.json()
    user_id = info['uuid']

    # ---get seller id---
    headers = {"Access-Token": token}
    response = requests.get(IAM_USER + "?email=" + seller_email, headers=headers)

    if response.status_code != 200:
        return "Email not found", 400

    seller_id = response.data['uuid']

    # ---create object---
    data = {'name': description, 'url': url }
    response = requests.post(NEW_OBJECT, data=data)

    if response.status_code != 200:
        return "Error creating object", 400

    object_uuid = response.data["id"]

    # ---create transaction---
    data = {'to_uuid': seller_id,
            'from_uuid': user_id,
            'object_uuid': object_uuid,
            'price': price,
            'state': "AWAITING_CONFIRMATION"}

    response = requests.post(NEW_TRANSACTION, data=data)

    if response.status_code != 200:
        return "Error creating transaction", 400

    response = redirect(TRANSACTIONS_URL, code=302)
    response.headers['Access-Control-Allow-Origin'] = '*'

    return response



@transaction.route("/confirm", methods = ['POST'])
def confirm_transaction():

    token = request.cookies.get('Access-Token')
    transaction_id = request.headers.get('transaction_id')

    if valid_user(token) == False
        return "Not logged in", 400

    return change_state('WAITING_PAYMENT', transaction_id)



@transaction.route("/pay", methods = ['POST'])
def payed_transaction():

    token = request.cookies.get('Access-Token')
    transaction_id = request.headers.get('transaction_id')

    if valid_user(token) == False
        return "Not logged in", 400

    return change_state('PAYED', transaction_id)



@transaction.route("/transit", methods = ['POST'])
def in_transit_transaction():

    token = request.cookies.get('Access-Token')
    transaction_id = request.headers.get('transaction_id')

    if valid_user(token) == False
        return "Not logged in", 400

    return change_state('IN_TRANSIT', transaction_id)



@transaction.route("/success", methods = ['POST'])
def successfull_transaction():

    token = request.cookies.get('Access-Token')
    transaction_id = request.headers.get('transaction_id')

    if valid_user(token) == False
        return "Not logged in", 400

    return change_state('SUCCESS', transaction_id)



@transaction.route("/refund", methods = ['POST'])
def refund_transaction():

    token = request.cookies.get('Access-Token')
    transaction_id = request.headers.get('transaction_id')

    if valid_user(token) == False
        return "Not logged in", 400

    return change_state('REFUND', transaction_id)



def change_state(state, transaction_id):

    # ---change transaction state---
    data = {'transaction_id': transaction_id,
            'state': state}
    response = requests.post(UPDATE_TRANSACTION, data=data)

    if response.status_code != 200:
        return "Error changing transaction state", 400

    response = redirect(TRANSACTIONS_URL, code=302)
    response.headers['Access-Control-Allow-Origin'] = '*'

    return response



@transaction.route("/list", methods = ['GET'])
def list_transactions():
    token = request.cookies.get('Access-Token')

    # ---validate user---
    if valid_user(token) == False
        return "Not logged in", 400

    # ---get user id---
    headers = {"Access-Token": token}
    response = requests.get(IAM_USER, headers=headers)

    if response.status_code != 200:
        return "Invalid Access Token", 400

    info = response.json()
    user_id = info['uuid']

    # ---get transaction list---
    response = requests.get(TRANSACTIONS_LIST + "?identifier=" + user_id + "/")

    if response.status_code != 200:
        return "Error retrieving transactions list", 400

    return response.json()


def valid_user(token):

    # ---validate user---
    headers = {"Access-Token": token}
    response = requests.get(IAM_VALIDATE, headers=headers))

    if response.status_code != 200:
        return False

    return True
