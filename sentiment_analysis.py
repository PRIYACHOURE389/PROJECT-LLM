from textblob import TextBlob

def analyze_sentiment(text):
    try:
        blob = TextBlob(text)
        sentiment_polarity = blob.sentiment.polarity
        if sentiment_polarity > 0:
            return 'positive'
        elif sentiment_polarity < 0:
            return 'negative'
        else:
            return 'neutral'
    except Exception as e:
        print(f"Error analyzing sentiment: {e}")
        return 'unknown'
