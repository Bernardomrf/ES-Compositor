
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

dashboard = Blueprint('dashboard', __name__)
logging.basicConfig(stream=sys.stderr)
logging.getLogger().setLevel(logging.DEBUG)
log = logging.getLogger()

@dashboard.route("/", methods = ['GET'])
def home():
    token = request.cookies.get('Access-Token')

    if token == None
        return "Not logged in", 400

    # ---validate user---
    if valid_user(token) == False
        return "Not logged in", 400

    return render_template('index.html')

def valid_user(token):

    # ---validate user---
    headers = {"Access-Token": token}
    response = requests.get(IAM_VALIDATE, headers=headers))

    if response.status_code != 200:
        return False

    return True