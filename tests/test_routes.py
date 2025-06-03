import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    yield client

# Test Creating a Sentiment Entry (POST)
def test_post_sentiment(client):
    response = client.post('/api/sentiment', json={"text": "Fantastic product!"})
    assert response.status_code == 201
    assert b"Positive" in response.data

# Test Retrieving Sentiment History (GET)
def test_get_sentiment_history(client):
    response = client.get('/api/sentiment')
    assert response.status_code == 200

# Test Updating Sentiment Entry (PUT)
def test_update_sentiment(client):
    response = client.put('/api/sentiment/1', json={"text": "Terrible service!"})
    assert response.status_code == 200
    assert b"Negative" in response.data

# Test Deleting Sentiment Entry (DELETE)
def test_delete_sentiment(client):
    response = client.delete('/api/sentiment/1')
    assert response.status_code == 200
    assert b"Sentiment deleted" in response.data

# Test Invalid Request (PUT on Non-Existent ID)
def test_update_nonexistent_sentiment(client):
    response = client.put('/api/sentiment/999', json={"text": "Bad experience!"})
    assert response.status_code == 404

# Test Invalid Request (DELETE on Non-Existent ID)
def test_delete_nonexistent_sentiment(client):
    response = client.delete('/api/sentiment/999')
    assert response.status_code == 404
