"""Middleware functions for token and role validations."""

from functools import wraps
from flask import redirect, url_for, session
from database.models import User

def token_required(f):
    """Ensure that a valid token is present in the session."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_token = session.get('user')
        if user_token is None:
            return redirect(url_for('routes.signin'))
        return f(*args, **kwargs)
    return decorated_function

def token_not_required(f):
    """Redirect to home if a token is present in the session."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_token = session.get('user')
        if user_token:
            return redirect(url_for('routes.home'))
        return f(*args, **kwargs)
    return decorated_function

def verfiy_is_admin(f):
    """Ensure the logged-in user has an admin role."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_token = session.get('user')
        if user_token:
            user_info = session["user"].get("userinfo")
            user_id = user_info.get('sub')
            user = User.query.filter_by(user_id=user_id).first()
            if user.role != 'admin':
                return redirect(url_for('routes.home'))
            return f(*args, **kwargs, role=user.role)
        return redirect(url_for('routes.home'))
    return decorated_function
