"""
This module initializes the Flask application and configures the SQLAlchemy database.
"""

from os import environ as env
from flask import Flask
from dotenv import find_dotenv, load_dotenv
from flask_sqlalchemy import SQLAlchemy

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{env.get("SQL_DIR")}/test.db'
db = SQLAlchemy(app)
