import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from liveListener import Listener

# # File containing API and Access credentials
# config_fname = 'config'

# # App credentials
# with open(config_fname, 'r') as f:
#     consumer_key = f.readline().replace('\n', '')
#     consumer_secret = f.readline().replace('\n', '')
#     access_token = f.readline().replace('\n', '')
#     access_secret = f.readline().replace('\n', '')
#
# auth = OAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_token, access_secret)
#
# api = tweepy.API(auth)

class TweetMiner:
    def __init__(self, config_fname='config'):
        _readdetails(config_fname)
        _authenticate(self)

    def choice(self):
        self.state = None
        while self.state != '1' or self.state != '2':
            print "Press 1 to calculate popularity of a phrase. Press 2 to analyze a user profile."
            self.state = str(raw_input())
            if self.state == '1' or self.state == '2':
                break
            print "Enter a valid choice"
        #Call functions

    def trackLiveTweets(self):
        print "Enter a key word to track for 5 minutes. Be as specific as possible"
        self.trackWord = str(raw_input())
        self.twitter_stream = Stream(self.auth, Listener())
        self.twitter_stream.filter(track=[self.trackWord])

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


if __name__ == "__main__":
    # print "Enter a key word to track for 5 minutes. Be as specific as possible"
    # trackWord = str(raw_input())

    # Tracking live tweets with keyword
    twitter_stream = Stream(auth, Listener())
    twitter_stream.filter(track=[trackWord])

    # Gathering tweets of a user
    '''
	print "Enter the user <screen_name> to track"
	screenName = str(raw_input())
	fname = screenName + "_tweets.json"
	for status in tweepy.Cursor(api.user_timeline, screen_name = screenName).items(200):
		with open(fname, "a") as f:
			json.dump(dict(status._json), f)
			f.write('\n')
	'''
