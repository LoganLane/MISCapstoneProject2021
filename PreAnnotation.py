# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 09:46:20 2021

@author: Sean Owens, Logan Lane, Abby Odasso, Michael Laws
"""

import pandas_profiling
import pandas as pd

df = pd.read_csv('saved_tweets4.csv', header = None)
df.rename(columns = {0: 'tweet'}, inplace = True)
df["Type"] = "false"

pandas_profiling.ProfileReport(df)

#Removal of duplicate entries in the dataset
print(df.shape)
df.drop_duplicates(inplace = True)
print(df.head(30))
print(df.shape)

df = df.sample(frac = 1)
print(df.head(30))
print(df.shape)

df.to_csv('nodupes.csv', index = False)