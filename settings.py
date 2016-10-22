import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

ALLOWED_HOSTS="0.0.0.0"
PORT = 80

HOST = "localhost"

IAM_USER = "http://bsilvr.duckdns.org:5368/user"
IAM_VALIDATE = "http://bsilvr.duckdns.org:5368/validate"
IAM_SIGNUP = "http://bsilvr.duckdns.org:5368/login"
IAM_LOGOUT = "http://bsilvr.duckdns.org:5368/logout"

PAY_SERVICE_INTERFACE = "http://.../payments_interface"#/payments_interface

TRANSACTIONS_NEW = "http://10.0.11.12:80/api/v1/transaction/new/"
TRANSACTIONS_NEW_OBJECT = "http://10.0.11.12:80/api/v1/object/new/"
TRANSACTIONS_UPDATE = "http://10.0.11.12:80/api/v1/transaction/state/"
TRANSACTIONS_LIST = "http://10.0.11.12:80/api/v1/transaction/history/"
TRANSACTIONS_DETAILS = "http://10.0.11.12:80/api/v1/transaction/details/"

AUTH_CALLBACK_URL = "http://bsilvr.duckdns.org:80/authorize/signup_callback"
TRANSACTIONS_URL = "http://bsilvr.duckdns.org:80/transaction"
