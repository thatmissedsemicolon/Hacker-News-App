"""
This module is responsible for running scheduled backups for the database.
"""

from user.user import app, Users

user = Users()

with app.app_context():
    user.backup_database()
