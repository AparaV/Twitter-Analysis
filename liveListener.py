import time
from tweepy.streaming import StreamListener

runTime = 30  # 5 minutes - change it back to 5 minutes


# Listening to Live Tweets
class Listener(StreamListener):
    def __init__(self, file='liveStream.json'):
        self.startTime = time.time()
        self.fname = file
        open(self.fname, 'w').close()

    #If I don't get any data, this function doesnt shut down!
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
