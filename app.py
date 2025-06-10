from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, SentimentAnalysis
from collections import Counter
from textblob import TextBlob
from routes import sentiment_bp

app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sentiment.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'it6finals'

# Initialize Database
db.init_app(app)
with app.app_context():
    db.create_all()

# Register Blueprint for API routes
app.register_blueprint(sentiment_bp)

# Home Route
@app.route('/')
def home():
    return render_template('home.html')

# Word Count & Sentiment Analysis
@app.route('/count', methods=['GET', 'POST'])
def count():
    if request.method == 'POST':
        data = request.form.get('fulltextarea', '').strip()
        if not data:
            return render_template('home.html', error="Please enter text to analyze.")

        # Word count logic using Counter for performance
        word_list = data.split()
        list_length = len(word_list)
        word_disc = Counter(word_list)
        sorted_word_list = sorted(word_disc.items(), key=lambda x: (-x[1], x[0]))

        # Create new entry and calculate sentiment using model method
        try:
            new_entry = SentimentAnalysis(text=data)
        except Exception as e:
            return render_template('home.html', error=f"Error processing sentiment: {str(e)}")

        # Sentiment breakdown counts and scores
        positive_words = [word for word in word_list if TextBlob(word).sentiment.polarity > 0]
        negative_words = [word for word in word_list if TextBlob(word).sentiment.polarity < 0]
        neutral_words = [word for word in word_list if TextBlob(word).sentiment.polarity == 0]

        positive_count = len(positive_words)
        negative_count = len(negative_words)
        neutral_count = len(neutral_words)

        positive_score = sum(TextBlob(word).sentiment.polarity for word in positive_words)
        negative_score = sum(TextBlob(word).sentiment.polarity for word in negative_words)
        neutral_score = sum(TextBlob(word).sentiment.polarity for word in neutral_words)

        # Save sentiment analysis result to database
        db.session.add(new_entry)
        db.session.commit()

        return render_template('count.html', fulltext=data, words=list_length, worddisc=sorted_word_list, sentiment=new_entry.sentiment, score=new_entry.score,
                               positive_count=positive_count, negative_count=negative_count, neutral_count=neutral_count,
                               positive_score=positive_score, negative_score=negative_score, neutral_score=neutral_score)

    return render_template('home.html')

# Sentiment History Page
@app.route('/sentiments')
def sentiment_history():
    entries = SentimentAnalysis.query.order_by(SentimentAnalysis.timestamp.desc()).all()
    return render_template('sentiment_history.html', entries=entries)

# Update Sentiment Entry
@app.route('/sentiments/update/<int:id>', methods=['POST'])
def update_sentiment_entry(id):
    entry = SentimentAnalysis.query.get_or_404(id)
    new_text = request.form.get('text', '').strip()
    if not new_text:
        flash('Text cannot be empty.', 'danger')
        return redirect(url_for('sentiment_history'))

    entry.text = new_text
    entry.score = TextBlob(new_text).sentiment.polarity
    entry.sentiment = "Positive" if entry.score > 0 else "Negative" if entry.score < 0 else "Neutral"
    db.session.commit()
    flash('Sentiment entry updated successfully.', 'success')
    return redirect(url_for('sentiment_history'))

# Delete Sentiment Entry
@app.route('/sentiments/delete/<int:id>', methods=['POST'])
def delete_sentiment_entry(id):
    entry = SentimentAnalysis.query.get_or_404(id)
    db.session.delete(entry)
    db.session.commit()
    flash('Sentiment entry deleted successfully.', 'success')
    return redirect(url_for('sentiment_history'))

if __name__ == "__main__":
    app.run(debug=True)
