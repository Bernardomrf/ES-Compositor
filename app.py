
from settings import *

from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

from views.transaction import transaction
from views.authorization import authorization
from views.dashboard import dashboard
from views.payment import payment
from views.gateway import gateway
from views.money import money
from views.rating import rating
from views.profile import profile
from views.change_state import change_state
from views.add_transaction import add_transaction
from views.pay_gateway import pay_gateway

app = Flask(__name__, static_url_path='/static')


app.register_blueprint(transaction, url_prefix='/transaction')
app.register_blueprint(authorization, url_prefix='/authorize')
app.register_blueprint(payment, url_prefix='/payment')
app.register_blueprint(dashboard, url_prefix='/dashboard')
app.register_blueprint(money, url_prefix='/money')
app.register_blueprint(rating, url_prefix='/rating')
app.register_blueprint(change_state, url_prefix='/change_state')
app.register_blueprint(add_transaction, url_prefix='/add_transaction')
app.register_blueprint(profile, url_prefix='/profile')
app.register_blueprint(pay_gateway, url_prefix='/pay_gateway')
app.register_blueprint(gateway)


if __name__ == '__main__':
    app.run(port=PORT, host=ALLOWED_HOSTS)
