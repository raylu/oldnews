#!/usr/bin/env python3

import html
from html.parser import HTMLParser
import json
from pprint import pprint
import re
from xml.etree import ElementTree

import requests
import yaml

def main():
	get_articles()

def get_articles():
	# http://api.nytimes.com/svc/news/v3/content/all/all.json?api-key=2f404f0c9e908329819e1930607e8131:0:72037309
	with open('nyt.json') as f:
		content = json.load(f)
	articles = content['results']
	output = []
	for article in articles:
		url = article['url']
		if 'http://www.nytimes.com/' not in url:
			continue
		output.append({
			'title': html.unescape(article['title']).strip(),
			'abstract': html.unescape(article['abstract']).strip(),
			'url': url,
			'content': parse_html(url),
		})
	with open('articles.yaml', 'w') as f:
		yaml.dump(output, f, default_flow_style=False)

rs = requests.Session()
def parse_html(url):
	url = url.replace('http://www.nytimes.com/', 'http://mobile.nytimes.com/')
	# set Referer to get NYT-S cookie
	response = rs.get(url, headers={'Referer': 'https://www.google.com/'})
	ce = ContentExtractor()
	ce.feed(response.text)
	text = '\n'.join(ce.text)
	return text

class ContentExtractor(HTMLParser):
	def __init__(self):
		super().__init__()
		self.include = False
		self.text = []

	def handle_starttag(self, tag, attrs):
		if tag != 'p' or not attrs:
			return
		attr = attrs[0]
		if attr[0] == 'class' and 'p-block' in attr[1].split():
			self.include = True

	def handle_data(self, data):
		if self.include:
			self.text.append(data)

	def handle_endtag(self, tag):
		if tag == 'p':
			self.include = False

if __name__ == '__main__':
	main()
