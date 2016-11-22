import json
import tweepy
import time
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

#File containing API and Access credentials
config_fname = 'config'

#App credentials
with open(config_fname, 'r') as f:
	consumer_key = f.readline().replace('\n', '')
	consumer_secret = f.readline().replace('\n', '')
	access_token = f.readline().replace('\n', '')
	access_secret = f.readline().replace('\n', '')

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

runTime = 5 * 60 #5 minutes

#Listening to Live Tweets
class MyListener(StreamListener):
	
	def __init__(self):
		self.startTime = time.time()

	def on_data(self, data):

		if (time.time() - self.startTime) >= runTime:
			return False
			
		try:
			with open('liveStream.json', 'a') as f:
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

if __name__ == "__main__":
	
	print "Enter a key word to track for 5 minutes. Be as specific as possible"
	trackWord = str(raw_input())
	
	#Tracking live tweets with keyword
	twitter_stream = Stream(auth, MyListener())
	twitter_stream.filter(track = [trackWord])

	#Gathering tweets of a user
	'''
	print "Enter the user <screen_name> to track"
	screenName = str(raw_input())
	fname = screenName + "_tweets.json"
	for status in tweepy.Cursor(api.user_timeline, screen_name = screenName).items(200):
		with open(fname, "a") as f:
			json.dump(dict(status._json), f)
			f.write('\n')
	'''
