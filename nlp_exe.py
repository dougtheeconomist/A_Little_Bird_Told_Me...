#Title: all-a-twitter_cni_member_conference
#Author: Doug Hart
#Date Created: 2/5/2020
#Last Updated: 2/6/2020
from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from scipy.optimize import nnls
from sklearn.decomposition import NMF
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.metrics import silhouette_samples, silhouette_score

import string
nltk.download('punkt')
from functions import tokenize, tidy_up, hand_label_topics
import numpy as np
import pandas as pd


df = pd.read_pickle('mct.pkl', compression='zip')

retwote = []
for i in retweet_list:
    retwote.append(cutter(i))
len(retwote)
df['retwote'] =0
for i in range(0,2037):
    count = 0
    for j in range(0,786):
        if df.username[i] == retwote[j]:
            count += 1
    df.retwote = count

#should do data selection first. i.e. all rows, exclude RTs, etc.
tidy_up(df)


'''~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~NLP Time~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'''
to_filter = ['#', ':', '!','“', '”', 't', 's', '’',';','@','&','cni19f','``','-','(', ')','.',"''",'...',',','*','%','--',"'",'https']

data = df.Text
content = data
wordnet = WordNetLemmatizer()

#V1
vectorizer = CountVectorizer(tokenizer= tokenize, stop_words='english', max_features=5000)
#V2
vectorizer = CountVectorizer(strip_accents='unicode', tokenizer= tokenize, stop_words='english', analyzer = 'word', max_features=5000)
#V3
vectorizer = CountVectorizer(strip_accents='unicode', tokenizer= tokenize, stop_words=text.ENGLISH_STOP_WORDS.union(), analyzer = 'word', max_features=5000)
#reconstruction error: 126.14881541284356

#V4 2000 Less features, a couple more stop words
vectorizer = CountVectorizer(strip_accents='unicode', tokenizer= word_tokenize, stop_words=text.ENGLISH_STOP_WORDS.union(to_filter), analyzer = 'word', max_features=3000)
#reconstruction error: 121.3807190237805

#V5 500 less feature, more stop words
vectorizer = CountVectorizer(strip_accents='unicode', tokenizer= word_tokenize, stop_words=text.ENGLISH_STOP_WORDS.union(to_filter), analyzer = 'word', max_features=2500)
#reconstruction error: 118.59462496974123

#V6 cut down to 1000 max features
vectorizer = CountVectorizer(strip_accents='unicode', tokenizer= word_tokenize, stop_words=text.ENGLISH_STOP_WORDS.union(to_filter), analyzer = 'word', max_features=1000)
#reconstruction error: 103.50973482444792

#V7 with just 500 features, getting scary
#re: 89.34899301698549

#V8 1250 features, or one per observation
#reconstruction error: 107.62346022537453

X = vectorizer.fit_transform(content)
V = X.toarray()
features = vectorizer.get_feature_names()
W = np.random.rand(data.shape[0],10)
H = np.zeros((10,5000))   

#To drop the columns with retweets 
for i in indexlist:
    df.drop(axis=0, index=i, inplace=True)

nmf = NMF(n_components=10)
W =nmf.fit_transform(V)
H = nmf.components_
nmf.inverse_transform(W)
print('reconstruction error:', nmf.reconstruction_err_)

topical = np.argsort(H, axis = 1)
topwords = topical[:, -10:]
words2 = []
for i in range(10):
    row = []
    for j in range(topwords.shape[1]):
        row.append(features[topwords[i][j]])
    words2.append(row)
words2
#this is my first carbage model. It tells me that I need to add more stopword
#as there are still a lot of punctuation/grammer words making it in. 

re =[125.46974230764488,125.46974231397594,125.46974228293287,125.46974231359194,
124.73021092995954,122.71859441059775,120.67649238366758,118.59462495454986,115.63319731909372,
111.04753081173351,103.50973482444792,89.34899301698549]
features [6000,5500,5000,4500,4000,3500,3000,2500,2000,1500,1000,500]


#beta
def get_errors(comps):
    errorlist = []
    for i in comps:
        vectorizer = TfidfVectorizer(tokenizer= word_tokenize, stop_words=text.ENGLISH_STOP_WORDS.union(to_filter),max_features=3000, strip_accents='unicode', analyzer = 'word')
        X = vectorizer.fit_transform(content)
        V = X.toarray()
        features = vectorizer.get_feature_names()
        W = np.random.rand(data.shape[0],10)
        H = np.zeros((10,5000)) 
        nmf = NMF(n_components=i)
        W =nmf.fit_transform(V)
        H = nmf.components_
        nmf.inverse_transform(W)
        errorlist.append(nmf.reconstruction_err_)
    return errorlist

#to tune max_features hyperparameter
def get_errors(list_):
    errorlist = []
    for i in list_:
        the_one = max(i,4186)
        vectorizer = CountVectorizer(strip_accents='unicode', tokenizer= word_tokenize, stop_words=text.ENGLISH_STOP_WORDS.union(to_filter), analyzer = 'word', max_features= i)
        X = vectorizer.fit_transform(content)
        V = X.toarray()
        features = vectorizer.get_feature_names()
        W = np.random.rand(data.shape[0],10)
        H = np.zeros((10,the_one)) 
        nmf = NMF(n_components=10)
        W =nmf.fit_transform(V)
        H = nmf.components_
        nmf.inverse_transform(W)
        errorlist.append(nmf.reconstruction_err_)
        print('*')
    return errorlist
    #output is basically the same as from beta version ‾\_(ツ)_/‾ 

'''~~~~~~~~~~~~~~~~~~~~~~~~~Moving forward for now~~~~~~~~~~~~~~~~~~~~~~~~~'''
#WITH 2000 max features, 10 categories
vectorizer = TfidfVectorizer(tokenizer= word_tokenize, stop_words=text.ENGLISH_STOP_WORDS.union(to_filter),max_features=2000, strip_accents='unicode', analyzer = 'word')
X = vectorizer.fit_transform(content)
V = X.toarray()
features = vectorizer.get_feature_names()
W = np.random.rand(data.shape[0],10)
H = np.zeros((10,2000)) 
V.shape  # (1128, 2000)
nmf = NMF(n_components=10)
W =nmf.fit_transform(V)
H = nmf.components_
nmf.inverse_transform(W)
print('reconstruction error:', nmf.reconstruction_err_)
#reconstruction error: 31.829236010766092

#Examples of hand labeler:
#1
hand_labels = hand_label_topics(H, vocabulary)
#then check with
rand_articles = np.random.choice(range(len(W)), 15)

for i in rand_articles:
    analyze_article(i, contents, web_urls, W, hand_labels)
#2
hand_labels = hand_label_topics(H, vocabulary)

for i in rand_articles:
    analyze_article(i, contents, web_urls, W, hand_labels)
