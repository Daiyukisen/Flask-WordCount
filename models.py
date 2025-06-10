from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from textblob import TextBlob

db = SQLAlchemy()

class SentimentAnalysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    sentiment = db.Column(db.String(20), nullable=False)
    score = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, text):
        super().__init__()
        self.text = text.strip() if text else ""
        self.calculate_sentiment()

    def calculate_sentiment(self):
        self.score = TextBlob(self.text).sentiment.polarity if self.text else 0
        self.sentiment = "Positive" if self.score > 0.2 else "Negative" if self.score < -0.2 else "Neutral"
