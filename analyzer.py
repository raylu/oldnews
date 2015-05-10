#!/usr/bin/env python3

from collections import Counter
import heapq
from pprint import pprint
import string

import nltk
import yaml

with open('articles.yaml', 'r') as f:
	articles = yaml.load(f)

df = Counter()
letters = set(string.ascii_lowercase)
for article in articles:
	tf = Counter()
	text = article['abstract'] + '\n' + article['content']
	for word in nltk.word_tokenize(text):
		word = word.lower()
		if word[0] not in letters:
			continue
		tf[word] += 1
	article['tf'] = tf
	df.update(tf)

for article in articles:
	tfidf = []
	for term, freq in article['tf'].items():
		score = freq / df[term]
		heapq.heappush(tfidf, (score, term))
	print(heapq.nlargest(3, tfidf))
