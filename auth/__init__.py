"""
Initialization module for authentication.
Handles configuration related to Auth0 and initializes the OAuth object.
"""

from os import environ as env
from flask import Flask
from dotenv import find_dotenv, load_dotenv
from authlib.integrations.flask_client import OAuth
from user.user import Users

app = Flask(__name__)

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration',
)

user = Users()
