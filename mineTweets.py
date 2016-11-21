import json
import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

#App credentials
consumer_key = ""
consumer_secret = ""
access_token = ""
access_secret = ""

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

#Listening to Live Tweets
class MyListener(StreamListener):

	def on_data(self, data):
		try:
			with open('live_stream.json', 'a') as f:
				f.write(data)
				return True
		except BaseException as e:
			print "Error"
		return True

	def on_error(self, status_code):
		print status_code
		if status_code == 420:
			print "Connection not established"
		return False

#Tracking live tweets with keyword "tracking"
''''
	twitter_stream = Stream(auth, MyListener())
	twitter_stream.filter(track = ['tracking'])
'''

#Gathering tweets from a user with screen_name = "screen_name"
for status in tweepy.Cursor(api.user_timeline, screen_name = "screen_name").items(200):
	with open("screen_name_tweets.json", "a") as f:
		json.dump(dict(status._json), f)
		f.write('\n')
