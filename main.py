from flask import Flask, jsonify
from flask import render_template
from flask import request
from threading import Thread
import tweetminer

app = Flask(__name__)

fname = './tmp/liveStream.json'

class Global:
    th = None
    score = -1
    phrase = ""
    finished = False

@app.route("/")
def init():
    return render_template('index.html')

@app.route("/", methods=['POST'])
def calc():
    text = request.form['query']
    run_time = int(request.form['runtime'])
    Global.finished = False
    Global.phrase = text
    Global.th = Thread(target=something, args=(text, run_time))
    Global.th.start()
    return render_template('loading.html', text=Global.phrase, time=run_time)

@app.route("/result")
def result():
    return render_template('output.html', text=Global.phrase, pop=Global.score)

def something(text, time):
    Global.score = calculate(text, time)
    Global.finished = True

@app.route("/status")
def status():
    return jsonify(dict(status=('finished' if Global.finished else 'running')))

def calculate(text, runTime):
    auth, api = tweetminer.get_credentials()
    tweetminer.get_live_tweets(auth, text, fname=fname, runTime=runTime)
    x = tweetminer.get_popularity(runTime=runTime, fname=fname)
    return x

if __name__ == "__main__":
    app.run(debug=True)
