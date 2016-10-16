import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

ALLOWED_HOSTS="0.0.0.0"
PORT = 5001

HOST = "localhost"
REDIS_PORT=6379

IAM_USER = "http://bsilvr.duckdns.org:5368/user"
IAM_VALIDATE = "http://bsilvr.duckdns.org:5368/validate"
IAM_SIGNUP = "http://bsilvr.duckdns.org:5368/login"
IAM_LOGOUT = "http://bsilvr.duckdns.org:5368/logout"

PAY_SERVICE_INTERFACE = "http://.../payments_interface"#/payments_interface

TRANSACTIONS_NEW = "http://192.168.33.11:8000/api/v1/transaction/new/"
TRANSACTIONS_NEW_OBJECT = "http://192.168.33.11:8000/api/v1/object/new/"
TRANSACTIONS_UPDATE = "http://192.168.33.11:8000/api/v1/transaction/state/"
TRANSACTIONS_LIST = "http://192.168.33.11:8000/api/v1/transaction/history/"
TRANSACTIONS_DETAILS = "http://192.168.33.11:8000/api/v1/transaction/details/"

AUTH_CALLBACK_URL = "http://localhost:5001/authorize/signup_callback"
TRANSACTIONS_URL = "http://localhost:5001/transaction"
