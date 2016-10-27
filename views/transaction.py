
import sys
import os
import requests
import logging
import json
import uuid
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
    token = request.cookies.get('Access-Token')

    if token == None:
        return "No token", 400

    # ---validate user---
    if valid_user(token) == False:
        return "Not logged in", 400

    # ---get user mail---
    headers = {"Access-Token": token}
    response = requests.get(IAM_USER, headers=headers)

    if response.status_code != 200:
        return "Invalid Access Token", 400

    user = response.json()['data']['email']
    name = response.json()['data']['name']
    image = response.json()['data']['picture_url']

    return render_template('transaction.html', user=user, image=image, name=name)



@transaction.route("/new", methods = ['POST'])
def new_transaction():
    token = request.cookies.get('Access-Token')
    price = request.form['price']
    seller_email = request.form['seller_email']
    description = request.form['description']
    url = request.form['url']

    # ---validate user---
    if valid_user(token) == False:
        return "Not logged in", 400

    # ---get user id---
    headers = {"Access-Token": token}
    response = requests.get(IAM_USER, headers=headers)

    if response.status_code != 200:
        return "Invalid Access Token", 400

    user_id = response.json()['data']['uid']

    # ---get seller id---
    #headers = {"Access-Token": token} FALAR COM O BRUNO
    headers = {}
    response = requests.get(IAM_USER + "?email=" + seller_email, headers=headers)

    if response.status_code != 200:
        return "Email not found", 400

    seller_id = json.loads(response.text)['data']['uid']
    # response.json()['data']['uid']

    # ---create object---
    data = {'name': description,
            'url': url,
            'identifier' : user_id
            }
    response = requests.post(TRANSACTIONS_NEW_OBJECT, data=data)

    if response.status_code == 400:
        return "Error creating object", 400

    info = response.json()
    object_uuid = info["id"]

    # ---create transaction---

    data = {'to_uuid': seller_id,
            'from_uuid': user_id,
            'object_uuid': object_uuid,
            'price': price,
            'state': "AWAITING_CONFIRMATION"}

    response = requests.post(TRANSACTIONS_NEW, data=data)

    if response.status_code != 201:
        return "Error creating transaction", 400

    response = redirect(TRANSACTIONS_URL, code=302)
    response.headers['Access-Control-Allow-Origin'] = '*'

    return response

@transaction.route("/list", methods = ['GET'])
def list_transactions():

    dataType = request.args.get('dataType')
    token = request.cookies.get('Access-Token')

    # ---validate user---
    if valid_user(token) == False:
        return "Not logged in", 400

    # ---get user id---
    headers = {"Access-Token": token}
    response = requests.get(IAM_USER, headers=headers)

    if response.status_code != 200:
        return "Invalid Access Token", 400

    user_id = response.json()['data']['uid']

    # ---get transaction list---
    response = requests.get(TRANSACTIONS_LIST + user_id + "/")
    info = response.json()

    if response.status_code != 200:
        return "Error retrieving transactions list", 400

    response = []
    if dataType == "seller":
        for trans in info['to_uuid']:

            resp = requests.get(IAM_USER + "?id=" + trans['from_uuid'])
            if resp.status_code != 200:
                return "ID not found", 400

            response.append({'state': transformState(trans['state']),
                            'buyer' : json.loads(resp.text)['data']['email'],
                            'price' : trans['price'],
                            'url' : trans['object']['url'],
                            'actions': action(dataType, trans['state'], trans['id'])
                            })
    elif dataType == "buyer":
        for trans in info['from_uuid']:

            resp = requests.get(IAM_USER + "?id=" + trans['to_uuid'])
            if resp.status_code != 200:
                return "ID not found", 400

            response.append({'state': transformState(trans['state']),
                            'seller' : json.loads(resp.text)['data']['email'],
                            'price' : trans['price'],
                            'url' : trans['object']['url'],
                            'actions': action(dataType  , trans['state'], trans['id'])
                            })

    return jsonify(response)

def valid_user(token):

    # ---validate user---
    headers = {"Access-Token": token}
    response = requests.post(IAM_VALIDATE, headers=headers)

    if response.status_code != 200:
        return False

    return True

def transformState(state):
    if state == "AWAITING_CONFIRMATION":
        return "<span class=\"badge\">Awaiting Confirmation</span>"
    elif state == "AWAITING_PAYMENT":
        return "<span class=\"badge\">Awaiting Payment</span>"
    elif state == "AWAITING_SHIPPING":
        return "<span class=\"badge\">Awaiting Shipment</span>"
    elif state == "SHIPPED":
        return "<span class=\"badge\">Shiped</span>"
    elif state == "COMPLETED":
        return "<span class=\"badge\">Success</span>"
    elif state == "REFUND":
        return "<span class=\"badge\">Refund</span>"

def action(dataType, state, id):

    if dataType == "buyer":
        if state == "AWAITING_PAYMENT":
            return "<a href=\"/change_state?id="+ id +"&state=AWAITING_SHIPPING\" class=\"btn btn-default\">Pay</a>"
        elif state == "SHIPPED":
            return "<a href=\"/change_state?id="+ id +"&state=COMPLETED\" class=\"btn btn-default\">Received</a>"
        else:
            return "None"
    elif dataType == "seller":
        if state == "AWAITING_CONFIRMATION":
            return "<a href=\"/change_state?id="+ id +"&state=AWAITING_PAYMENT\" class=\"btn btn-default\">Confirm</a>"
        elif state == "AWAITING_SHIPPING":
            return "<a href=\"/change_state?id="+ id +"&state=SHIPPED\" class=\"btn btn-default\">Sended</a>"
        else:
            return "None"
