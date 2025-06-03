from flask import Blueprint, request, jsonify
from models import db, SentimentAnalysis

sentiment_bp = Blueprint('sentiment_bp', __name__)

# Create Sentiment Entry (POST)
@sentiment_bp.route('/sentiment', methods=['POST'])
def create_sentiment():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "Invalid input, please enter text"}), 400

    new_entry = SentimentAnalysis(text=data['text'])
    db.session.add(new_entry)
    db.session.commit()

    return jsonify({
        "message": "Sentiment saved",
        "sentiment": new_entry.sentiment,
        "score": new_entry.score,
        "id": new_entry.id
    }), 201

# Retrieve Sentiment History (GET)
@sentiment_bp.route('/sentiment', methods=['GET'])
def get_sentiment_history():
    entries = SentimentAnalysis.query.all()
    history = [
        {"id": entry.id, "text": entry.text, "sentiment": entry.sentiment, "score": entry.score, "timestamp": entry.timestamp}
        for entry in entries
    ]
    return jsonify({"message": "Sentiment history retrieved", "data": history}), 200

# Update Sentiment Entry (PUT)
@sentiment_bp.route('/sentiment/<int:id>', methods=['PUT'])
def update_sentiment(id):
    entry = SentimentAnalysis.query.get(id)
    if not entry:
        return jsonify({"error": "Entry not found"}), 404

    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "Invalid input, please enter text"}), 400

    entry.update_sentiment(data['text'])
    db.session.commit()

    return jsonify({
        "message": "Sentiment updated",
        "sentiment": entry.sentiment,
        "score": entry.score
    }), 200

# Delete Sentiment Entry (DELETE)
@sentiment_bp.route('/sentiment/<int:id>', methods=['DELETE'])
def delete_sentiment(id):
    entry = SentimentAnalysis.query.get(id)
    if not entry:
        return jsonify({"error": "Entry not found"}), 404

    db.session.delete(entry)
    db.session.commit()

    return jsonify({"message": "Sentiment deleted"}), 200
