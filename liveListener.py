import time
from tweepy.streaming import StreamListener

runTime = 5 * 60  # 5 minutes


# Listening to Live Tweets
class Listener(StreamListener):
    def __init__(self, file='liveStream.json'):
        self.startTime = time.time()
        self.fname = file
        open(self.fname, 'w').close()

    def on_data(self, data):

        if (time.time() - self.startTime) >= runTime:
            return False

        try:
            with open(self.fname, 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            print "Error"
        return True

    def on_error(self, status_code):
        print status_code
        if status_code == 420:
            print "Connection not established"
        return False
