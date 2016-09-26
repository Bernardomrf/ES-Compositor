
from settings import *

from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

from views.github import github
from views.authorization import authorization

# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='/static')


app.register_blueprint(github, url_prefix='/github')
app.register_blueprint(authorization)

if __name__ == '__main__':
    app.run(port=PORT, host=ALLOWED_HOSTS)

