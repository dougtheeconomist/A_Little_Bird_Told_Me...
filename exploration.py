#Title: all-a-twitter_cni_member_conference
#Author: Doug Hart
#Date Created: 2/3/2020
#Last Updated: 2/3/2020

import numpy as np
import pandas as pd
import plotly.graph_objects as go


#loading the data
df = pd.read_csv('data/cni_tweets.csv')

'''~~~~~~~~~~~~~~~~~~~~~~~~~~~~Basic Exploration~~~~~~~~~~~~~~~~~~~~~~~~~~~~'''
df.info()
df.head()
df.describe()
