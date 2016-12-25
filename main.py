from flask import Flask, jsonify
from flask import render_template
from flask import request
from threading import Thread
import tweetminer

app = Flask(__name__)

fname = './tmp/liveStream.json'

th = None
score = -1
phrase = ""
finished = False

@app.route("/")
def init():
    return render_template('index.html')

@app.route("/", methods=['POST'])
def calc():
    global th
    global finished
    global score
    global phrase
    text = request.form['query']
    run_time = int(request.form['runtime'])
    finished = False
    phrase = text
    th = Thread(target=something, args=(text, run_time))
    th.start()
    # x = calculate(text, run_time)
    return render_template('loading.html', text=phrase, time=run_time)

@app.route("/result")
def result():
    return render_template('output.html', text=phrase, pop=score)

def something(text, time):
    global finished
    global score
    score = calculate(text, time)
    finished = True

@app.route("/status")
def status():
    global finished
    return jsonify(dict(status=('finished' if finished else 'running')))

def calculate(text, runTime):
    auth, api = tweetminer.get_credentials()
    tweetminer.get_live_tweets(auth, text, fname=fname, runTime=runTime)
    x = tweetminer.get_popularity(runTime=runTime, fname=fname)
    return x

if __name__ == "__main__":
    app.run(debug=True)
