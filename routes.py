from flask import Blueprint, request, jsonify, render_template
from models import db, SentimentAnalysis

sentiment_bp = Blueprint('sentiment_bp', __name__)

# Sentiment Analysis Page
@sentiment_bp.route('/sentiment-page')
def sentiment_page():
    return render_template('sentiment.html')

# Create Sentiment Entry
@sentiment_bp.route('/sentiment', methods=['POST'])
def create_sentiment():
    data = request.json
    if not data or 'text' not in data:
        return jsonify({"error": "Invalid input"}), 400

    new_entry = SentimentAnalysis(text=data['text'])
    db.session.add(new_entry)
    db.session.commit()
    return jsonify({"message": "Sentiment saved", "id": new_entry.id, "sentiment": new_entry.sentiment, "score": new_entry.score}), 201

# Retrieve Sentiment History
@sentiment_bp.route('/sentiment', methods=['GET'])
def get_sentiment_history():
    if not db.engine.table_names():  
        return jsonify({"error": "Database table missing! Run db.create_all() first."}), 500

    entries = SentimentAnalysis.query.all()
    history = [{"id": entry.id, "text": entry.text, "sentiment": entry.sentiment, "score": entry.score, "timestamp": entry.timestamp} for entry in entries]
    return jsonify(history), 200
