from flask import Flask, render_template, request
from routes import sentiment_bp
from models import db
import operator

app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sentiment.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Database
db.init_app(app)

# Ensure tables exist
with app.app_context():
    db.create_all()

# Register API Routes
app.register_blueprint(sentiment_bp)

# Home Route
@app.route('/')
def home():
    return render_template('home.html')

# Word Count Feature
@app.route('/count', methods=['GET', 'POST'])
def count():
    if request.method == 'POST':
        data = request.form.get('fulltextarea', '').strip()
        if not data:
            return render_template('home.html', error="Please enter text to analyze.")

        word_list = data.split()
        list_length = len(word_list)

        word_disc = {}
        for word in word_list:
            word_disc[word] = word_disc.get(word, 0) + 1

        sort_list = sorted(word_disc.items(), key=lambda x: x[1], reverse=True)
        return render_template('count.html', fulltext=data, words=list_length, worddisc=sort_list)

    return render_template('home.html')

if __name__ == "__main__":
    app.secret_key = 'your_secret_key_here'
    app.run(debug=True)
