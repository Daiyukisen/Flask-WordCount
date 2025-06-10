# Flask-WordCount

This project is a WORD COUNT APP built using Flask, a micro-framework for Python. It provides word count and sentiment analysis features with a complete CRUD (Create, Read, Update, Delete) functionality for sentiment entries.

## Features

- Word count and sentiment analysis of input text.
- Sentiment classification into Positive, Negative, or Neutral.
- Save sentiment analysis results to a database.
- View sentiment history with timestamps.
- Update and delete sentiment entries via the web UI.
- RESTful API endpoints for sentiment management (create, retrieve, update, delete).
- Unit tests for sentiment analysis classification.

## Installation

To use this project, your computer needs:

- Python 3.7.1 or higher
- Flask 1.0.2 or higher

You can install Flask and other dependencies using pip:

```bash
pip install flask flask_sqlalchemy textblob
```

## Running the App

Run the Flask application with:

```bash
python app.py
```

The app will be available at `http://127.0.0.1:5000/`.

## Usage

- Navigate to the home page.
- Enter text in the textarea and submit to get word count and sentiment analysis.
- View sentiment history by clicking the "View Sentiment History" button.
- Update or delete sentiment entries from the history page.

## API Endpoints

- `POST /sentiment` - Create a new sentiment entry.
- `GET /sentiment` - Retrieve all sentiment entries.
- `PUT /sentiment/<id>` - Update a sentiment entry by ID.
- `DELETE /sentiment/<id>` - Delete a sentiment entry by ID.

## Testing

Unit tests for sentiment analysis classification are located in `tests/test_sentiment_analysis.py`.

Run the tests with:

```bash
python -m unittest discover tests
```

All tests should pass, verifying the sentiment classification logic for positive, negative, and neutral sentences.

## Notes

- The sentiment analysis uses TextBlob for polarity scoring.
- Sentiment thresholds are set to classify polarity > 0.2 as Positive, < -0.2 as Negative, and in between as Neutral.
- Adjust thresholds in `models.py` if needed to better fit your use case.
