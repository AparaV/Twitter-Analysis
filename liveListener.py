from tweepy.streaming import StreamListener

# Listening to Live Tweets
class Listener(StreamListener):
    def __init__(self, file='liveStream.json'):
        self.fname = file
        open(self.fname, 'w').close()

    def on_data(self, data):
        try:
            with open(self.fname, 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            print ("Error")
        return True

    def on_error(self, status_code):
        print (status_code)
        if status_code == 420:
            print ("Connection not established")
        return False
