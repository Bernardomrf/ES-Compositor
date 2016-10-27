import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

ALLOWED_HOSTS="0.0.0.0"
PORT = 80

HOST = "localhost"

IAM_USER = "http://im.transafe.rafaelferreira.pt:80/user"
IAM_VALIDATE = "http://im.transafe.rafaelferreira.pt:80/validate"
IAM_SIGNUP = "http://im.transafe.rafaelferreira.pt:80/login"
IAM_LOGOUT = "http://im.transafe.rafaelferreira.pt:80/logout"

PAY_SERVICE_MYCARDS = "http://payments.transafe.rafaelferreira.pt:80/api/v1/cards/mycards/"
PAY_SERVICE_CREATE_CARD = "http://payments.transafe.rafaelferreira.pt:80/api/v1/cards/create/"

TRANSACTIONS_NEW = "http://10.0.11.12:80/api/v1/transaction/new/"
TRANSACTIONS_NEW_OBJECT = "http://10.0.11.12:80/api/v1/object/new/"
TRANSACTIONS_UPDATE = "http://10.0.11.12:80/api/v1/transaction/state/"
TRANSACTIONS_LIST = "http://10.0.11.12:80/api/v1/transaction/history/"
TRANSACTIONS_DETAILS = "http://10.0.11.12:80/api/v1/transaction/details/"

AUTH_CALLBACK_URL = "http://transafe.rafaelferreira.pt:80/authorize/signup_callback"
TRANSACTIONS_URL = "http://transafe.rafaelferreira.pt:80/transaction"
LOGIN_PAGE_URL = "http://transafe.rafaelferreira.pt:80/"
DASHBOARD_URL = "http://transafe.rafaelferreira.pt:80/dashboard"

NOTIFICATION_EMAIL = "http://10.0.11.14:80/api/v1/notification/messenger/"
