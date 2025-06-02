from flask import Blueprint, request, jsonify
from textblob import TextBlob
from models import db, SentimentAnalysis

sentiment_bp = Blueprint('sentiment_bp', __name__)

# Create Sentiment Entry
@sentiment_bp.route('/sentiment', methods=['POST'])
def create_sentiment():
    data = request.json
    if not data or 'text' not in data:
        return jsonify({"error": "Invalid input"}), 400

    new_entry = SentimentAnalysis(text=data['text'])
    db.session.add(new_entry)
    db.session.commit()
    return jsonify({"message": "Sentiment analysis saved", "id": new_entry.id, "sentiment": new_entry.sentiment, "score": new_entry.score}), 201

# Retrieve Sentiment History
@sentiment_bp.route('/sentiment', methods=['GET'])
def get_sentiment_history():
    entries = SentimentAnalysis.query.all()
    history = [{"id": entry.id, "text": entry.text, "sentiment": entry.sentiment, "score": entry.score, "timestamp": entry.timestamp} for entry in entries]
    return jsonify(history), 200
