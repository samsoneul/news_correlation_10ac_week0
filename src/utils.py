import pandas as pd
import string

def calculate_sentiment_stats(df):
    """
    Calculate aggregate statistics and top sentiments for positive, neutral, and negative sentiments.
    
    Args:
    - df (DataFrame): DataFrame containing 'source_name' and 'title_sentiment' columns.
    
    Returns:
    - DataFrame: Aggregate statistics for positive, neutral, and negative sentiments.
    - dict: Top sentiments for positive, neutral, and negative sentiments.
    """
    # Calculate sentiment counts
    sentiment_counts = df.groupby('source_name')['title_sentiment'].value_counts().unstack(fill_value=0)

    # Aggregate statistics
    agg_stats = sentiment_counts.aggregate(['mean', 'median', 'var'])

    # Top sentiments
    top_sentiments = {
        'positive': sentiment_counts["Positive"].sort_values(ascending=False).reset_index(name='Positive Count').head(10),
        'neutral': sentiment_counts["Neutral"].sort_values(ascending=False).reset_index(name='Neutral Count').head(10),
        'negative': sentiment_counts["Negative"].sort_values(ascending=False).reset_index(name='Negative Count').head(10)
    }

    return agg_stats, top_sentiments



def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Tokenize the text
    tokens = text.split()
    # Remove stopwords
    stop_words = set(["a", "an", "and", "the", "is", "in", "it", "of", "to", "with", "for"])
    tokens = [word for word in tokens if word not in stop_words]
    # Join tokens back into a string
    text = ' '.join(tokens)
    return text