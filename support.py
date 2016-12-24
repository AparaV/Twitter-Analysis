import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from liveListener import Listener
from calculatePopularity import CalculatePopularity

def get_credentials(fname='config'):
    with open('config', 'r') as f:
        consumer_key = f.readline().replace('\n', '')
        consumer_secret = f.readline().replace('\n', '')
        access_token = f.readline().replace('\n', '')
        access_secret = f.readline().replace('\n', '')
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)
    return auth, api

def get_live_tweets(auth, phrase, fname='liveStream.json'):
    twitter_stream = Stream(auth, Listener(fname))
    twitter_stream.filter(track=[phrase])

def get_popularity(fname='liveStream.json'):
    temp = CalculatePopularity(fname)
    score = temp.calculateScore()
    return score