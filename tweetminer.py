import tweepy
import time
import os
from tweepy import OAuthHandler
from tweepy import Stream
from liveListener import Listener
from calculatePopularity import CalculatePopularity

def get_credentials():
    consumer_key = os.environ.get('CONSUMER_KEY')
    consumer_secret = os.environ.get('CONSUMER_SECRET')
    access_token = os.environ.get('ACCESS_TOKEN')
    access_secret = os.environ.get('ACCESS_SECRET')
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)
    return auth, api

def get_live_tweets(auth, phrase, fname='./tmp/liveStream.json', runTime=60):
    twitter_stream = Stream(auth, Listener(fname))
    twitter_stream.filter(track=[phrase], async=True)
    time.sleep(runTime)
    twitter_stream.disconnect()

def get_popularity(runTime, fname='./tmp/liveStream.json'):
    temp = CalculatePopularity(runTime=runTime, file=fname)
    score = temp.calculateScore()
    return score