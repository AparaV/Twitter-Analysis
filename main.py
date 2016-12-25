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
    return render_template('loading.html', text=phrase, time=run_time)

@app.route("/result")
def result():
    search = phrase
    x = score
    #resetglobal()
    return render_template('output.html', text=search, pop=x)

def something(text, time):
    global finished
    global score
    score = calculate(text, time)
    finished = True

@app.route("/status")
def status():
    #global finished
    return jsonify(dict(status=('finished' if finished else 'running')))

def calculate(text, runTime):
    auth, api = tweetminer.get_credentials()
    tweetminer.get_live_tweets(auth, text, fname=fname, runTime=runTime)
    x = tweetminer.get_popularity(runTime=runTime, fname=fname)
    return x

def resetglobal():
    global th
    #global score
    #global phrase
    global finished
    th = None
    #score = -1
    #phrase = ""
    finished = False

if __name__ == "__main__":
    app.run(debug=False)
