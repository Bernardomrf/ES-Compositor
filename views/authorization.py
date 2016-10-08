
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

@authorization.route("/signup", methods = ['GET'])
def signup():
    url = IAM_SIGNUP

    response = redirect(url, code=302)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Referer'] = AUTH_CALLBACK_URL

    return response

@authorization.route("/signup_callback", methods = ['GET'])
def signup_callback():

    token = request.headers.get('Access-Token')

    resp = make_response(render_template('index.html'))
    resp.set_cookie('Access-Token', token)

    return resp

@authorization.route("/logout", methods = ['GET'])
def logout():
    url = IAM_LOGOUT
    token = request.cookies.get('Access-Token')

    response.set_cookie('Access-Token', '', expires=0)

    headers = {"Access-Token": token}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return "Invalid Access Token", 400

    return render_template('login.html')
