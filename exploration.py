#Title: CNI on twitter eda/cleaning
#Author: Doug Hart
#Date Created: 2/3/2020
#Last Updated: 2/10/2020

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
#Step 1)
#turns out I needed to do this before removing rows
indexlist = []
for i in range(0, 2037):
    if (df['Text'][i][0:2]) == 'RT':
        indexlist.append(i)
    else:
        pass
len(indexlist)  #786



#786 retweets
786/2002   # =0.3926
#Tells us that 39% of our relevant tweets are retweets

#Step2: isolating incomplete tweets
indexlist2 = []
for i in range(0, 2037):
    if '… https://t.co' in (df['Text'][i]):
        indexlist2.append(i)
    else:
        pass
len(indexlist2) #589
589/2002  #0.2942

#checking if these indices overlap
cut_RT = []
for num in indexlist:
    if num in indexlist2:
        cut_RT.append(num)
cut_RT  # empty, no overlap! Makes things easier

#Extracting urls to scrape:
scrapelist = []
for i in indexlist2:
    splitlist = df['Text'][i].split()
    count =0
    while count < 1:
        check = splitlist.pop()
        if 'https://t.co/' in check:
            scrapelist.append(check)
            count += 1
        else:
            continue
'''SEE tweet_scraping.py FOR NEXT INTERMEDIATE STEPS'''
#importing scraped data back in to replace partials
with open('data/fulltweet_list.txt', 'r') as scraped:
    primelist = json.load(scraped)

mergedf =pd.DataFrame(data = primelist, index = indexlist2)
#here are the indexes to merge on
df.Text.iloc[indexlist2[400]]
mergedf.iloc[400]

for i in range(0, len(indexlist2):
    df.replace(to_replace= df.Text.iloc[indexlist2[i]], value= mergedf.iloc[i])
#saved this to csv, complete_tweets

flag1 = 'After nearly a year of work and many conversations I am proud to release:Responsible Operations'
df.drop('flag', axis=1)
df['flag'] = 0
for i in range(2037):
    if flag1 in df.Text[i]:
        df.flag[i] = 1
sum(df.flag)  #= 192
# or 114? after updating with whole tweets, this decreased, what happened

#to track tweets BY CNI(all 18 of them)
cni_indexlist = []
for i in range(0, 2037):
    if (df['Name'][i] == 'CNI'):
        cni_indexlist.append(i)
    else:
        pass

#language column can be sorted by 'und' to filter out tweets that are just urls
#Step 3)

# OR
morespam = []
for i in range(0,len(df.Language)):
    if df.Language[i] == 'und':
        morespam.append(i)
for i in range(0,len(df.Language)):
    if df.Language == 'ro':
        morespam.append(i)
#language 'or' are just paper title with url, so probably don't need them either

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
df.drop(axis = 0, index= )
spamlist =[1943, 1944, 1945, 1946]
for i in spamlist:
    df.drop(axis=0, index=i, inplace=True)
#dropping empty and non-relevant columns
df.drop('Profile Image', inplace=True, axis = 1)
df.drop('Time Zone', inplace=True, axis = 1)
df.drop('Geo', inplace=True, axis = 1)
#after looking at a random sample of the media column, have concluded not important
df.drop('Media', inplace=True, axis = 1)

#Identifying tweets by CNI
cnilist = []
for i in range(0,2037):
    if df.username[i] == 'cni_org':
        cnilist.append(i)
cnilist

#finding number of unique tweeters within data
handles = set(df.username)
len(handles)  #653
handles_ = [item for item in handles]
len(handles_)
n_rts = []
#finding average number of followers
df.groupby('username').mean().follower_count.mean()

for i in range(0,653):
    count = 0
    for j in range(0,786):
        if handles_[i] == retwote[j]:
            count += 1
    n_rts.append(count)
for i in range(653):
print('{}, {}rts'.format(handles_[i],n_rts[i]))
#cni is number 410 with 25 retweets

#seperating date from time information
df['date'] = None
df['time'] = None

for i in range(0,2037):
    df.date[i] = df.uts[i][0:10]
    df.time[i] = df.uts[i][10:-1]
    if i%100 ==0:
        print(i)

#top words of whole doc, I believe 
'''
{'Topic # 01': ['lynch',
  'cliff',
  'science',
  'data',
  '?',
  'computing',
  'research',
  'quantum',
  'need',
  'today',
  'encrypted',
  'archiving',
  'flows',
  'encryption',
  'internet',
  'right',
  'notes',
  'agencies/institutions',
  'decrypt',
  'fiction']}
  '''
  
  #finding connections via mentions
new = [item for item in df.user_mentions]
ilist = [num for num in range(0,2037)]
ilist.reverse()
for i in ilist:
    if type(new[i]) == float:
        new.pop(i)
len(new)  #1498
mention = []
for i in range(0, 1498):
    for j in new[i].split(' '):
        mention.append(j)
len(mention)  #2158 number of different mentions
mentions = set(mention)
len(mentions) #224 number of twitter users mentioned
mlist = list(mentions)

mcount = [0 for num in range(0, 653)]
handle = list(handles)
for i in range(0, 653):
    for j in range(0, len(mention)):
        if handle[i] == mention[j]:
            mcount[i] += 1
#total number of times user within data was mentioned
sum(mcount)  #1864
#average of these mentions per user
sum(mcount) / 653  #2.9
#to find out how many of these were cni, want to subtract those
for i in range(0, 653):
    if handle[i] == 'cni_org':
        print(i)   #  410
#also should subtract ThomasGPadilla, as this is likely spam
print(mcount[410])  #113
real_count = 1864 - 113 -223  # 1528
#real answer is . . . 
1528 / 651 = 2.4
#This still rounds to 3

#dealing with location data
#weeding out missing data
cleaner_loc = []
for i in df.index:
    if type(df.Location[i]) == str:
        cleaner_loc.append(re.findall(r'\w+', df.Location[i], re.IGNORECASE))
    else:
        pass
#then narrowing down to just two words, 
# anything else is probably a description or pun
countlist = [num for num in range(0, 907)]
countlist.reverse()

for i in countlist:
    if len(cleaner_loc[i]) != 2:
        cleaner_loc.pop(i)
len(cleaner_loc)  # = 409
#then isolating states with state abreviation
stateloc = []
otherloc = []
for i in range(0,409):
    if len(cleaner_loc[i][1]) == 2:
        stateloc.append(cleaner_loc[i])
    else:
        otherloc.append(cleaner_loc[i])
len(otherloc)  # = 189
len(stateloc)  # = 220

stateloc.append(['Toledo', 'OH'])
stateloc.append(['Cleveland', 'OH'])

#otherloc boils down to:
otherloc2 = [['London', 'England'],
 ['Vancouver', 'Canada'],
 ['Dublin', 'Ireland'],
 ['Delft', 'Nederland'],
 ['Barcelona', 'Catalonia'],
 ['Helsinki', 'Finland'],
 ['Lausanne', 'Suisse'],
 ['london', 'ontario'],
 ['Sydney', 'Australia'],
 ['Livingston', 'Scotland'],
 ['Wien', 'Österreich'],
 ['Cambridge', 'England'],
 ['Vienna', 'Austria'],
 ['Linz', 'Austria']]

 ulist = [['Columbia', 'University']]


#to get city coordinate data
dfgeo = pd.read_csv('uscities.csv')
citylist2 = []
for i in range(0, len(dfgeo.city)):
    citylist2.append((dfgeo.city[i] + ', ' + dfgeo.state_id[i]))
