import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

ALLOWED_HOSTS="0.0.0.0"
PORT = 80

HOST = "localhost"

IAM_USER = "https://im.transafe.rafaelferreira.pt/user"
IAM_VALIDATE = "https://im.transafe.rafaelferreira.pt/validate"
IAM_SIGNUP = "https://im.transafe.rafaelferreira.pt/login"
IAM_LOGOUT = "https://im.transafe.rafaelferreira.pt/logout"

PAY_SERVICE_TOKEN_ID = ""
PAY_SERVICE_MYCARDS = "https://payments.transafe.rafaelferreira.pt/api/v1/cards/mycards/"
PAY_SERVICE_CREATE_CARD = "https://payments.transafe.rafaelferreira.pt/api/v1/cards/create/"
PAY_SERVICE_CREATE_PAYMENT = "https://payments.transafe.rafaelferreira.pt/api/v1/payments/create/"
PAY_SERVICE_COMPLETE_PAYMENT = "https://payments.transafe.rafaelferreira.pt/api/v1/payments/complete/"

TRANSACTIONS_NEW = "http://10.0.11.12/api/v1/transaction/new/"
TRANSACTIONS_NEW_OBJECT = "http://10.0.11.12/api/v1/object/new/"
TRANSACTIONS_UPDATE = "http://10.0.11.12/api/v1/transaction/state/"
TRANSACTIONS_LIST = "http://10.0.11.12/api/v1/transaction/history/"
TRANSACTIONS_DETAILS = "http://10.0.11.12/api/v1/transaction/details/"
TRANSACTIONS_TRACKING = "http://10.0.11.12:80/api/v1/transaction/tracking_code/"

AUTH_CALLBACK_URL = "https://transafe.rafaelferreira.pt/authorize/signup_callback"
TRANSACTIONS_URL = "https://transafe.rafaelferreira.pt/transaction"
LOGIN_PAGE_URL = "https://transafe.rafaelferreira.pt/"
DASHBOARD_URL = "https://transafe.rafaelferreira.pt/dashboard"
PAY_GATEWAY_URL = "https://transafe.rafaelferreira.pt/pay_gateway"
PAY_GATEWAY_CALLBACK_URL = "https://transafe.rafaelferreira.pt/pay_gateway/callback"
CHANGE_STATE_URL = "https://transafe.rafaelferreira.pt/pay_gateway/change_state"
PAY_GATEWAY_CONFIRMED_URL = "https://transafe.rafaelferreira.pt/pay_gateway/payment_success"

NOTIFICATION_EMAIL = "http://10.0.11.14/api/v1/notification/email/"
NOTIFICATION_MESSENGER = "http://10.0.11.14/api/v1/notification/messenger/"

PAYPAL_CLIENT_ID = "AW3iw3rOWtZt_VrhggnaNYl1_7FJ6lAf04SwAXAFfHmVUAkXX6bz55pSBnemeJ3z-Vytymv1FP7mVWBt"
PAYPAL_CLIENT_SECRET = "ENqKPCSabqwaDsLKncTGjeXDLlYyIEALMg9yiRdZG8BS7TvqLPINd303YhMvmLCJptEeRRHhUSS0JM6T"
