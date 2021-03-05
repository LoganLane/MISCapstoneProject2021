# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 18:52:35 2021

@author: Owner
"""

from twython import Twython
import csv
import json


with open("twitter_credentials.json", "r") as file:
    creds = json.load(file)   
    
twitter = Twython(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'], creds['ACCESS_TOKEN'], creds['ACCESS_SECRET'])
    
results = {'q': 'hate -filter:retweets', 'tweet_mode':'extended', 'count': 100, 'lang': 'en'}

string_ = {'text': []}
for status in twitter.search(**results)['statuses']:
    string_['text'].append(status['text'])
    with open(r'saved_tweets4.csv', 'a',encoding = 'utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(list([string_['text']]))
        
 