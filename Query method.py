# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 18:52:35 2021

@author: Sean Owens, Logan Lane, Abby Odasso, Michael Laws
"""

from twython import Twython
import csv
import json


with open("twitter_credentials.json", "r") as file:
    creds = json.load(file)   
    
twitter = Twython(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'], creds['ACCESS_TOKEN'], creds['ACCESS_SECRET'])
    
results = twitter.search(q= 'hate -filter:retweets', tweet_mode ='extended', count= 100, lang= 'en')

all_tweets = results['statuses']

for tweet in all_tweets:
   
    with open(r'saved_tweets4.csv', 'a',encoding = 'utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(list([tweet['full_text']]))
        
 