import json
from config import TWITTER_STREAMING_DATA_FILE
from twitter_data import write_streaming_data


def make_word_sentiment_dict(file="AFINN-111.txt"):
    """Build a dict with words as keys and their sentiment values as values"""
    ret = {}
    with open(file, "r") as f:
        for line in f:
            l = line.strip().split("\t")
            ret[l[0]] = int(l[1])
    return ret


def sentence_sentiment_value(sentence, sentiment_dict):
    """
    Returns the sentiment value of a sentence. The 'sentiment_dict' argument
    is a dictionary of words and their correspondent negative or positive values
    """
    ret = 0

    for word in sentence.split():
        try:
            ret = ret + sentiment_dict[word]
        except KeyError:
            pass

    return ret


def get_twitter_sentiment(file=TWITTER_STREAMING_DATA_FILE):
    """Returns the current twitter_sentiment"""
    sentiment_dict = make_word_sentiment_dict()

    def f():
        ret = 0
        with open(file, 'r') as f:
            data = json.load(f)
            for tweet in data:
                ret = ret + sentence_sentiment_value(tweet, sentiment_dict)
        return ret

    try:
        return f()
    except FileNotFoundError:
        print("Getting twitter streaming data, please wait...")
        write_streaming_data()
        return f()
