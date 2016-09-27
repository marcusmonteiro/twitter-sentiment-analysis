import os.path
from config import TWITTER_STREAMING_DATA_FILE
from twitter_data import write_streaming_data
from twitter_sentiment_analysis import get_twitter_sentiment

def main():
    if not os.path.isfile(TWITTER_STREAMING_DATA_FILE):
        write_streaming_data()
    print(get_twitter_sentiment())