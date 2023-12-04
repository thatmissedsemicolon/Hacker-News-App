"""
This module sets up and runs the Flask server.
"""

from os import environ as env
from flask import Flask, render_template, session
from flask_cors import CORS
from dotenv import find_dotenv, load_dotenv
from routes.routes import bp
from database.models import db, User
from user.user import Users

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{env.get("SQL_DIR")}/test.db'

db.init_app(app)

CORS(
    app,
    origins= [
        "https://www.mydomain.com", 
        "https://mydomain.com"
    ]
)

app.register_blueprint(bp)

users = Users()

@app.errorhandler(404)
def page_not_found(_):
    """
    Handles 404 page not found errors.
    """
    user_token = session.get('user')
    if user_token:
        user_info = session["user"].get("userinfo")
        user_id = user_info.get('sub')
        user = User.query.filter_by(user_id=user_id).first()
        return render_template('404.html', session=session.get("user"), user_role=user.role), 404
    return render_template('404.html'), 404


@app.route('/about')
def about():
    """
    Endpoint for the about page.
    """
    user_token = session.get('user')
    if user_token:
        user_info = session["user"].get("userinfo")
        user_id = user_info.get('sub')
        user = User.query.filter_by(user_id=user_id).first()
        return render_template('about.html', session=session.get("user"), user_role=user.role)
    return render_template('about.html', session=session.get("user"))


@app.context_processor
def context_processor():
    """
    Context processors for the templates.
    """
    return {
        "has_user_liked_post": users.has_user_liked_post, 
        "has_user_disliked_post": users.has_user_disliked_post
    }


if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=8000)
