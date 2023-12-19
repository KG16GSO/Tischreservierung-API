import tempfile
import pytest
import json
from Reservation import init_reservation, query_db, init_db
 
@pytest.fixture
def client():
    app = init_reservation()
    # Set up a test client for the Flask application
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True
 
    with app.test_client() as client:
        with app.app_context():
            init_db(app)
        yield client
 
 
def test_get_tables(client):
    # Test /getTables endpoint with a valid 'time' parameter
    response = client.get('/getTables?time=2023-01-01--12:00:00')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
 
def test_get_reservations(client):
    # Test /getReservierungen endpoint
    response = client.get('/getReservierungen')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)



