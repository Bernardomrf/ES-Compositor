
import sys
import os
import requests
import logging
import json
import paypalrestsdk
from datetime import datetime, timedelta
from flask_restful import reqparse, abort, Api, Resource
from flask import request
from flask import jsonify, make_response, redirect, render_template, url_for
from flask import Blueprint

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from settings import *

pay_gateway = Blueprint('pay_gateway', __name__)
logging.basicConfig(stream=sys.stderr)
logging.getLogger().setLevel(logging.DEBUG)
log = logging.getLogger()

@pay_gateway.route("/", methods = ['GET'])
def home():

    trans_id=request.args.get('id')
    log.debug(trans_id)

    return render_template('pay_gateway.html', trans_id=trans_id)


@pay_gateway.route("/mb", methods = ['GET'])
def multibanco():
    return render_template('pay_multibanco.html')


@pay_gateway.route("/paypal", methods = ['GET'])
def paypal():
    trans_id=request.args.get('id')
    log.debug(trans_id)

    resp = requests.get(TRANSACTIONS_DETAILS + trans_id + "/")
    if resp.status_code != 200:
        return "ID not found", 400
    info = resp.json()



    paypalrestsdk.configure({"mode": "sandbox",
                            "client_id": PAYPAL_CLIENT_ID,
                            "client_secret": PAYPAL_CLIENT_SECRET})

    payment = paypalrestsdk.Payment({
    "intent": "sale",

    "payer": {
        "payment_method": "paypal"
        },

    "redirect_urls": {
        "return_url": PAY_GATEWAY_CALLBACK_URL + "/?id="+trans_id,
        "cancel_url": PAY_GATEWAY_URL + "/?id="+trans_id
        },

    "transactions": [{

        "item_list": {
            "items": [{
                "name": info['object']['name'],
                "sku": "item",
                "price": info['price'],
                "currency": "EUR",
                "quantity": 1}]},

        "amount": {
            "total": info['price'],
            "currency": "EUR"},
        "description": info['object']['name'] + " " + info['object']['url']}]})

    if payment.create():
        for link in payment.links:
            if link.method == "REDIRECT":
                redirect_url = str(link.href)
                return redirect(redirect_url, 302)
    else:
        return "ERROR"

@pay_gateway.route("/transafe", methods = ['GET'])
def transafe():

    trans_id=request.args.get('id')
    log.debug(trans_id)

    resp = requests.get(TRANSACTIONS_DETAILS + trans_id + "/")
    if resp.status_code != 200:
        return "ID not found", 400
    info = resp.json()


    data = {'user_id1': info['from_uuid'], 'user_id2': info['to_uuid'], 'transaction_id': trans_id, 'amount': info['price'],
            'description': info['object']['name'], 'callback': PAY_GATEWAY_CALLBACK_URL + "?id="+trans_id}
    #response = requests.post(PAY_SERVICE_CREATE_PAYMENT, data=data)

    #log.debug(response.text)
    return redirect(requests.post(PAY_SERVICE_CREATE_PAYMENT, data=data).url, 302)


@pay_gateway.route("/callback", methods = ['GET'])
def callback():
    log.debug("confirmado")
    trans_id=request.args.get('id')

    token = request.cookies.get('Access-Token')

    if token == None:
        return "No token", 400

    # ---validate user---
    if valid_user(token) == False:
        return "Not logged in", 400

    data = {'transaction_id': trans_id,
            'state': 'AWAITING_SHIPPING'}
    response = requests.post(TRANSACTIONS_UPDATE, data=data)

    if response.status_code != 200:
        return "Error changing transaction state", 400

    data = {'email': 'bernardomrf@gmail.com',
            'message': 'AWAITING_SHIPPING'}
    response = requests.post(NOTIFICATION_EMAIL, data=data)

    response = redirect(PAY_GATEWAY_CONFIRMED_URL, code=302)
    response.headers['Access-Control-Allow-Origin'] = '*'

    return response

@pay_gateway.route("/payment_success", methods = ['GET'])
def payment_success():

    return render_template('pay_completed.html')

@pay_gateway.route("/complete", methods = ['GET'])
def complete():
    log.debug("confirmado")
    trans_id=request.args.get('id')

    token = request.cookies.get('Access-Token')

    if token == None:
        return "No token", 400

    # ---validate user---
    if valid_user(token) == False:
        return "Not logged in", 400

    data = {'transaction_id': trans_id}

    response = requests.post(PAY_SERVICE_COMPLETE_PAYMENT, data=data)
    log.debug(response.text)
    if response.status_code != 200:
        return "Error completing payment", 400

    data = {'transaction_id': trans_id,
            'state': 'COMPLETED'}
    response = requests.post(TRANSACTIONS_UPDATE, data=data)

    if response.status_code != 200:
        return "Error changing transaction state", 400

    data = {'email': 'bernardomrf@gmail.com',
            'message': 'AWAITING_SHIPPING'}
    response = requests.post(NOTIFICATION_EMAIL, data=data)

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
