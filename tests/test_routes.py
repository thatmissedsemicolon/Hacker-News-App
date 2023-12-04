# pylint: disable=redefined-outer-name

"""Module for testing routes in the app."""

import pytest
from app import app

@pytest.fixture
def test_client():
    """Provide test client for Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_basic_routes(test_client):
    """Test basic routes to ensure they are accessible."""
    routes = ["/", "/signin", "/signup", "/newsfeed", "/about"]
    for route in routes:
        res = test_client.get(route)
        assert res.status_code == 200

def test_other_routes(test_client):
    """Test other miscellaneous routes."""
    res = test_client.get("/profile")
    assert res.status_code == 302

    res = test_client.get("/updateUser")
    assert res.status_code == 405

def test_auth(test_client):
    """Test authentication related routes."""
    res = test_client.get("/authorize")
    assert res.status_code == 302

    res = test_client.get("/logout")
    assert res.status_code == 302

    res = test_client.get("/callback")
    assert res.status_code == 400

def test_likes_token_required(test_client):
    """Test like routes that require token."""
    routes = ["/like/1", "/dislike/1"]
    for route in routes:
        res = test_client.get(route)
        assert res.status_code == 405

def test_admin_routes_get_token_required(test_client):
    """Test admin routes accessed via GET that require token."""
    routes = ["/admin/newsitems", "/admin/edit-post/1", "/admin/backups"]
    for route in routes:
        res = test_client.get(route)
        assert res.status_code == 302

def test_admin_routes_post_token_required(test_client):
    """Test admin routes accessed via POST that require token."""
    routes = ["/admin/delete-post/1", "/admin/view-reactions-users/1", "/admin/create_backup"]
    for route in routes:
        res = test_client.get(route)
        assert res.status_code == 405
