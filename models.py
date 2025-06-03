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

    def update_sentiment(self, new_text):
        """ Updates sentiment based on new text input """
        self.text = new_text.strip()
        self.score = TextBlob(new_text).sentiment.polarity
        self.sentiment = (
            "Positive" if self.score > 0.2 
            else "Negative" if self.score < -0.2 
            else "Neutral"
        )
        self.timestamp = datetime.utcnow()
