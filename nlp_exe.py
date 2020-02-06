from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from scipy.optimize import nnls
from sklearn.decomposition import NMF
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
%matplotlib inline

df = pd.read_pickle('mct.pkl')
data = df.Text
content = data

vectorizer = CountVectorizer(stop_words='english', max_features=5000)
X = vectorizer.fit_transform(content)
V = X.toarray()
features = vectorizer.get_feature_names()
W = np.random.rand(data.shape[0],10)
H = np.zeros((10,5000))   

#To drop the columns with retweets 
for i in indexlist:
    df.drop(axis=0, index=i, inplace=True)