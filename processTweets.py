import json
import re
import operator
import string
import collections
import vincent
import pandas
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Setup regex to ingore emoticons
emoticons_str = r"""
	(?:
		[:=;] Eyes
		[oO\-]? # Nose (optional)
		[D\)\]\(\]/\\OpP] # Mouth
	)"""

# Setup regex to split mentions, hashtags, urls, etc. together
regex_str = [
    emoticons_str,
    r'<[^>]+>',  # HTML tags
    r'(?:@[\w_]+)',  # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)",  # hashtags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+',  # URLs
    r'(?:(?:\d+,?)+(?:\.?\d+)?)',  # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])",  # words with - and '
    r'(?:[\w_]+)',  # other words
    r'(?:\S)'  # anything else
]

tokens_re = re.compile(r'(' + '|'.join(regex_str) + ')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^' + emoticons_str + '$', re.VERBOSE | re.IGNORECASE)


def tokenize(s):
    return tokens_re.findall(s)


def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    for token in tokens:
        token = token.encode('utf-8')
    return tokens


punctuation = list(string.punctuation)
others = ['RT', 'via', u'\u2026', 'The', u'\u2019', 'amp', 'nil']
stop = stopwords.words('english') + punctuation + others


# Find most common words
def terms_only(fname, number):
    with open(fname, 'r') as f:
        count_all = Counter()
        for line in f:
            tweet = json.loads(line)
            terms_stop = [term for term in preprocess(tweet.get('text', 'nil'))
                          if term not in stop and not term.startswith(('#', '@'))]
            count_all.update(terms_stop)
        print(count_all.most_common(number))
        return count_all.most_common(number)


# Find most common hashtags
def hash_only(fname, number):
    with open(fname, 'r') as f:
        count_all = Counter()
        for line in f:
            tweet = json.loads(line)
            terms_hash = [term for term in preprocess(tweet.get('text', 'nil'))
                          if term not in stop if term.startswith('#')]
            count_all.update(terms_hash)
        print(count_all.most_common(number))


# Find most common mentions
def mentions_only(fname, number):
    with open(fname, 'r') as f:
        count_all = Counter()
        for line in f:
            tweet = json.loads(line)
            terms_mentions = [term for term in preprocess(tweet.get('text', 'nil'))
                              if term not in stop if term.startswith('@')]
            count_all.update(terms_mentions)
        print(count_all.most_common(number))


# Find most common two-term occurances
def cooccurances(fname, number):
    with open(fname, 'r') as f:
        com = collections.defaultdict(lambda: collections.defaultdict(int))

        for line in f:
            tweet = json.loads(line)
            terms_only = [term for term in preprocess(tweet.get('text', 'nil'))
                          if term not in stop and not term.startswith(('#', '@'))]
            for i in range(len(terms_only)):
                for j in range(i + 1, len(terms_only)):
                    w1, w2 = sorted([terms_only[i], terms_only[j]])
                    if w1 != w2:
                        com[w1][w2] += 1
        com_max = []
        for t1 in com:
            t1_max_terms = sorted(com[t1].items(), key=operator.itemgetter(1), reverse=True)[:number]
            for t2, t2_count in t1_max_terms:
                com_max.append(((t1, t2), t2_count))
        terms_max = sorted(com_max, key=operator.itemgetter(1), reverse=True)
        print(terms_max[:number])


# Main Function Begins
if __name__ == "__main__":
    fname = "liveStream.json"
    number = 10
    '''
	print "Terms only"
	terms_only(fname, number)

	print "\nHashtags only"
	hash_only(fname, number)

	print "\nMentions only"
	mentions_only(fname, number)

	print "\nCooccurances"
	cooccurances(fname, number)
	'''

    word_freq = terms_only(fname, 20)
    labels, freq = zip(*word_freq)
    data = {'data': freq, 'x': labels}
    bar = vincent.Bar(data, iter_idx='x')
    bar.to_json('term_freq.json')

    # Time data visualization
    dates_Search = []
    with open(fname, 'r') as f:
        for line in f:
            tweet = json.loads(line)
            terms_only = [term for term in preprocess(tweet.get('text', 'nil'))]
            if 'search' in terms_only:
                dates_Search.append(tweet['created_at'])

    ones = [1] * len(dates_Search)

    idx = pandas.DatetimeIndex(dates_Search)
    Search = pandas.Series(ones, idx)

    per_minute = Search.resample('1Min', how='sum').fillna(0)

    time_chart = vincent.Line(per_minute)
    time_chart.axis_titles(x="time", y="Freq")
    time_chart.to_json('time_chart.json')
