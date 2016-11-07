
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

    response = redirect(url+'?referer='+AUTH_CALLBACK_URL + "&api_token=" + IAM_CLIENT_SECRET, code=302)
    response.set_cookie('Access-Token', '', expires=0)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.referrer = AUTH_CALLBACK_URL
    response.headers['Referer'] = AUTH_CALLBACK_URL

    return response

@authorization.route("/signup_callback", methods = ['GET'])
def signup_callback():

    token = request.args.get('access_token')
    response = redirect('/dashboard', code=302)
    response.set_cookie('Access-Token',value=token)

    return response

@authorization.route("/logout", methods = ['GET'])
def logout():

    token = request.cookies.get('Access-Token')

    response = redirect(IAM_LOGOUT+ "?" +urllib.urlencode({"redirect_url": LOGIN_PAGE_URL,"access_token": token, "api_oken" : IAM_CLIENT_SECRET}), 302)

    return response
