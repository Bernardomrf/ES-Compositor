import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

ALLOWED_HOSTS="0.0.0.0"
PORT = 5001

HOST = "localhost"
REDIS_PORT=6379

AUTH_CALLBACK_URL = "http://localhost:5001/signin_callback"
TRANSACTIONS_URL = "http://localhost:5001/transaction"

LOGIN_CALLBACK = "http://localhost:5001/login_callback"
SIGNUP_CALLBACK = "http://localhost:5001/signup_callback"
