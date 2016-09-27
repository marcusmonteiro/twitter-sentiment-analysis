import json
import time
import tweepy
from utils import get_or_set_environment_variable
from config import TWITTER_STREAMING_DATA_FILE, MINUTES_GETTING_STREAM


def make_tweepy_api():
    """Returns a tweepy api object with the authentication set by environment variables"""
    consumer_key = get_or_set_environment_variable("TWITTER_CONSUMER_KEY")
    consumer_secret = get_or_set_environment_variable("TWITTER_CONSUMER_SECRET")
    access_token = get_or_set_environment_variable("TWITTER_ACCESS_TOKEN")
    access_token_secret = get_or_set_environment_variable("TWITTER_ACCESS_TOKEN_SECRET")

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    return tweepy.API(auth)


def write_streaming_data(minutes=MINUTES_GETTING_STREAM, file=TWITTER_STREAMING_DATA_FILE):
    """Write a stream of tweet statuses to a file"""
    seconds = minutes * 60
    class StdOutListener(tweepy.StreamListener):
        def __init__(self, time_limit=seconds):
            self.start_time = time.time()
            self.time_limit = time_limit
            self.tweets = []
            super(StdOutListener, self).__init__()

        def on_data(self, data):
            if (time.time() - self.start_time) < self.time_limit:
                try:
                    self.tweets.append(json.loads(data)['text'])
                except KeyError:
                    pass
                return True
            else:
                with open(file, mode="w", encoding="utf-8") as f:
                    f.write(json.dumps(self.tweets))
                return False

        def on_error(self, status):
            print(status)

    twitter_stream = tweepy.Stream(auth=make_tweepy_api().auth, listener=StdOutListener())
    twitter_stream.sample()
