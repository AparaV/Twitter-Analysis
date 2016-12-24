from flask import Flask
from flask import render_template
from flask import request
import support

app = Flask(__name__)

fname = 'liveStream.json'

@app.route("/")
def get_input():
    return render_template('index.html')

@app.route("/", methods=['POST'])
def calc():
    text = request.form['text']
    print text
    x = flask_pop(text)
    print text
    return render_template('index.html', phrase=text, x=x)

def flask_pop(phrase):
    auth, api = support.get_credentials()
    support.get_live_tweets(auth, phrase, fname=fname)
    score = support.get_popularity(fname=fname)
    return score

if __name__ == "__main__":
    app.run()
