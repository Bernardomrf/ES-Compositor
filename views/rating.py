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
        return redirect(LOGIN_PAGE_URL, code=302)

    user = response.json()['data']['email']
    name = response.json()['data']['name']
    image = response.json()['data']['picture_url']

    return render_template('rating.html', user=user, name=name, image=image)


@rating.route("/review", methods=['GET'])
def review():
    token = request.cookies.get('Access-Token')
    trans_id = request.args.get('id')

    if token == None:
        return redirect(LOGIN_PAGE_URL, code=302)

    # ---validate user---
    valid_user(token)

    # ---get user mail---
    headers = {"Access-Token": token, "API-Token": IAM_CLIENT_SECRET}
    response = requests.get(IAM_USER, headers=headers)

    if response.status_code != 200:
        return redirect(LOGIN_PAGE_URL, code=302)

    user = response.json()['data']['email']
    name = response.json()['data']['name']
    image = response.json()['data']['picture_url']

    return render_template('add_rating.html', user=user, name=name, image=image, trans_id=trans_id)


@rating.route("/user_rating/<email>/<size>/", methods=["GET"])
def user_rating(email, size):
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

        try:
            response = requests.get(RATING_RATE + user_id + "/?fields=rating,user_id_source,user_id_destination,message&size="+size,
                                    timeout=0.3)
            return jsonify({"user": json.loads(response_iam_details.text), "rating": json.loads(response.text)})
        except requests.exceptions.ConnectionError, requests.exceptions.Timeout:
            return jsonify({"user": json.loads(response_iam_details.text), "rating": "Rating service is down!"})


@rating.route("/rate", methods=['POST'])
def rate():
    trans_id = request.args.get('id')
    log.debug(trans_id)

    token = request.cookies.get('Access-Token')

    if token == None:
        return redirect(LOGIN_PAGE_URL, code=302)

    # ---validate user---
    valid_user(token)

    rate = request.form['rate']
    description = request.form['description']

    resp = requests.get(TRANSACTIONS_DETAILS.format(trans_id))
    if resp.status_code != 200:
        return "ID not found", 400

    info = resp.json()


    log.debug(info['to_uuid'])
    log.debug(info['from_uuid'])

    data = {'dest_id': info['to_uuid'],
            'source_id': info['from_uuid'],
            'transaction_id': trans_id,
            'rating': rate,
            'message': description}

    response = requests.post(RATING_RATE, data=data)

    if response.status_code != 200:
        return "Error rating", 400


    return redirect(DASHBOARD_URL, code=302)


def valid_user(token):
    # ---validate user---
    headers = {"Access-Token": token, "API-Token": IAM_CLIENT_SECRET}
    response = requests.post(IAM_VALIDATE, headers=headers)

    if response.status_code != 200:
        return redirect(LOGIN_PAGE_URL, code=302)
