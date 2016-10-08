
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

gateway = Blueprint('gateway', __name__)
logging.basicConfig(stream=sys.stderr)
logging.getLogger().setLevel(logging.DEBUG)
log = logging.getLogger()

@dashboard.route("/", methods = ['GET'])
def home():
    return render_template('login_page.html')
