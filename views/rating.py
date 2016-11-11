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


@rating.route("/", methods=['GET'])
def home():
    token = request.cookies.get('Access-Token')

    if token == None:
        return redirect(LOGIN_PAGE_URL, code=302)

    # ---validate user---
    valid_user(token)

    # ---get user mail---
    headers = {"Access-Token": token, "API-Token": IAM_CLIENT_SECRET}
    response = requests.get(IAM_USER, headers=headers)

    if response.status_code != 200:
        return "Invalid Access Token", 400

    user = response.json()['data']['email']
    name = response.json()['data']['name']
    image = response.json()['data']['picture_url']

    return render_template('rating.html', user=user, name=name, image=image)


@rating.route("/review", methods=['GET'])
def review():
    token = request.cookies.get('Access-Token')

    if token == None:
        return redirect(LOGIN_PAGE_URL, code=302)

    # ---validate user---
    valid_user(token)

    # ---get user mail---
    headers = {"Access-Token": token, "API-Token": IAM_CLIENT_SECRET}
    response = requests.get(IAM_USER, headers=headers)

    if response.status_code != 200:
        return "Invalid Access Token", 400

    user = response.json()['data']['email']
    name = response.json()['data']['name']
    image = response.json()['data']['picture_url']

    return render_template('add_rating.html', user=user, name=name, image=image)


@rating.route("/user_rating/<email>/", methods=["GET"])
def user_rating(email):
    token = request.cookies.get('Access-Token')

    if token is None:
        return redirect(LOGIN_PAGE_URL, code=302)

    # ---validate user---
    valid_user(token)

    headers = {"API-Token": IAM_CLIENT_SECRET}
    response_iam = requests.get(IAM_USER + "?email=" + email, headers=headers)

    if response_iam.status_code != 200:
        return "Email not found", 400
    else:
        user_id = json.loads(response_iam.text)['data']['uid']
        response_iam_details = requests.get(IAM_USER + "?id=" + user_id, headers=headers)
        response = requests.get(RATING_RATE + user_id + "/")
        return jsonify({"user": json.loads(response_iam_details.text), "rating": json.loads(response.text)})


@rating.route("/rate", methods=['POST'])
def rate():
    trans_id = request.args.get('id')

    token = request.cookies.get('Access-Token')

    if token == None:
        return redirect(LOGIN_PAGE_URL, code=302)
        
    # ---validate user---
    valid_user(token)

    rate = request.form['rate']
    description = request.form['description']

    log.debug(rate)
    log.debug(description)





def valid_user(token):
    # ---validate user---
    headers = {"Access-Token": token, "API-Token": IAM_CLIENT_SECRET}
    response = requests.post(IAM_VALIDATE, headers=headers)

    if response.status_code != 200:
        return redirect(LOGIN_PAGE_URL, code=302)
