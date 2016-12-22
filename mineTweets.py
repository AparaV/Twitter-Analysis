import tweepy
import json
from tweepy import OAuthHandler
from tweepy import Stream
from liveListener import Listener


class TweetMiner:
    def __init__(self, config_fname='config'):
        self._readdetails(config_fname)
        self._authenticate()

    def mine(self):
        self.state = None
        while self.state != '1' or self.state != '2':
            print "Press 1 to calculate popularity of a phrase. Press 2 to analyze a user profile."
            self.state = str(raw_input())
            if self.state == '1' or self.state == '2':
                break
            print "Enter a valid choice"
        # Call functions
        if self.state == '1':
            return self.state, self.trackLiveTweets()
        elif self.state == '2':
            return self.state, self.getUserTweets()

    # Tracking live tweets for popularity calculation
    def trackLiveTweets(self):
        print "Enter a key word to track for 5 minutes. Be as specific as possible"
        self.file = 'tweets.json'
        self.trackWord = str(raw_input())
        self.twitter_stream = Stream(self.auth, Listener(self.file))
        self.twitter_stream.filter(track=[self.trackWord])
        return self.file

    # Getting tweets from user profile for analysis
    def getUserTweets(self):
        print "Enter the user <screen_name> to track. For example, '@user' without the quotes."
        self.screenName = str(raw_input())
        self.file = self.screenName + "_tweets.json"
        open(self.file, 'w').close()
        for status in tweepy.Cursor(self.api.user_timeline, screen_name=self.screenName).items(200):
            with open(self.file, "a") as f:
                json.dump(dict(status._json), f)
                f.write('\n')
        return self.file

    def _readdetails(self, config_fname):
        with open(config_fname, 'r') as f:
            self.consumer_key = f.readline().replace('\n', '')
            self.consumer_secret = f.readline().replace('\n', '')
            self.access_token = f.readline().replace('\n', '')
            self.access_secret = f.readline().replace('\n', '')

    def _authenticate(self):
        self.auth = OAuthHandler(self.consumer_key, self.consumer_secret)
        self.auth.set_access_token(self.access_token, self.access_secret)
        self.api = tweepy.API(self.auth)
