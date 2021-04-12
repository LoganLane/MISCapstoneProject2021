# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 09:16:49 2021

@author: Sean Owens, Logan Lane, Abby Odasso, Michael Laws
"""
import pandas_profiling
import pandas as pd
import nltk

import numpy as np
from numpy import asarray
from numpy import savetxt



import heapq


df = pd.read_csv('ProccessedData.csv')
print(df.head(30))

pandas_profiling.ProfileReport(df)

print(df.dtypes)

df['Scrubbed_Tweet'] = df['Scrubbed_Tweet'].apply(str)


print(df.dtypes)


#Replaces Misspelled words encountered after our data processing was completed.
d = {'u':'you','ur':'your','peopl':'people','ppl':'people','thi':'this','realli':'really','everi':'every','tri':'try','curri':'curry','littl':'little',
         'jesu':'jesus','crippl':'cripple','hous':'house','someon':'someone','believ':'believe','happi':'happy','jungl':'jungle','mani':'many',
         'mayb':'maybe','pleas':'please','plz':'please','whi':'why','rememb':'remember','ye':'yes','babi':'baby','gon':'gone','someth':'something',
         'caus':'cause','eveyon':'everyone','anoth':'another','aaaaaaaaaaaaaaa':'a','aa':'a','aaaa':'a','abl':'able','absolut':'absolute',
         'abolsutley':'absolute','abt':'about','abus':'abuse','accus':'accuse','achiev':'achieve','acknowledg':'acknowledge','activ':'active','administ':'administer',
         'ador':'adore','advanc':'advance','advantag':'advantage','dispos':'dispose','studi':'study','discu':'discuss','veri':'very','ga':'gas',
         'arthriti':'arthritis','faggi':'fag','gimpi':'gimpy','sinc':'since','everyon':'everyone','noth':'nothing','bc':'because',
         'countri':'country','funni':'funny','alreadi':'already','anyth':'anything','definit':'definite','theyr':'they are','deserv':'deserve','leav':'leave',
         'pretti':'pretty','forc':'force','creat':'create','becom':'become','everyth':'everything','gon':'gone','sinc':'since','pirat':'pirate',
         'countri':'country','busi':'busy','bunni':'bunny','imagin':'imagine','dirti':'dirty','ignor':'ignore','cri':'cry','r':'are','probabl':'probably',
         'nobodi':'nobody','vaccin':'vaccine','polit':'polite','sometim':'sometime','appreci':'appreciate','polic':'police','invad':'invade','cuz':'because','pictur':'picture',
         'anim':'animal','onli':'only','els':'else','whatev':'whatever','le':'less','tho':'though','futur':'future','famili':'family','illeg':'illegal'}
     

df['Scrubbed_Tweet'] = df['Scrubbed_Tweet'].apply(lambda x : ' '.join(d[word] if word in d else word for word in x.split()))


#creating our corups to be vectorized
corpus = []
for i in range(0,9406):
    tweet = df['Scrubbed_Tweet'][i]
    tweet = tweet.lower()
    tweet = tweet.split()
    tweet = ' '.join(tweet)
    corpus.append(tweet)
    

print(corpus)


wordfreq = {}
for sentence in corpus:
    tokens = nltk.word_tokenize(sentence)
    for token in tokens:
        if token not in wordfreq.keys():
            wordfreq[token] = 1
        else:
            wordfreq[token] += 1


most_freq = heapq.nlargest(200, wordfreq, key=wordfreq.get)

sentence_vectors = []
for sentence in corpus:
    sentence_tokens = nltk.word_tokenize(sentence)
    sent_vec = []
    for token in most_freq:
        if token in sentence_tokens:
            sent_vec.append(1)
        else:
            sent_vec.append(0)
    sentence_vectors.append(sent_vec)

sentence_vectors = np.asarray(sentence_vectors)

print(sentence_vectors[2])


