
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


    return render_template('login.html')

def valid_user(token):

    # ---validate user---
    headers = {"Access-Token": token}
    response = requests.post(IAM_VALIDATE, headers=headers)
    log.debug(token)
    log.debug(response.text)

    if response.status_code != 200:
        return False

    return True
