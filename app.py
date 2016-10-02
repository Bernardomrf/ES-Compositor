
from settings import *

from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

from views.transaction import transaction
from views.authorization import authorization
from views.dashboard import dashboard

# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='/static')


app.register_blueprint(transaction, url_prefix='/transaction')
app.register_blueprint(authorization, url_prefix='/authorize')
app.register_blueprint(dashboard)


if __name__ == '__main__':
    app.run(port=PORT, host=ALLOWED_HOSTS)
