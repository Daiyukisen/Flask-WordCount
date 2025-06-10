import unittest
import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models import SentimentAnalysis

class TestSentimentAnalysis(unittest.TestCase):

    def test_positive_sentences(self):
        positive_sentences = [
            "I love this product, it works wonderfully.",
            "The service was excellent and very helpful.",
            "This is a fantastic experience."
        ]
        for sentence in positive_sentences:
            sa = SentimentAnalysis(sentence)
            self.assertEqual(sa.sentiment, "Positive", f"Failed on sentence: {sentence}")

    def test_negative_sentences(self):
        negative_sentences = [
            "I hate this item, it broke immediately.",
            "The support was terrible and unresponsive.",
            "This is a disappointing outcome."
        ]
        for sentence in negative_sentences:
            sa = SentimentAnalysis(sentence)
            self.assertEqual(sa.sentiment, "Negative", f"Failed on sentence: {sentence}")

    def test_neutral_sentences(self):
        neutral_sentences = [
            "It is a product.",
            "The event took place yesterday.",
            "This is a book on the table."
        ]
        for sentence in neutral_sentences:
            sa = SentimentAnalysis(sentence)
            self.assertEqual(sa.sentiment, "Neutral", f"Failed on sentence: {sentence}")

if __name__ == '__main__':
    unittest.main()
