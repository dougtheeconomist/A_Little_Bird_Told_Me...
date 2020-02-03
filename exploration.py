#Title: all-a-twitter_cni_member_conference
#Author: Doug Hart
#Date Created: 2/3/2020
#Last Updated: 2/3/2020

import numpy as np
import pandas as pd
import plotly.graph_objects as go


#loading the data
df = pd.read_csv('data/cni_tweets.csv')

#dropping empty and non-relevant columns
df.drop('Profile Image', inplace=True, axis = 1)
df.drop('Time Zone', inplace=True, axis = 1)
df.drop('Geo', inplace=True, axis = 1)
#after looking at a random sample of the media column, have concluded not important
df.drop('Media', inplace=True, axis = 1)

'''~~~~~~~~~~~~~~~~~~~~~~~~~~~~Basic Exploration~~~~~~~~~~~~~~~~~~~~~~~~~~~~'''
df.info()
df.head()
df.describe()

#changing column names for convenience
df.rename(columns={'Universal Time Stamp': 'univ_ts', 
                   'Local Time Stamp': 'local_ts',
                  'User Mentions': 'user_mentions',
                  'Follower Count': 'follower_count'}, inplace=True)

time_trial = df['univ_ts'] == df['local_ts']
sum(time_trial)
#returns 2037, same number of rows so these are exactly the same
#can drop one without losing information
df.drop('local_ts', inplace=True, axis = 1)
'''
Reading through some tweets, fall into several categories:
    1) complete tweet
    2) partial tweet with  ...(url to full tweet)
    3) retweet denoted by RT
Steps for cleaning to address this:
    1) parse out anything starting with RT
    2) parse out anything that contains ...http
    3) at least one url that linked to an extended conversation about topic discussed at event
    row 686 of original data but found another one that is just pictures of a talks slides
    4)
'''
#language column can be sorted by 'und' to filter out tweets that are just urls
df = df[df["Language"] != 'und']
#language 'or' are just paper title with url, so probably don't need them either
df = df[df["Language"] != 'ro']
#rows 1945-1948 are spam, but not deparcated by language tag
#ID values for these rows are:
1204381864087166977
1204205653893566464
1204204698397483010
1204193158080401414
df = df[df["ID"] != 1204381864087166977]
df = df[df["ID"] != 1204205653893566464]
df = df[df["ID"] != 1204204698397483010]
df = df[df["ID"] != 1204193158080401414]
