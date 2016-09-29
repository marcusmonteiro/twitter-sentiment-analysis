import json
import os.path
import time
from config import TWITTER_STREAMING_DATA_FILE, HOURS_PASSED_FOR_FILE_UPDATE, SECONDS_IN_HOUR
from twitter_data import write_streaming_data


def make_word_sentiment_dict(file='AFINN-111.txt'):
    '''Build a dict with words as keys and their sentiment values as values'''
    ret = {}
    with open(file, 'r') as f:
        for line in f:
            l = line.strip().split('\t')
            ret[l[0]] = int(l[1])
    return ret


def sentence_sentiment_value(sentence, sentiment_dict):
    '''
    Returns the sentiment value of a sentence. The 'sentiment_dict' argument
    is a dictionary of words and their correspondent negative or positive values
    '''
    ret = 0

    for word in sentence.split():
        try:
            ret = ret + sentiment_dict[word]
        except KeyError:
            pass

    return ret

def update_data_file(file=TWITTER_STREAMING_DATA_FILE, hours=HOURS_PASSED_FOR_FILE_UPDATE):
    '''Update data file when a certain time has passed after it was last modified'''
    try:
        with open(file) as f:
            SECONDS_FOR_UPDATE = hours * SECONDS_IN_HOUR
            last_modified = os.path.getmtime(file)
            if (time.time() - last_modified) > SECONDS_FOR_UPDATE:
                write_streaming_data()
    except FileNotFoundError:
        pass


def get_twitter_sentiment(file=TWITTER_STREAMING_DATA_FILE):
    '''Returns the current twitter_sentiment'''
    sentiment_dict = make_word_sentiment_dict()
    update_data_file()

    def f():
        ret = {
          'sentiment_value': 0,
          'tweets_read': 0,
          'tweet_samples': []
        }
        max_number_samples = 10
        with open(file, 'r') as f:
            data = json.load(f)
            for tweet in data:
                ret['sentiment_value'] = ret['sentiment_value'] + sentence_sentiment_value(tweet, sentiment_dict)
                ret['tweets_read'] = ret['tweets_read'] + 1
                if len(ret['tweet_samples']) < max_number_samples:
                    ret['tweet_samples'].append(tweet)
        return ret

    try:
        return f()
    except FileNotFoundError:
        print('Getting twitter streaming data, please wait...')
        write_streaming_data()
        return f()
