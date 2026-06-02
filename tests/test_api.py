import pytest 
import sys
import os

sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
)

from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
        
        
def test_get_all_sentiments(client):
     response = client.get('/sentiment')
     assert response.status_code == 200

def test_create_sentiment(client):
    response = client.post('/sentiment',
    json={"text":"I love programmimng"}
    )
    assert response.status_code == 201
def test_invalid_create(client):
    response = client.post('/sentiment',json={} )
    assert response.status_code == 400

def test_get_invalid_sentiment(client):
    response = client.get('/sentiment/999')
    assert response.status_code == 404
def test_delete_invalid_sentiment(client):
    response = client.delete('/sentiment/9999')
    assert response.status_code == 404