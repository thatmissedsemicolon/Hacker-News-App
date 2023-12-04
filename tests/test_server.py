"""
Test the server is running and responding to requests
"""

import requests

def test_server():
    """Test the server make sure its online."""
    res = requests.head("https://pythonserver.tech", timeout=10)
    assert res.status_code == 200
