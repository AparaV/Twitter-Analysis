import json

def likeScore(likes, followers):
	if followers == 0:
		return 0
	return float(likes) / followers * 100

def findRetweetIndex(retweetCount, totalTweets):
	return float(retweetCount) / totalTweets * 100

def findFavoriteIndex(likes):
	return sum(likes) / float(len(likes))

def findFollowersIndex(followers):
	return sum(followers) / float(len(followers))

fname = "liveStream.json"

if __name__ == "__main__":
	totalTweets = 0
	retweetCount = 0
	likes_score = []
	followers_score = []
	
	#calculate popularity of tweets
	with open(fname, 'r') as f:
		for line in f:
			totalTweets += 1
			tweet = json.loads(line)
			
			try:
				retweetCount += int(tweet['retweeted_status']['retweet_count'])
			except KeyError:
				retweetCount += 0
			
			try:
				followers =  int(tweet['user']['followers_count'])
			except KeyError:
				followers = 0
			followers_score.append(followers)
			
			try:
				likes = int(tweet['retweeted_status']['favorite_count'])
			except KeyError:
				likes = 0
			likeIndex = likeScore(likes, followers)
			likes_score.append(likeIndex)
	
	retweetIndex = findRetweetIndex(retweetCount, totalTweets)
	favoriteIndex = findFavoriteIndex(likes_score)
	followersIndex = findFollowersIndex(followers_score)
	
	print "Retweet Index", retweetIndex
	print "Favorite Index", favoriteIndex
	print "Followers Index", followersIndex
	
	popularityScore = retweetIndex + favoriteIndex + followersIndex
	
	print "Popularity Score", popularityScore
			
