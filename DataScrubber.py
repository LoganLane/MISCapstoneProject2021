# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 09:46:20 2021

@author: Sean Owens, Logan Lane, Abby Odasso, Michael Laws
"""
import pandas_profiling
import pandas as pd
import nltk
import unidecode

from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer 
from nltk.corpus import stopwords


pd.set_option('display.max_columns', 4)
#opens dataset and creates a data frame object
df = pd.read_csv('AnnotatedData.csv')
print(df.head(30))

pandas_profiling.ProfileReport(df)

#Removal of duplicate entries in the dataset
print(df.shape)
df.drop_duplicates(inplace = True)
print(df.head(30))
print(df.shape)

#removal of usernames
df['Scrubbed_Tweet'] = df['tweet'].apply(lambda x: ' '.join([tweet for tweet in x.split()if not tweet.startswith("@")]))
print(df[["Scrubbed_Tweet", "Type"]].head(10))

#removal of retweets
df['Scrubbed_Tweet'] = df['Scrubbed_Tweet'].apply(lambda x: ' '.join([tweet for tweet in x.split()if not tweet.startswith("RT")]))
print(df[["Scrubbed_Tweet", "Type"]].head(10))
print(df.shape)

#removal of hyperlinks
df['Scrubbed_Tweet'] = df['Scrubbed_Tweet'].apply(lambda x: ' '.join([tweet for tweet in x.split()if not tweet.startswith("http")]))
print(df[["Scrubbed_Tweet", "Type"]].head(10))
print(df.shape)

#removal of hashtags
df['Scrubbed_Tweet'] = df['Scrubbed_Tweet'].apply(lambda x: ' '.join([tweet for tweet in x.split()if not tweet.startswith("#")]))
print(df[["Scrubbed_Tweet","Type"]].head(10))

#removal of monetary signs and user namess starting with a $. $ is used for usernames on other sites and applications
df['Scrubbed_Tweet'] = df['Scrubbed_Tweet'].apply(lambda x: ' '.join([tweet for tweet in x.split()if not tweet.startswith("$")]))
print(df[["Scrubbed_Tweet","Type"]].head(10))

#removal of Emoji from tweets
df['Scrubbed_Tweet'] = df['Scrubbed_Tweet'].str.replace(r'[^\x00-\x7F]+', '', regex=True)
print(df[["Scrubbed_Tweet","Type"]].head(30))

#removal of numbers
df['Scrubbed_Tweet'] = df['Scrubbed_Tweet'].apply(lambda x : ' '.join([tweet for tweet in x.split() if tweet.isalpha()]))
print(df[["Scrubbed_Tweet","Type"]].head(10))

#removal of greek characters
df['Scrubbed_Tweet'] = df['Scrubbed_Tweet'].apply(lambda x: ' '.join([unidecode.unidecode(tweet) for tweet in x.split()]))
print(df[["Scrubbed_Tweet","Type"]].head(10))

#removal of stopwords
df['Scrubbed_Tweet'] = df['Scrubbed_Tweet'].apply(lambda x: ' '.join([word for word in x.split() if not word in set(stopwords.words('English'))]))
print(df[["Scrubbed_Tweet","Type"]].head(10))

#Lemmatizes the tweets to reduce words to their root
lemmatizer = WordNetLemmatizer()
df['Scrubbed_Tweet'] = df['Scrubbed_Tweet'].apply(lambda x : ' '.join([lemmatizer.lemmatize(word) for word in x.split()]))
print(df[["Scrubbed_Tweet","Type"]].head(10))


ps = PorterStemmer()
df['Scrubbed_Tweet'] = df['Scrubbed_Tweet'].apply(lambda x : ' '.join([ps.stem(word) for word in x.split()]))
print(df[["Scrubbed_Tweet","Type"]].head(10))

#dropping tweet column from data frame and saving to a new csv
del df['tweet']
df.to_csv('ProccessedData.csv', index = False)

