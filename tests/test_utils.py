import unittest
import pandas as pd
from src.utils import calculate_sentiment_stats  # Adjusted import statement

class TestUtils(unittest.TestCase):

    def setUp(self):
        # Sample data for testing
        data = {
            'source_name': ['website1', 'website2', 'website1', 'website2', 'website3'],
            'title_sentiment': ['Positive', 'Negative', 'Positive', 'Neutral', 'Negative']
        }
        self.df = pd.DataFrame(data)

    def test_calculate_sentiment_counts(self):
        # Call the function with the sample data
        _, top_sentiments = calculate_sentiment_stats(self.df)

        # Expected top sentiments
        expected_top_sentiments = {
            'positive': {
                'source_name': ['website1', 'website2'],
                'Positive Count': [2, 0]
            },
            'neutral': {
                'source_name': ['website2', 'website1', 'website3'],
                'Neutral Count': [1, 1, 0]
            },
            'negative': {
                'source_name': ['website1', 'website3', 'website2'],
                'Negative Count': [1, 1, 1]
            }
        }

        # Check if the calculated top sentiments match the expected values
        self.assertEqual(top_sentiments['positive'].to_dict(), expected_top_sentiments['positive'])
        self.assertEqual(top_sentiments['neutral'].to_dict(), expected_top_sentiments['neutral'])
        self.assertEqual(top_sentiments['negative'].to_dict(), expected_top_sentiments['negative'])


if __name__ == '__main__':
    unittest.main()
