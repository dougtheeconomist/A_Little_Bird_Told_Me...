#Title: all-a-twitter_cni_member_conference
#Author: Doug Hart
#Date Created: 2/5/2020
#Last Updated: 2/6/2020
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from scipy.optimize import nnls
from sklearn.decomposition import NMF
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
import string
nltk.download('punkt')
from functions.py import tokenize, tidy_up
import numpy as np
import pandas as pd


df = pd.read_pickle('mct.pkl', compression='zip')

#should do data selection first. i.e. all rows, exclude RTs, etc.
tidy_up(df)


'''~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~NLP Time~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'''

data = df.Text
content = data
wordnet = WordNetLemmatizer()
def tokenize(doc):
    '''
    INPUT: string
    OUTPUT: list of strings

    Tokenize and stem/lemmatize the document.
    '''
    return [wordnet.lemmatize(word) for word in word_tokenize(doc.lower())]

#V1
vectorizer = CountVectorizer(tokenizer= tokenize, stop_words='english', max_features=5000)
#V2
vectorizer = CountVectorizer(strip_accents='unicode', tokenizer= tokenize, stop_words='english', analyzer = 'word', max_features=5000)
#V3
vectorizer = CountVectorizer(strip_accents='unicode', tokenizer= tokenize, stop_words=text.ENGLISH_STOP_WORDS.union(), analyzer = 'word', max_features=5000)
text.ENGLISH_STOP_WORDS.union(my_additional_stop_words)
#V4
vectorizer = TfidfVectorizer()
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
to_filter = ['#', ':', '!','“', '”', 't', 's', '’',';','@','&','cni19f','``','-','(', ')']]
