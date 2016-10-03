
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

authorization = Blueprint('authorization', __name__)
logging.basicConfig(stream=sys.stderr)
logging.getLogger().setLevel(logging.DEBUG)
log = logging.getLogger()

"""
@authorization.route("/", methods = ['GET'])
def home():
    return render_template('index.html')
"""
@authorization.route("/signin", methods = ['POST'])
def signin():
    url = AUTH_SERVICE_SIGNUP

    response = redirect(url, code=302)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['callback_url'] = AUTH_CALLBACK_URL

    return response

@authorization.route("/signin_callback", methods = ['GET'])
def signin_callback():

    access_token = request.headers.get('Access-Token')

    resp = make_response(render_template('index.html'))
    resp.set_cookie('Access-Token', access_token)

    return resp

def valid_token():
    pass
