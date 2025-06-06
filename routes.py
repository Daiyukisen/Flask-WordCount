from flask import Blueprint, request, jsonify
from models import db, SentimentAnalysis
from textblob import TextBlob

sentiment_bp = Blueprint('sentiment_bp', __name__)

# Create Sentiment Entry (API)
@sentiment_bp.route('/sentiment', methods=['POST'])
def create_sentiment():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "Invalid input, please enter text"}), 400

    new_entry = SentimentAnalysis(text=data['text'])
    db.session.add(new_entry)
    db.session.commit()

    return jsonify({"message": "Sentiment saved", "data": {"id": new_entry.id, "text": new_entry.text, "sentiment": new_entry.sentiment, "score": new_entry.score}}), 201

# Retrieve Sentiment History (API)
@sentiment_bp.route('/sentiment', methods=['GET'])
def get_sentiment_history():
    entries = SentimentAnalysis.query.all()
    history = [{"id": entry.id, "text": entry.text, "sentiment": entry.sentiment, "score": entry.score, "timestamp": entry.timestamp} for entry in entries]

    return jsonify({"message": "Sentiment history retrieved", "data": history}), 200

# Update Sentiment Entry (API)
@sentiment_bp.route('/sentiment/<int:id>', methods=['PUT'])
def update_sentiment(id):
    entry = SentimentAnalysis.query.get(id)
    if not entry:
        return jsonify({"error": "Entry not found"}), 404

    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "Invalid input"}), 400

    entry.text = data['text'].strip()
    entry.score = TextBlob(entry.text).sentiment.polarity
    entry.sentiment = "Positive" if entry.score > 0 else "Negative" if entry.score < 0 else "Neutral"

    db.session.commit()

    return jsonify({"message": "Sentiment entry updated", "data": {"id": entry.id, "text": entry.text, "sentiment": entry.sentiment, "score": entry.score}}), 200

# Delete Sentiment Entry (API)
@sentiment_bp.route('/sentiment/<int:id>', methods=['DELETE'])
def delete_sentiment(id):
    entry = SentimentAnalysis.query.get(id)
    if not entry:
        return jsonify({"error": "Entry not found"}), 404

    db.session.delete(entry)
    db.session.commit()

    return jsonify({"message": "Sentiment entry deleted"}), 200
