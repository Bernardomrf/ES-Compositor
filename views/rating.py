
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

rating = Blueprint('rating', __name__)
logging.basicConfig(stream=sys.stderr)
logging.getLogger().setLevel(logging.DEBUG)
log = logging.getLogger()

@rating.route("/", methods = ['GET'])
def home():

    token = request.cookies.get('Access-Token')

    if token == None:
        return redirect(LOGIN_PAGE_URL, code=302)

    # ---validate user---
    valid_user(token)

    # ---get user mail---
    headers = {"Access-Token": token}
    response = requests.get(IAM_USER, headers=headers)

    if response.status_code != 200:
        return "Invalid Access Token", 400

    user = response.json()['data']['email']
    name = response.json()['data']['name']
    image = response.json()['data']['picture_url']

    return render_template('rating.html', user=user, name=name, image=image)

def valid_user(token):

    # ---validate user---
    headers = {"Access-Token": token}
    response = requests.post(IAM_VALIDATE, headers=headers)

    if response.status_code != 200:
        return redirect(LOGIN_PAGE_URL, code=302)
