from flask import Flask
from flask import render_template
from flask import request
import tweetminer

app = Flask(__name__)

fname = 'liveStream.json'

@app.route("/")
def init():
    return render_template('index.html')

@app.route("/", methods=['POST'])
def calc():
    text = request.form['query']
    print text
    x = calculate(text)
    print x
    return render_template('index.html', phrase=text, pop=x)

def calculate(phrase):
    runTime = 10
    auth, api = tweetminer.get_credentials()
    tweetminer.get_live_tweets(auth, phrase, fname=fname, runTime=runTime)
    score = tweetminer.get_popularity(runTime=runTime, fname=fname)
    return score

if __name__ == "__main__":
    app.run()
