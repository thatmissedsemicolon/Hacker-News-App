"""
This module is responsible for running scheduled tasks to fetch latest news.
"""

from user.user import app, Users

user = Users()

with app.app_context():
    user.fetch_news()
