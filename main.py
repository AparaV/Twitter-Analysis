from mineTweets import TweetMiner
from calculatePopularity import CalculatePopularity
from processTweets import AnalyzeUser

if __name__ == "__main__":
    miner = TweetMiner()
    state, fname = miner.mine()

    if state == '1':
        pop = CalculatePopularity(fname)
        print pop.calculateScore()

    elif state == '2':
        user = AnalyzeUser(fname)
        user.analyze()