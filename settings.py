import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

ALLOWED_HOSTS="0.0.0.0"
PORT = 5001

HOST = "192.168.99.100"
REDIS_PORT=6379

LOGIN_CALLBACK = "http://192.168.99.100:5001/login_callback"
SIGNUP_CALLBACK = "http://192.168.99.100:5001/signup_callback"
