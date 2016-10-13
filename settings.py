import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

ALLOWED_HOSTS="0.0.0.0"
PORT = 5001

HOST = "localhost"
REDIS_PORT=6379

IAM_USER = "http://.../user"
IAM_VALIDATE = "http://.../validate"
IAM_SIGNUP = "http://.../login"
IAM_LOGOUT = "http://.../logout"

PAY_SERVICE_INTERFACE = "http://.../payments_interface"#/payments_interface

TRANSACTIONS_NEW = "http://.../api/v1/transaction/new/"
TRANSACTIONS_NEW_OBJECT = "http://.../api/v1/object/new/"
TRANSACTIONS_UPDATE = "http://.../api/v1/transaction/state/"
TRANSACTIONS_LIST = "http://.../api/v1/transaction/history/"
TRANSACTIONS_DETAILS = "http://.../api/v1/transaction/details/"

AUTH_CALLBACK_URL = "http://localhost:5001/authorize/signup_callback"
TRANSACTIONS_URL = "http://localhost:5001/transaction"
