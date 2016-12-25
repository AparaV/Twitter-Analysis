from flask import Flask
from flask import render_template
from flask import request
import tweetminer

app = Flask(__name__)

fname = './tmp/liveStream.json'

@app.route("/")
def init():
    return render_template('index.html')

@app.route("/", methods=['POST'])
def calc():
    text = request.form['query']
    run_time = int(request.form['runtime'])
    x = calculate(text, run_time)
    return render_template('index.html', phrase=text, pop=x)

def calculate(phrase, runTime):
    auth, api = tweetminer.get_credentials()
    tweetminer.get_live_tweets(auth, phrase, fname=fname, runTime=runTime)
    score = tweetminer.get_popularity(runTime=runTime, fname=fname)
    return score

if __name__ == "__main__":
    app.run()
