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

        self.retweetIndex = self._findRetweetIndex()
        self.favoriteIndex = self._findFavoriteIndex()
        self.followersIndex = self._findFollowersIndex()

        popularityScore = 0
        popularityScore += int(self.retweetIndex + self.favoriteIndex + self.followersIndex + self.totalTweets)

        return popularityScore

    def _likeScore(self, likes, followers):
        if followers != 0:
            return float(likes) / followers
        return 0

    def _findRetweetIndex(self):
        if self.totalTweets != 0:
            return float(self.retweetCount) / self.totalTweets
        return 0

    def _findFavoriteIndex(self):
        if len(self.likes_score) != 0:
            return sum(self.likes_score) / float(len(self.likes_score))
        return 0

    def _findFollowersIndex(self):
        if len(self.followers_score) != 0:
            return sum(self.followers_score) / float(len(self.followers_score))
        return 0