# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 15:08:04 2021

@author: Sean Owens
"""

from twython import TwythonStreamer
import csv
import json
import re
import emoji

#Opening a json file to get user credentials for Twitter API access and saving that information into a variable for later use 
with open("twitter_credentials.json", "r") as file:
    creds = json.load(file)   

#Pulls only the infromation in the Tweets we need
#In our case we are pulling just the users handle and tweet content
def process_tweet(tweet):
    d = {}
    d['text'] = tweet['text']
    d['text'] = deEmojify(d['text'])
    
    return d

def give_emoji_free_text(self, text):
    allchars = [str for str in text]
    emoji_list = [c for c in allchars if c in emoji.UNICODE_EMOJI]
    clean_text = ' '.join([str for str in text.split() if not any(i in str for i in emoji_list)])

    return clean_text

def deEmojify(text):
        regrex_pattern = re.compile(pattern = "["
           
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U0001F1F2-\U0001F1F4"  # Macau flag
        u"\U0001F1E6-\U0001F1FF"  # flags
        u"\U0001F600-\U0001F64F"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f904-\U0001f942"
        u"\u0101"
        u"\U0001F1F2"
        u"\U0001F1F4"
        u"\U0001F620"
        u"\u200d"
        u"\u2640-\u2642"
                           "]+", flags = re.UNICODE)
        return regrex_pattern.sub(r'',text)

#Creating the streaming object that will collect the information from Twitter
class MyStreamer(TwythonStreamer):
    
    #Only allows for english Tweets and saves them into a CSV file
    def on_success(self, data):
        if data['lang'] == 'en':
            tweet_data = process_tweet(data)
            self.save_to_csv(tweet_data)
     
    #If an error occurs this will disconnect from the API        
    def on_error(self, status_code, data):
        print(status_code, data)
        self.disconnect()
    
    #Will be used to write the information into our CSV 
    def save_to_csv(self, tweet):
        with open(r'saved_tweets.csv', 'a') as file:
            writer = csv.writer(file)
            writer.writerow(list(tweet.values()))

#Pulls our credentials from the json file            
stream = MyStreamer(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'],
                    creds['ACCESS_TOKEN'], creds['ACCESS_SECRET'])

#Filtering for keywords in our tweet search
stream.statuses.filter(track='china, virus, muslim, women')
