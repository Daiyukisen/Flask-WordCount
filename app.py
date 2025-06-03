from flask import Flask, render_template
from models import db
from routes import sentiment_bp  # Import API routes

app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sentiment.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Database
db.init_app(app)

# Ensure tables exist before processing routes
with app.app_context():
    db.create_all()

# Register API Routes
app.register_blueprint(sentiment_bp, url_prefix="/api")

# Home Route
@app.route('/')
def home():
    return render_template('home.html')

if __name__ == "__main__":
    app.secret_key = 'it6finals'
    app.run(debug=True)
