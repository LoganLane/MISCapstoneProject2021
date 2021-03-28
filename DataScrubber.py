# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 09:46:20 2021

@author: Owner
"""
import pandas_profiling
import pandas as pd
import unidecode

from nltk.corpus import stopwords


pd.set_option('display.max_columns', 4)
#opens dataset and creates a data frame object
df = pd.read_csv('Saved_tweets2_type_added.csv')
print(df.head(30))

pandas_profiling.ProfileReport(df)

#Removal of duplicate entries in the dataset
print(df.shape)
df.drop_duplicates(inplace = True)
print(df.head(30))
print(df.shape)

#removal of usernames
df['Scrubbed_Tweet'] = df['Tweet'].apply(lambda x: ' '.join([tweet for tweet in x.split()if not tweet.startswith("@")]))
print(df[["Scrubbed_Tweet", "Type"]].head(10))

#removal retweets
df['Scrubbed_Tweet'] = df['Tweet'].apply(lambda x: ' '.join([tweet for tweet in x.split()if not tweet.startswith("RT")]))
print(df[["Scrubbed_Tweet", "Type"]].head(10))
print(df.shape)

#removal of hashtags
df['Scrubbed_Tweet'] = df['Scrubbed_Tweet'].apply(lambda x: ' '.join([tweet for tweet in x.split()if not tweet.startswith("#")]))
print(df[["Scrubbed_Tweet","Type"]].head(10))

#removal of numbers
df['Scrubbed_Tweet'] = df['Scrubbed_Tweet'].apply(lambda x : ' '.join([tweet for tweet in x.split() if tweet.isalpha()]))
print(df[["Scrubbed_Tweet","Type"]].head(10))

#removal of greek characters
df['Scrubbed_Tweet'] = df['Scrubbed_Tweet'].apply(lambda x: ' '.join([unidecode.unidecode(tweet) for tweet in x.split()]))
print(df[["Scrubbed_Tweet","Type"]].head(10))

#removal of stopwords
df['Scrubbed_Tweet'] = df['Scrubbed_Tweet'].apply(lambda x: ' '.join([tweet for tweet in x.split() if not tweet in set(stopwords.words('English'))]))
print(df[["Scrubbed_Tweet","Type"]].head(10))
