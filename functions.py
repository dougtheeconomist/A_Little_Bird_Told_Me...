#Title: CNI analysis functions
#Author: Doug Hart
#Date Created: 2/6/2020
#Last Updated: 2/8/2020

import numpy as np

def tokenize(doc):
    '''
    INPUT: string
    OUTPUT: list of strings

    Tokenize and stem/lemmatize the document.
    '''
    return [wordnet.lemmatize(word) for word in word_tokenize(doc.lower()) if word.isalpha()]

'''~~~~~~~~~~~~~~~~~~~~~~analysis_prep_function~~~~~~~~~~~~~~~~~~~~~~'''

def tidy_up(df):
    '''to drop columns, rows that aren't needed or that contain non'relevant data'''
    df.drop('Profile Image', inplace=True, axis = 1)
    df.drop('Time Zone', inplace=True, axis = 1)
    df.drop('Geo', inplace=True, axis = 1)
    df.drop('Local Time Stamp', inplace=True, axis = 1)
    #after looking at a random sample of the media column, have concluded not important
    df.drop('Media', inplace=True, axis = 1)
    df.rename(columns={'Universal Time Stamp': 'uts', 
                    'User Mentions': 'user_mentions',
                    'Follower Count': 'follower_count',
                    'User Name': 'username'}, inplace=True)

    indexlist = []
    for i in range(0, 2037):
        if (df['Text'][i][0:2]) == 'RT':
            indexlist.append(i)
        else:
            pass
    len(indexlist)  #786
    # for i in indexlist:
    #     df.drop(axis=0, index=i, inplace=True)
   
    morespam = []
    for i in range(0,len(df.Language)):
        if df.Language[i] == 'und':
            morespam.append(i)
    for i in range(0,len(df.Language)):
        if df.Language[i] == 'ro':
            morespam.append(i)

    maybespam = []
    for i in range(0,2037):
        if 'After nearly a year of work and many conversations I am proud to release' in df.Text[i]:
            maybespam.append(i)
     #contains spam and tweets by cni
    droplist =[0,4,14,15,16,42,48,417,1139,1161,1338,1537,1579,1801,1802,1898,1940,
    1943, 1944, 1945, 1946,1973,2008,2020,2027]
    droplist.extend(morespam)
    droplist.extend(maybespam)
    droplist.extend(indexlist)
    droplist.sort()
    dropset = set(droplist)

    for i in dropset:
        df.drop(axis=0, index=i, inplace=True)

'''~~~~~~~~~~~~~~~~~~~~~~~~end_prep_function~~~~~~~~~~~~~~~~~~~~~~~~'''

#From the internet; finding topwords in categories from nmf

def get_nmf_topics(model, n_top_words=10, num_topics=10):
    
    #the word ids obtained need to be reverse-mapped to the words so we can print the topic names.
    features = vectorizer.get_feature_names()
    
    word_dict = {}
    for i in range(num_topics):
        
        #for each topic, obtain the largest values, and add the words they map to into the dictionary.
        words_ids = model.components_[i].argsort()[:-20 - 1:-1]
        # words = [feat_names[key] for key in words_ids]
        words = [features[key] for key in words_ids]
        word_dict['Topic # ' + '{:02d}'.format(i+1)] = words
    
    return pd.DataFrame(word_dict)

# to call; get_nmf_topics(model, 20)

def run_it(data, feat, groups):
    '''Beta version, not sure what in all to return'''
    data_ = data
    content = data
    wordnet = WordNetLemmatizer()

    vectorizer = CountVectorizer(strip_accents='unicode', tokenizer= word_tokenize, stop_words=text.ENGLISH_STOP_WORDS.union(to_filter), analyzer = 'word', max_features= feat)
    X = vectorizer.fit_transform(content)
    V = X.toarray()
    features = vectorizer.get_feature_names()
    W = np.random.rand(data.shape[0],groups)
    H = np.zeros((groups,feat)) 
    nmf = NMF(n_components=groups)
    W =nmf.fit_transform(V)
    H = nmf.components_
    nmf.inverse_transform(W)
    print('reconstruction error:', nmf.reconstruction_err_)
    return V, H, W

def cutter(tweet):
    '''to cut origin handle out of retweets
    to match retweet to origin'''
    marker = None
    for i in range(0, len(tweet)):
        if tweet[i] ==':':
            marker = i
            break
        else:
            continue
    out = tweet[4:]
    return out


def phrase_counter(column,phrase):
    '''Returns the count of rows that contain the string denoted as 
    phrase found within the specified column of data

    column: iterable, column from dataframe or list

    phrase: string, as part of larger string in row of column
    '''
    count = 0
    for i in range(0,len(column)):
        if phrase in column[i].lower():
            count += 1
    return count

#from assignment

def hand_label_topics(H, vocabulary):
    import numpy as np
    '''
    Print the most influential words of each latent topic, and prompt the user
    to label each topic. The user should use their humanness to figure out what
    each latent topic is capturing.
    '''
    hand_labels = []
    for i, row in enumerate(H):
        top_five = np.argsort(row)[::-1][:20]
        print('topic', i)
        print('-->', ' '.join(vocabulary[top_five]))
        label = input('please label this topic: ')
        hand_labels.append(label)
        print()
    return hand_labels

def softmax(v, temperature=1.0):
    import numpy as np
    '''
    A heuristic to convert arbitrary positive values into probabilities.
    See: https://en.wikipedia.org/wiki/Softmax_function
    '''
    expv = np.exp(v / temperature)
    s = np.sum(expv)
    return expv / s

def classify_text(tweet_index, contents, W, hand_labels):
    '''
    Print an analysis of a tweet, including the body of the tweet
    and a summary of which topics it represents. The topics are identified
    via the hand-labels which were assigned by the user.
    '''
    print(tweet_index)
    print(contents[tweet_index])
    probs = softmax(W[tweet_index], temperature=0.01)
    for prob, label in zip(probs, hand_labels):
        print('--> {:.2f}% {}'.format(prob * 100, label))
    print()

# classify_text(0,df.Text, W, labels)

def assign_categories(W, df):
    df.reset_index(inplace=True)
    df.rename(columns={'index': 'or_index'}, inplace=True)
    df['digital_preservation'] = 0
    df['conference_attendance_barriers'] = 0
    df['qc_encryption'] = 0
    df['ds_library_diversity'] = 0
    df['training_researchers'] = 0
    for i in df.index:
        prob = (softmax(W[i], temperature=0.01))
        df.digital_preservation[i] = prob[0]*100
        df.conference_attendance_barriers[i] = prob[1]*100
        df.qc_encryption[i] = prob[2]*100
        df.ds_library_diversity[i] = prob[3]*100
        df.training_researchers[i] = prob[4]*100
    
    return (df['digital_preservation'], df['conference_attendance_barriers'], 
    df['qc_encryption'], df['ds_library_diversity'],df['training_researchers']
    )

def prob_counter(column,threshold):
    count = 0
    for i in df.index:
        if column[i] >= threshold:
            count += 1
    return count

#from the net
def get_sentiment(tweet): 
        ''' 
        Utility function to classify sentiment of passed tweet 
        using textblob's sentiment method 
        '''
        # create TextBlob object of passed tweet text 
        analysis = TextBlob(tweet) 
        # set sentiment 
        if analysis.sentiment.polarity > 0: 
            return 'positive'
        elif analysis.sentiment.polarity == 0: 
            return 'neutral'
        else: 
            return 'negative'

#to get lattidute, longitude data from city, state
def getlatlon(statelisting):
    lat = None
    lon = None
    ind = None
    
    if statelisting in citylist2:
        ind= citylist2.index(statelisting)
    else:
        return None, None 
    
    lat = dfgeo.lat[ind]
    lon = dfgeo.lng[ind]
    return lat, lon

#to generate plotly location graph, will need to edit
def getgraph(lat, lon):
    fig = go.Figure(data=go.Scattergeo(
        lon = lon,
        lat = lat
#         text = Locations of UFO sightings,
        mode = 'markers',
        marker_color = 'greens',
        ))

    fig.update_layout(
        title = 'Locations of Conference Attendees on Twitter',
        geo_scope='usa',
    )
    fig.show()