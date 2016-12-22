#Twitter Analysis
Analyze most recent tweets and calculate the 'popularity' of a word or phrase on Twitter.
You can also check out what your friends (or you!) most commonly tweet about.

##Dependencies
```
pip install tweepy
pip install pandas
pip install vincent
pip install nltk
```
Additionally, download the stopwords package by going into the python console
```
>>>import nltk
>>>nltk.download()
```
A GUI window will open. Go to Corpora and download stopwords

##API Keys
You will need an active Twitter account in order to use the code. You must register a new app with that Twitter account to get the following credentials and put them in a file named 'config' in the same order.

+ Consumer Key (API Key)
+ Consumer Secret (API Secret)
+ Access Token
+ Access Token Secret

Be sure to keep these information confidential!

##What's next?
Right now, the math is a bit wibbly wobbly. So when you calculate the popularity, you will not get an absolutely deterministic score. You will have to get the scores of a few other phrases in order to get a qualitative feel. Hence, the algorithm I use still needs a lot of work.
I plan to incorporate (if I find the time) a time frequency feature that would display how often a phrase was tweeted or how often your friend is active on Twitter.
