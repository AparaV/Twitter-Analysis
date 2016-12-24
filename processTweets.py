import collections
import json
import operator
import re
import string
from collections import Counter

import pandas
import vincent
from server import Server
from nltk.corpus import stopwords



class AnalyzeUser():
    def __init__(self, file='tweets.json'):
        self.fname = file
        self.emoticons_re = None
        self.tokens_re, self.emoticons_re = self._setupregex()
        self.punctuation = list(string.punctuation)
        self.others = ['RT', 'via', u'\u2026', 'The', u'\u2019', 'amp', 'nil']
        self.stop = stopwords.words('english') + self.punctuation + self.others

    def analyze(self, number=20):
        self.number = number
        common_terms = self.terms_only()
        common_hashes = self.hash_only()
        common_mentions = self.mentions_only()
        common_coocurrances = self.cooccurances()
        self.toJSON(common_terms)
        #self.timeDataVisualization()
        #self.printInstructions()
        #self.server = Server()
        #self.server.openbrowser('http://localhost:8000/chart.html')

    def printInstructions(self):
        print "Setup server by going into console:"
        print ">>>python -m SimpleHTTPServer"
        print "Go to http://localhost:8000 on your browser"
        print "View chart.html"

    def toJSON(self, common):
        labels, freq = zip(*common)
        data = {'data': freq, 'x': labels}
        bar = vincent.Bar(data, iter_idx='x')
        bar.to_json('term_freq.json')

    def timeDataVisualization(self):
        dates_Search = []
        with open(self.fname, 'r') as f:
            for line in f:
                tweet = json.loads(line)
                terms_only = [term for term in self._preprocess(tweet.get('text', 'nil'))]
                if 'search' in terms_only:
                    dates_Search.append(tweet['created_at'])
        ones = [1] * len(dates_Search)

        idx = pandas.DatetimeIndex(dates_Search)
        Search = pandas.Series(ones, idx)

        per_minute = Search.resample('1Min', how='sum').fillna(0)

        time_chart = vincent.Line(per_minute)
        time_chart.axis_titles(x="time", y="Freq")
        time_chart.to_json('time_chart.json')

    def terms_only(self):
        with open(self.fname, 'r') as f:
            count_all = Counter()
            for line in f:
                tweet = json.loads(line)
                terms_stop = [term for term in self._preprocess(tweet.get('text', 'nil'))
                              if term not in self.stop and not term.startswith(('#', '@'))]
                count_all.update(terms_stop)
            return count_all.most_common(self.number)

    def hash_only(self):
        with open(self.fname, 'r') as f:
            count_all = Counter()
            for line in f:
                tweet = json.loads(line)
                terms_hash = [term for term in self._preprocess(tweet.get('text', 'nil'))
                              if term not in self.stop if term.startswith('#')]
                count_all.update(terms_hash)
            return count_all.most_common(self.number)

    # Find most common mentions
    def mentions_only(self):
        with open(self.fname, 'r') as f:
            count_all = Counter()
            for line in f:
                tweet = json.loads(line)
                terms_mentions = [term for term in self._preprocess(tweet.get('text', 'nil'))
                                  if term not in self.stop if term.startswith('@')]
                count_all.update(terms_mentions)
            return count_all.most_common(self.number)

    # Find most common two-term occurances
    def cooccurances(self):
        with open(self.fname, 'r') as f:
            com = collections.defaultdict(lambda: collections.defaultdict(int))

            for line in f:
                tweet = json.loads(line)
                terms_only = [term for term in self._preprocess(tweet.get('text', 'nil'))
                              if term not in self.stop and not term.startswith(('#', '@'))]
                for i in range(len(terms_only)):
                    for j in range(i + 1, len(terms_only)):
                        w1, w2 = sorted([terms_only[i], terms_only[j]])
                        if w1 != w2:
                            com[w1][w2] += 1
            com_max = []
            for t1 in com:
                t1_max_terms = sorted(com[t1].items(), key=operator.itemgetter(1), reverse=True)[:self.number]
                for t2, t2_count in t1_max_terms:
                    com_max.append(((t1, t2), t2_count))
            terms_max = sorted(com_max, key=operator.itemgetter(1), reverse=True)
            return terms_max[:self.number]

    def _setupregex(self):
        emoticons_str = r"""
            (?:
                [:=;] Eyes
                [oO\-]? # Nose (optional)
                [D\)\]\(\]/\\OpP] # Mouth
            )"""

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
        return tokens_re, emoticon_re

    def _tokenize(self, s):
        return self.tokens_re.findall(s)

    def _preprocess(self, s, lowercase=False):
        tokens = self._tokenize(s)
        if lowercase:
            tokens = [token if self.emoticon_re.search(token) else token.lower() for token in tokens]
        for token in tokens:
            token = token.encode('utf-8')
        return tokens
