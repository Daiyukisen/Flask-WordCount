import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    yield client

# Test Home Page Loads Successfully
def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"WordCount App" in response.data

# Test Word Count Page Loads on Submission
def test_word_count_submission(client):
    response = client.post('/count', data={"fulltextarea": "Hello world Hello"})
    assert response.status_code == 200
    assert b"Total Word Count:" in response.data
    assert b"Hello" in response.data
