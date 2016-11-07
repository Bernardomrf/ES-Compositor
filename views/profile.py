
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

profile = Blueprint('profile', __name__)
logging.basicConfig(stream=sys.stderr)
logging.getLogger().setLevel(logging.DEBUG)
log = logging.getLogger()

@profile.route("/", methods = ['GET'])
def home():

    token = request.cookies.get('Access-Token')

    if token == None:
        return redirect(LOGIN_PAGE_URL, code=302)

    # ---validate user---
    valid_user(token)

    # ---get user info---
    headers = {"Access-Token": token, "API-Token" : IAM_CLIENT_SECRET}
    response = requests.get(IAM_USER, headers=headers)

    if response.status_code != 200:
        return "Invalid Access Token", 400


    email = response.json()['data']['email']
    uid = response.json()['data']['uid']
    name = response.json()['data']['name']
    image = response.json()['data']['picture_url']
    address = response.json()['data']['address']
    phone = response.json()['data']['phone']



    return render_template('profile.html', name=name, email=email, id=uid, image=image, address=address)

@profile.route("/editAddress", methods = ['POST'])
def editAddress():

    token = request.cookies.get('Access-Token')

    if token == None:
        return redirect(LOGIN_PAGE_URL, code=302)

    address = request.form["address"]

    # ---validate user---
    valid_user(token)

    # ---add user info---

    headers = {"Access-Token": token}
    data = {"address": address}
    response = requests.post(IAM_USER_DATA, data=data, headers=headers)

    if response.status_code != 200:
        return "Invalid Access Token", 400

    return redirect("/profile", code=302, Response=None)

@profile.route("/editPhone", methods = ['POST'])
def editPhone():

    token = request.cookies.get('Access-Token')

    if token == None:
        return redirect(LOGIN_PAGE_URL, code=302)

    phone = request.form["phone"]

    # ---validate user---
    valid_user(token)

    # ---add user info---

    headers = {"Access-Token": token}
    data = {"phone": phone}
    response = requests.post(IAM_USER_DATA, data=data, headers=headers)

    if response.status_code != 200:
        return "Invalid Access Token", 400

    return redirect("/profile", code=302, Response=None)

def valid_user(token):

    # ---validate user---
    headers = {"Access-Token": token, "API-Token" : IAM_CLIENT_SECRET}
    response = requests.post(IAM_VALIDATE, headers=headers)

    if response.status_code != 200:
        return redirect(LOGIN_PAGE_URL, code=302)
