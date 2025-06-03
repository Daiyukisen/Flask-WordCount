from flask import Flask, render_template, request
from models import db
import operator
from textblob import TextBlob  # Import for sentiment analysis

app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sentiment.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Database
db.init_app(app)

# Ensure tables exist before processing routes
with app.app_context():
    db.create_all()

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

        # Word count logic
        word_list = data.split()
        list_length = len(word_list)

        word_disc = {word: word_list.count(word) for word in set(word_list)}
        sorted_word_list = sorted(word_disc.items(), key=lambda x: x[1], reverse=True)

        # Sentiment analysis logic
        sentiment_score = TextBlob(data).sentiment.polarity
        if sentiment_score > 0.1:
            sentiment_text = "Positive"
        elif sentiment_score < -0.1:
            sentiment_text = "Negative"
        else:
            sentiment_text = "Neutral"

        return render_template(
            'count.html', 
            fulltext=data, 
            words=list_length, 
            worddisc=sorted_word_list, 
            sentiment=sentiment_text, 
            score=sentiment_score
        )

    return render_template('home.html')

if __name__ == "__main__":
    app.secret_key = 'it6finals'
    app.run(debug=True)
