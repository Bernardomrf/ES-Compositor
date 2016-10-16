
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

payment = Blueprint('payment', __name__)
logging.basicConfig(stream=sys.stderr)
logging.getLogger().setLevel(logging.DEBUG)
log = logging.getLogger()

@payment.route("/pay", methods = ['GET'])
def pay():

    # ---validate user---
    if valid_user(token) == False:
        return "Not logged in", 400

    url = PAY_SERVICE_INTERFACE #/payments_interface

    response = redirect(url, code=302)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Referer'] = TRANSACTIONS_URL

    return response

def valid_user(token):

    # ---validate user---
    headers = {"Access-Token": token}
    response = requests.post(IAM_VALIDATE, headers=headers)

    if response.status_code != 200:
        return False

    return True
