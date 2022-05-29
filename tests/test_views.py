# test_views.py
"""
tests
"""

def test_index_ok(client):
    """
    Test to ensure HTTP "OK"
    """
    # Make a GET request to / and store the response object
    # using the Django test client.
    response = client.get('/')
    # Assert that the status_code is 200 (OK)
    assert response.status_code == 200
