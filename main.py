from tweepy import Stream

from mineTweets import TweetMiner
from calculatePopularity import CalculatePopularity
from processTweets import AnalyzeUser
from flask import Flask
from flask import render_template
from flask import request
from flask import session
import tweepy
from liveListener import Listener

app = Flask(__name__)

name = 'Apara'

@app.route("/")
def get_input():
    return render_template('sample.html', name=name)

@app.route("/calc", methods=['POST'])
def calc():
    text = request.form['text']
    print text
    x = flask_pop(text)
    print text
    return render_template('sample.html', x=x)

def flask_pop(phrase):
    with open('config', 'r') as f:
        consumer_key = f.readline().replace('\n', '')
        consumer_secret = f.readline().replace('\n', '')
        access_token = f.readline().replace('\n', '')
        access_secret = f.readline().replace('\n', '')
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)
    print 'hello'
    twitter_stream = Stream(auth, Listener('liveStream.json'))
    print 'hello'
    twitter_stream.filter(track=[phrase])
    print 'hello'
    pop = CalculatePopularity('liveStream.json')
    print 'hello'
    return pop.calculateScore()

def main():
    miner = TweetMiner()
    state, fname = miner.mine()

    if state == '1':
        pop = CalculatePopularity(fname)
        print pop.calculateScore()

    elif state == '2':
        user = AnalyzeUser(fname)
        user.analyze()


if __name__ == "__main__":
    app.run()
