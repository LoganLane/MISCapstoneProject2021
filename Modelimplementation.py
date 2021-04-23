# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 09:16:49 2021

@author: Sean Owens, Logan Lane, Abby Odasso, Michael Laws
"""
import pandas_profiling
import pandas as pd
import nltk
import numpy as np
import heapq
import tensorflow as tf





df = pd.read_csv('ProccessedData.csv')
df.head(30)

pandas_profiling.ProfileReport(df)


df.dtypes

df['Scrubbed_Tweet'] = df['Scrubbed_Tweet'].apply(str)

df.dtypes


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
for i in range(0,6998):
    tweet = df['Scrubbed_Tweet'][i]
    tweet = tweet.lower()
    tweet = tweet.split()
    tweet = ' '.join(tweet)
    corpus.append(tweet)
    
#Creating a list of all words that occur in the data set and the number of occurances for each
wordfreq = {}
for sentence in corpus:
    tokens = nltk.word_tokenize(sentence)
    for token in tokens:
        if token not in wordfreq.keys():
            wordfreq[token] = 1
        else:
            wordfreq[token] += 1

#creates a list of the top 500 most common words in our dataset
most_freq = heapq.nlargest(500, wordfreq, key=wordfreq.get)


#creating vectors based on if the word occured in the most_freq list
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


# creating a new dataframe object that combines the newly vectorized data and a tpye column for our model to analyze
pf = pd.DataFrame(sentence_vectors)
pf['Type'] = df['Type']
#splitting our dataframe into two dataframes the first for training oour data and the second for testing
pf_1 = pf.iloc[:5000,:]
pf_2 = pf.iloc[5000:,:]
print(pf_1.shape)


#creating a target variable for the ML model to use for predition of outcomes
target = pf_1.pop('Type')
dataset = tf.data.Dataset.from_tensor_slices((pf_1.values,target.values))

#formats features tensor and target variable so information is grouped properly and displays the first 5 index points from data
for feat, targ in dataset.take(5):
    print ('Features: {}, target {}'.format(feat, targ))

#creates a traindataset variable to be passed to the model as well as shuffeling the data to ensure no two runs are in the same order
train_dataset = dataset.shuffle(len(pf_1)).batch(3)

#Default model creation given by tensorflow
def get_compiled_model():
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(10,activation ='relu'),
        tf.keras.layers.Dense(10, activation='relu'),
        tf.keras.layers.Dense(1)
        ])
    model.compile(optimizer='adam',
                  loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
                  metrics=['accuracy'])
    return model

#Creating model using the default model creation function get_compiled_model
model = get_compiled_model()
#Printing the epochs of the model being trained on our dataset
print(model.fit(train_dataset, epochs=10))


target = pf_2.pop('Type')
dataset = tf.data.Dataset.from_tensor_slices((pf_2.values,target.values))

for feat, targ in dataset.take(5):
    'Features: {}, target {}'.format(feat, targ)

test_dataset = dataset.shuffle(len(pf_1)).batch(3)


print(model.fit(test_dataset, epochs=1))
