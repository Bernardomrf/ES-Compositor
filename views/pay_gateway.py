
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

    return render_template('pay_gateway.html')

@pay_gateway.route("/paypal", methods = ['GET'])
def paypal():

    paypalrestsdk.configure({"mode": "sandbox",
                            "client_id": PAYPAL_CLIENT_ID,
                            "client_secret": PAYPAL_CLIENT_SECRET})

    payment = paypalrestsdk.Payment({
    "intent": "sale",

    "payer": {
        "payment_method": "paypal"
        },

    "redirect_urls": {
        "return_url": "http://transafe.rafaelferreira.pt/pay_gateway/callback",
        "cancel_url": "http://localhost:3000/pay_gateway/cancel"
        },

    "transactions": [{

        "item_list": {
            "items": [{
                "name": "item",
                "sku": "item",
                "price": "5.00",
                "currency": "EUR",
                "quantity": 1}]},

        "amount": {
            "total": "5.00",
            "currency": "EUR"},
        "description": "This is the payment transaction description."}]})

    if payment.create():
        for link in payment.links:
            if link.method == "REDIRECT":
                redirect_url = str(link.href)
                return redirect(redirect_url, 302)
    else:
        return "ERROR"

@pay_gateway.route("/transafe", methods = ['GET'])
def transafe():
    log.debug("TRANSAFE")

    pass

@pay_gateway.route("/callback", methods = ['GET'])
def callback():
    # Chance state
    pass

def valid_user(token):

    # ---validate user---
    headers = {"Access-Token": token}
    response = requests.post(IAM_VALIDATE, headers=headers)

    if response.status_code != 200:
        return False

    return True
