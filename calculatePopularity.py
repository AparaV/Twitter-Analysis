import json


class CalculatePopularity():
    def __init__(self, file='liveStream.json'):
        self.fname = file

    def calculateScore(self):
        self.totalTweets = 0
        self.retweetCount = 0
        self.likes_score = []
        self.followers_score = []
        with open(self.fname, 'r') as f:
            for line in f:
                self.totalTweets += 1
                tweet = json.loads(line)

                try:
                    self.retweetCount += int(tweet['retweeted_status']['retweet_count'])
                except KeyError:
                    self.retweetCount += 0

                try:
                    followers = int(tweet['user']['followers_count'])
                except KeyError:
                    followers = 0
                self.followers_score.append(followers)

                try:
                    likes = int(tweet['retweeted_status']['favorite_count'])
                except KeyError:
                    likes = 0
                likeIndex = self._likeScore(likes, followers)
                self.likes_score.append(likeIndex)

        self.retweetIndex = self._findRetweetIndex(self.retweetCount, self.totalTweets)
        self.favoriteIndex = self._findFavoriteIndex(self.likes_score)
        self.followersIndex = self._findFollowersIndex(self.followers_score)

        print "Retweet Index", self.retweetIndex
        print "Favorite Index", self.favoriteIndex
        print "Followers Index", self.followersIndex

        popularityScore = int(self.retweetIndex + self.favoriteIndex + self.followersIndex + self.totalTweets)
        return popularityScore

    def _likeScore(self, likes, followers):
        if followers == 0:
            return 0
        return float(likes) / followers

    def _findRetweetIndex(self, retweetCount, totalTweets):
        return float(retweetCount) / totalTweets

    def _findFavoriteIndex(self, likes):
        return sum(likes) / float(len(likes))

    def _findFollowersIndex(self, followers):
        return sum(followers) / float(len(followers))
