import unittest
import os
from twitter_sentiment_analysis import *


TEST_FILE = 'AFINN-111.test.txt'


class TestMakeWordSentimentDict(unittest.TestCase):

    def write_to_test_file(self, lines):
        with open(TEST_FILE, 'w+') as f:
            for line in lines:
                f.write(line)

    def remove_test_file(self):
        try:
            os.remove(TEST_FILE)
        except FileNotFoundError:
            pass

    def test_file_not_found(self):
        self.remove_test_file()
        self.assertRaises(FileNotFoundError, make_word_sentiment_dict, TEST_FILE)

    def test_empty_file(self):
        lines = []
        self.write_to_test_file(lines)
        self.assertRaises(Exception, make_word_sentiment_dict, TEST_FILE)
        self.remove_test_file()


if __name__ == '__main__':
    unittest.main()