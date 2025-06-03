import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    yield client

# Test Word Count Route
def test_word_count(client):
    response = client.post('/count', data={'fulltextarea': "Hello world Hello"})
    assert response.status_code == 200
    assert b'3 words' in response.data  # Checks total word count
    assert b'Hello' in response.data    # Checks word frequency
    assert b'world' in response.data    # Checks another word presence

# Test Sentiment Analysis Route (Positive Sentiment)
def test_sentiment_positive(client):
    response = client.post('/count', data={'fulltextarea': "I love this product!"})
    assert response.status_code == 200
    assert b'Positive' in response.data  # Validates sentiment detection

# Test Sentiment Analysis Route (Negative Sentiment)
def test_sentiment_negative(client):
    response = client.post('/count', data={'fulltextarea': "I hate this service!"})
    assert response.status_code == 200
    assert b'Negative' in response.data  # Validates sentiment detection

# Test Sentiment Analysis Route (Neutral Sentiment)
def test_sentiment_neutral(client):
    response = client.post('/count', data={'fulltextarea': "The product is good, but the price is a little high."})
    assert response.status_code == 200
    assert b'Neutral' in response.data  # Validates mixed/neutral response
