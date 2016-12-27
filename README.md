#Popularity on Twitter
This app tracks all live tweets containing a search query and calculates a score based on the collected data.
This app is written in Python and makes use of [tweepy](http://www.tweepy.org/), a python wrapper for the Twitter API.

Check it out in action at [Popularity on Twitter](https://popularity-on-twitter.herokuapp.com/) hosted on [Heroku](http://heroku.com).

##How it works?
Using the Twitter [Streaming API](https://dev.twitter.com/streaming/overview), it downloads all live tweets for a specified amount of time that is determined during runtime.
This can be difficult as the stream does no stop until a manual termination. However, I found a [fix](http://stackoverflow.com/a/41325744/5055644) for that.

Then it becomes a matter of some math to compute the score. This is the formula I used:

>First, I had find all the factors that determine the popularity. The total number of tweets gathered in the time interval is the most obvious.
>The number of followers the tweeter has should also play a role because if he has more followers, then the tweet ends up on more user’s feeds.
>Then there is the retweet count. This makes sense because if a tweet is being retweeted more, then it is clearly reaching more people and getting more attention.
>Then the number of likes is similar to the retweet count.
>
>Hence, I calculated the total number of tweets. Then I summed up retweet count for all tweets and calculated the retweet index.
>Then I averaged the number of followers each user had across the entire set. Then, for the likes, I divided the likes each tweet had with the number
>of followers the user had because liked tweets show up less on someone else’s feed. I averaged this new likes index across the entire set.
>Then I summed them all up and divided them by the amount of time the tweets were collected
>
>Clearly there are some fallacies here. For instance, I should probably factor in the number of followers for the retweets similar to the likes count.
>Maybe I could assign weights to each of these factors and then find the score which would help a lot as it scales down the score to a range.
>There is obviously scope for improvement here. In fact, I want to improve this and I tweak this often when I get new ideas.

That was taken from my [blog post](https://traxex33.github.io/#!/archive/2016/dec/building-twitter-app). Consider reading it if you want to know more.
It also contains math equations (GitHub doesn't natively support rendering mathematical equations).

##Some nuances
Twitter has a rate limit on the streaming API. Hence, you are bound to get some errors if you make too many queries.
Others may also be using it. So don't be surprised if you get an error thrown on your first attempt.
Wait for a few hours and try again. Better yet, fork the repo and run it locally!

##How do I run it locally?
Simple.

Clone this repo to you machine.

Install all dependencies that are listed in `requirements.txt`

Register your app on Twitter to gain your Consumer Key, Consumer Secret and optionally Access Token and Access Secret.

Then, go into `tweetminer.py` and modify the following piece of code in the `get_credentials()` function as follows:

```
consumer_key = os.environ.get('CONSUMER_KEY', 'your_consumer_key')
consumer_secret = os.environ.get('CONSUMER_SECRET', 'your_consumer_secret')
access_token = os.environ.get('ACCESS_TOKEN', 'your_access_token')
access_secret = os.environ.get('ACCESS_SECRET', 'your_access_secret')
```

Now run `main.py` and go to `localhost:5000/` to test your copy.
