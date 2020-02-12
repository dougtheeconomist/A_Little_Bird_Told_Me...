#Title: all-a-twitter_cni_member_conference
#Author: Doug Hart
#Date Created: 2/5/2020
#Last Updated: 2/11/2020
from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from scipy.optimize import nnls
from sklearn.decomposition import NMF
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer

from textblob import TextBlob 

import string
from functions import tokenize, tidy_up, hand_label_topics
import numpy as np
import pandas as pd

from functions import (tokenize, tidy_up, hand_label_topics,
get_nmf_topics, phrase_counter, classify_text, softmax)
from wordcloud import WordCloud, STOPWORDS 
import matplotlib.pyplot as plt
%matplotlib inline

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
#this is my first garbage model. It tells me that I need to add more stopword
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
        proportion =1- (np.count_nonzero(W)/W.size)
        proplist.append(proportion)
        errorlist.append(nmf.reconstruction_err_)
        print('*')
    return errorlist
    #output is basically the same as from beta version ‾\_(ツ)_/‾ 

'''~~~~~~~~~~~~~~~~~~~~~~~~~Moving forward for now~~~~~~~~~~~~~~~~~~~~~~~~~'''
#WITH 2000 max features, 5 categories
vectorizer = TfidfVectorizer(tokenizer= word_tokenize, stop_words=text.ENGLISH_STOP_WORDS.union(to_filter),max_features=2000, strip_accents='unicode', analyzer = 'word')
X = vectorizer.fit_transform(content)
V = X.toarray()
features = vectorizer.get_feature_names()
W = np.random.rand(data.shape[0],5)
H = np.zeros((5,2000)) 
V.shape  # (1128, 2000)
nmf = NMF(n_components=5)
W =nmf.fit_transform(V)
H = nmf.components_
nmf.inverse_transform(W)
print('reconstruction error:', nmf.reconstruction_err_)
#reconstruction error: 32.450515841580675
# proportion: 0.4136888888888889
# overlap: 2.4


#utilizing hand_lebel_topics function:
my_topic_labels = ['Digital preservation',
 'Barriers to attendance livestreaming',
 'Quantum computings threat to encryption',
 'Data_science, libraries and diversity problem',
 'Training successful scholarly researchers']
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


#After final model and hand labels applied
classify_text(0,df.Text, W, labels)

assign_categories(W, df)
#finding breakdown of categories
prob_counter(df.digital_preservation,10)
prob_counter(df.conference_attendance_barriers,10)
prob_counter(df.qc_encryption,10)
prob_counter(df.ds_library_diversity,10)
prob_counter(df.training_researchers,10)
560+181+148+534+462 #=1885
#dividing to get percentage of tweets in each category
# 29.71%
# 9.6%
# 7.85%
# 28.33%
# 24.51%
#adds up to 99.95%

#now averaging with figures found by just looking at highest % 
#for each row
count1 = 0
count2 = 0
count3 = 0
count4 = 0
count5 = 0
for i in df.index:
    b = max(df.digital_preservation[i],df.conference_attendance_barriers[i],df.qc_encryption[i],df.ds_library_diversity[i],df.training_researchers[i])
    if df.digital_preservation[i] == b:
        count1 +=1
    if df.conference_attendance_barriers[i] == b:
        count2 +=1
    if df.qc_encryption[i] == b:
        count3 +=1
    if df.ds_library_diversity[i] ==b:
        count4 +=1
    if df.training_researchers[i] ==b:
        count5 +=1
#comes to 102.48%, becuase of ties


(0.29708222811671087+0.3502222222222222) / 2  #= 32.37%
(0.0960212201591512+0.064) / 2 #=8%
(0.07851458885941645+0.03911111111111111) / 2  #= 5.88%
(0.28328912466843503+0.3031111111111111) / 2  #= 29.32%
(0.24509283819628647+0.26844444444444443) / 2  #= 25.68%
#adds up to 101.24%



#Graphing histograms of categories
fig, axs=plt.subplots(2,3, figsize = (15, 10))
ax = axs[0,0]
dp=ax.hist(df.digital_preservation)
ax.set_xlabel('Probabilities',fontsize = 18)
ax.set_ylabel('tweets',fontsize = 18)
ax.set_title('Digital Preservation',fontsize = 22, pad = 8)

ax = axs[0,1]
cab=ax.hist(df.conference_attendance_barriers)
ax.set_xlabel('Probabilities',fontsize = 18)
ax.set_ylabel('tweets',fontsize = 18)
ax.set_title('Conference Attendance',fontsize = 22, pad = 8)

ax = axs[1,0]
qc=ax.hist(df.qc_encryption)
ax.set_xlabel('Probabilities',fontsize = 18)
ax.set_ylabel('tweets',fontsize = 18)
ax.set_title('QC & Encryption',fontsize = 22, pad = 8)

ax = axs[1,1]
div=ax.hist(df.ds_library_diversity)
ax.set_xlabel('Probabilities',fontsize = 18)
ax.set_ylabel('tweets',fontsize = 18)
ax.set_title('DS, Libraries, & Diversity',fontsize = 22, pad = 8)

ax = axs[1,2]
tr=ax.hist(df.training_researchers)
ax.set_xlabel('Probabilities',fontsize = 18)
ax.set_ylabel('tweets',fontsize = 18)
ax.set_title('Training Researchers',fontsize = 22, pad = 8)
plt.tight_layout()

'''~~~~~~~~~~~~~~~~~~~~~~~Sentiment Analysis~~~~~~~~~~~~~~~~~~~~~~~'''

df['positive'] = 0
df['negative'] = 0
df['neutral'] = 0

for i in df.index:
    if get_sentiment(df.Text[i]) == 'positive':
        df.positive[i] = 1
    if get_sentiment(df.Text[i]) == 'negative':
        df.negative[i] = 1
    if get_sentiment(df.Text[i]) == 'neutral':
        df.neutral[i] = 1

sum(df.positive)  #=573
#50.9% positive
sum(df.negative)  #=160
#14.22% negative
sum(df.neutral)  #=392
#34.84% neutral

#creating column of polarities, may contain some None values still
df['sentiment_polarity'] = None
for i in df.index:
    analysis = TextBlob(df.Text[i])
    df.sentiment_polarity[i] = analysis.sentiment.polarity

np.mean(df.sentiment_polarity)  # = 0.1124532
#max is 1, min is -1


#Now to repeat with retweets included
np.mean(df.sentiment_polarity)  # = .10398576

um(df.positive)  #=902
#50.42% positive
sum(df.negative)  #=271
#15.15% negative
sum(df.neutral)  #=616
#34.43% neutral

finding sentiment mean for just negatives
scount =0
for i in df.index:
    if df.negative[i]:
        scount += df.sentiment_polarity[i]
scount / 160
'''~~~~~~~~~~combining sentiment with topic modeling results~~~~~~~~~~'''

df['topicnum'] = 0
for i in df.index:
    b = max(df.digital_preservation[i],df.conference_attendance_barriers[i],df.qc_encryption[i],df.ds_library_diversity[i],df.training_researchers[i])
    if df.digital_preservation[i] == b:
        df.topicnum[i] =1
    if df.conference_attendance_barriers[i] == b:
        df.topicnum[i] =2
    if df.qc_encryption[i] == b:
        df.topicnum[i] =3
    if df.ds_library_diversity[i] ==b:
        df.topicnum[i] =4
    if df.training_researchers[i] ==b:
        df.topicnum[i] =5

df.groupby('topicnum').sum()

#cat1
# positive 199, 51.55%
# negative 43, 11.14%
# neutral 144, 37.31%

#cat2
# positive 27, 41.54%
# negative 16, 24.62%
# neutral 22, 33.85%

#cat3
# positive 33, 86.84%
# negative 2, 5.26%
# neutral 3, 7.9%

#cat4
# positive 192, 57.48%
# negative 47, 14.07%
# neutral 95, 28.44%

#cat5
# positive 122, 40.4%
# negative 52, 17.22%
# neutral 128, 42.38%
