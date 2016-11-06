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


@change_state.route("/", methods=['GET'])
def home():
    transaction_id = request.args.get('id')
    state = request.args.get('state')

    token = request.cookies.get('Access-Token')

    if token == None:
        return redirect(LOGIN_PAGE_URL, code=302)

    # ---validate user---
    valid_user(token)

    resp = requests.get(TRANSACTIONS_DETAILS.format(transaction_id))
    if resp.status_code != 200:
        return "ID not found", 400
    info = resp.json()

    data = {'transaction_id': transaction_id,
            'state': state}
    response = requests.post(TRANSACTIONS_UPDATE, data=data)

    if response.status_code != 200:
        return "Error changing transaction state", 400

    data = get_message(state, info['from_uuid'], info['object']['url'])

    response = requests.post(NOTIFICATION_EMAIL, data=data)

    response = redirect(TRANSACTIONS_URL, code=302)
    response.headers['Access-Control-Allow-Origin'] = '*'

    return response


def get_message(state, from_uuid, url):
    resp = requests.get(IAM_USER + "?id=" + from_uuid)
    if resp.status_code != 200:
        return "ID not found", 400
    from_email = json.loads(resp.text)['data']['email']

    if state == 'AWAITING_PAYMENT':
        return {'email': from_email,
                'message': 'The transaction for this item: ' + url + ' has been confirmed and is waiting for your payment.'}
    if state == 'SHIPPED':
        return {'email': from_email,
                'message': 'The item you orded: ' + url + ' has been sended. Complete the transaction on the platform as soon as the item arrives.'}


def valid_user(token):
    # ---validate user---
    headers = {"Access-Token": token}
    response = requests.post(IAM_VALIDATE, headers=headers)

    if response.status_code != 200:
        return redirect(LOGIN_PAGE_URL, code=302)
