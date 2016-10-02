
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

@authorization.route("/login", methods = ['POST'])
def login():
    pass

@authorization.route("/login_callback", methods = ['GET'])
def login_callback():
    pass

@authorization.route("/signup", methods = ['POST'])
def signup():
    pass

@authorization.route("/signup_callback", methods = ['GET'])
def signup_callback():
    pass

@authorization.route("/addService", methods = ['POST'])
def add_service():
    pass
