"""
This module provides authentication functionality using Auth0.
"""

from urllib.parse import quote_plus, urlencode
from flask import redirect, url_for, request, session
from . import oauth, env, user


class Auth:
    """Handles authentication-related tasks for the application."""

    def __init__(self):
        """Initializes the Auth class."""

    def callback(self):
        """Handles the callback after the user has been authenticated."""
        token = oauth.auth0.authorize_access_token()
        session["user"] = token
        user_info = session["user"].get("userinfo")
        user.add_user_if_not_exists(user_info)
        return redirect("/")

    def authorize_user(self):
        """Initiates the user authorization process."""
        screen_hint = request.args.get('screen_hint', 'login')
        return oauth.auth0.authorize_redirect(
            redirect_uri=url_for("routes.callback", _external=True),
            screen_hint=screen_hint
        )

    def logout(self):
        """Logs out the user and clears the session."""
        session.clear()
        return redirect(
            "https://"
            + env.get("AUTH0_DOMAIN")
            + "/v2/logout?"
            + urlencode(
                {
                    "returnTo": url_for("routes.home", _external=True),
                    "client_id": env.get("AUTH0_CLIENT_ID"),
                },
                quote_via=quote_plus,
            )
        )
