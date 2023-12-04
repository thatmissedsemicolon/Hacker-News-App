"""
Registers the blueprint from routes module to the app.
"""

from flask import Flask
from routes.routes import bp  # Relative import to get the bp from routes module.

app = Flask(__name__)

app.register_blueprint(bp)
