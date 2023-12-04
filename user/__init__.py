"""
This module initializes the user package.
"""

from os import environ as env
from flask import Flask
from dotenv import find_dotenv, load_dotenv
from database.models import db

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{env.get("SQL_DIR")}/test.db'

db.init_app(app)
