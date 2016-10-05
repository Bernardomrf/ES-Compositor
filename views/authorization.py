
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
@authorization.route("/signup", methods = ['GET'])
def signup():
    url = AUTH_SERVICE_SIGNUP

    response = redirect(url, code=302)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['referer'] = AUTH_CALLBACK_URL

    return response

@authorization.route("/login", methods = ['GET'])
def signup():
    url = AUTH_SERVICE_LOGIN

    response = redirect(url, code=302)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['referer'] = AUTH_CALLBACK_URL

    return response

@authorization.route("/signin_callback", methods = ['GET'])
def signin_callback():

    access_token = request.headers.get('access-token')

    resp = make_response(render_template('index.html'))
    resp.set_cookie('access-token', access_token)

    return resp

def valid_token():
    pass
