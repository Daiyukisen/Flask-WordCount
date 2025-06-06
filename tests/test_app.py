import unittest
from app import app, db
from models import SentimentAnalysis
import json

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.drop_all()

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'WordCount & Sentiment Analysis', response.data)

    def test_count_post_valid(self):
        response = self.client.post('/count', data={'fulltextarea': 'happy happy sad'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Total Word Count', response.data)
        self.assertIn(b'happy', response.data)

    def test_count_post_empty(self):
        response = self.client.post('/count', data={'fulltextarea': ''}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please enter text to analyze.', response.data)

    def test_sentiment_history(self):
        with app.app_context():
            entry = SentimentAnalysis(text='happy')
            db.session.add(entry)
            db.session.commit()
        response = self.client.get('/sentiments')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sentiment Analysis History', response.data)
        self.assertIn(b'happy', response.data)

    def test_update_sentiment_entry(self):
        with app.app_context():
            entry = SentimentAnalysis(text='happy')
            db.session.add(entry)
            db.session.commit()
            entry_id = entry.id
        response = self.client.post(f'/sentiments/update/{entry_id}', data={'text': 'sad'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sentiment entry updated successfully.', response.data)
        with app.app_context():
            updated_entry = SentimentAnalysis.query.get(entry_id)
            self.assertEqual(updated_entry.text, 'sad')

    def test_update_sentiment_entry_empty_text(self):
        with app.app_context():
            entry = SentimentAnalysis(text='happy')
            db.session.add(entry)
            db.session.commit()
            entry_id = entry.id
        response = self.client.post(f'/sentiments/update/{entry_id}', data={'text': ''}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Text cannot be empty.', response.data)

    def test_delete_sentiment_entry(self):
        with app.app_context():
            entry = SentimentAnalysis(text='happy')
            db.session.add(entry)
            db.session.commit()
            entry_id = entry.id
        response = self.client.post(f'/sentiments/delete/{entry_id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sentiment entry deleted successfully.', response.data)
        with app.app_context():
            deleted_entry = SentimentAnalysis.query.get(entry_id)
            self.assertIsNone(deleted_entry)

    def test_api_create_sentiment(self):
        response = self.client.post('/sentiment', json={'text': 'happy'})
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Sentiment saved')
        self.assertEqual(data['data']['text'], 'happy')

    def test_api_create_sentiment_invalid(self):
        response = self.client.post('/sentiment', json={})
        self.assertEqual(response.status_code, 400)

    def test_api_get_sentiment_history(self):
        with app.app_context():
            entry = SentimentAnalysis(text='happy')
            db.session.add(entry)
            db.session.commit()
        response = self.client.get('/sentiment')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Sentiment history retrieved')
        self.assertTrue(len(data['data']) > 0)

    def test_api_update_sentiment(self):
        with app.app_context():
            entry = SentimentAnalysis(text='happy')
            db.session.add(entry)
            db.session.commit()
            entry_id = entry.id
        response = self.client.put(f'/sentiment/{entry_id}', json={'text': 'sad'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['data']['text'], 'sad')

    def test_api_update_sentiment_invalid(self):
        # Create an entry first
        with app.app_context():
            entry = SentimentAnalysis(text='happy')
            db.session.add(entry)
            db.session.commit()
            entry_id = entry.id
        response = self.client.put(f'/sentiment/{entry_id}', json={})
        self.assertEqual(response.status_code, 400)

    def test_api_update_sentiment_not_found(self):
        response = self.client.put('/sentiment/9999', json={'text': 'sad'})
        self.assertEqual(response.status_code, 404)

    def test_api_delete_sentiment(self):
        with app.app_context():
            entry = SentimentAnalysis(text='happy')
            db.session.add(entry)
            db.session.commit()
            entry_id = entry.id
        response = self.client.delete(f'/sentiment/{entry_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Sentiment entry deleted')

    def test_api_delete_sentiment_not_found(self):
        response = self.client.delete('/sentiment/9999')
        self.assertEqual(response.status_code, 404)

    def test_sentiment_analysis_model(self):
        text = "I am happy"
        entry = SentimentAnalysis(text)
        self.assertEqual(entry.text, text)
        self.assertIn(entry.sentiment, ["Positive", "Negative", "Neutral"])
        self.assertIsInstance(entry.score, float)

if __name__ == '__main__':
    unittest.main()
