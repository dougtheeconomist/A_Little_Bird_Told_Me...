def tokenize(doc):
    '''
    INPUT: string
    OUTPUT: list of strings

    Tokenize and stem/lemmatize the document.
    '''
    return [wordnet.lemmatize(word) for word in word_tokenize(doc.lower()) if word.isalpha()]

def tidy_up(df):
    df.drop('Profile Image', inplace=True, axis = 1)
    df.drop('Time Zone', inplace=True, axis = 1)
    df.drop('Geo', inplace=True, axis = 1)
    #after looking at a random sample of the media column, have concluded not important
    df.drop('Media', inplace=True, axis = 1)
    df.rename(columns={'Universal Time Stamp': 'univ_ts', 
                    'Local Time Stamp': 'local_ts',
                    'User Mentions': 'user_mentions',
                    'Follower Count': 'follower_count'}, inplace=True)

    indexlist = []
    for i in range(0, 2037):
        if (df['Text'][i][0:2]) == 'RT':
            indexlist.append(i)
        else:
            pass
    len(indexlist)  #786
    for i in indexlist:
        df.drop(axis=0, index=i, inplace=True)
    spamlist =[1943, 1944, 1945, 1946]
    for i in spamlist:
        df.drop(axis=0, index=i, inplace=True)
