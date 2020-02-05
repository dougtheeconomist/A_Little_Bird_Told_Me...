#Title: tweet scraping
#Author: Doug Hart
#Date Created: 2/4/2020
#Last Updated: 2/4/2020

from pymongo import MongoClient
client = MongoClient()

import json # to work with json file format
from bs4 import BeautifulSoup
import pprint
import requests
import re

with open('data/url_list.txt', 'r') as scraper:
    scrapelist = json.load(scraper)
len(scrapelist)  

'''~~~~~~~~~~~~~~~~~~~~~~~~~~~To Scrape html block~~~~~~~~~~~~~~~~~~~~~~~~~~~'''
db = client.tweets

pages = db.pages3
for i, item in enumerate(scrapelist):

    r = requests.get(item)
    pages.insert_one({'html': r.content})
#To confirm correct number of documents
pages.count_documents({})  #if this doesn't match len(scrapelist), issues
#Both are 589
'''~~~~~~~~~~~~~~~~~isolating, saving text from block to list~~~~~~~~~~~~~~~~~'''
#isolating tweet with hashtag info from last page
soup.find_all('title')[0].text
#OR
soup.find("title").text
'''
the thing that lagged me down was 
list(pages.find({}))
'''

huge_thing = list(pages.find({}))
tweetlist = []
for i in range(0, len(huge_thing)):
    if i == 33:
        pass
    else:
        soup2 = BeautifulSoup(huge_thing[i]['html'])
        tweetlist.append(soup2.find("title").text)

len(tweetlist)  #588 because one didn't run properly

tlinex32 ='Cliff Lynch talking about many manifestations of balkanization that are happening. One is that the urban/rural broadband divide is getting worse not better - consequences for access to medical services, employment #cni19f'
#to clip twitter handles from beginning of string
def clipper(tweet):
    marker = None
    for i in range(0, len(tweet)):
        if tweet[i] =='"':
            marker = i
            break
        else:
            continue
    out = tweet[i:-1]
    return out

primelist = []
for i in range(0, len(tweetlist)):
    primelist.append(clipper(tweetlist[i]))
len(primelist)
primelist.insert(33,tlinex32)
#now I have new list to import back into main file
'''
refined_list = ["Whether you can attend in person or not, the CNI mtg roadmap is always a great what\'s going on read/update. If you will be at #cni19f I hope to see you at my session w @thecorkboard on privacy in learning analytics!\n\nhttps://t.co/cjQtPk700C",
               "Whether you can attend in person or not, the CNI mtg roadmap is always a great what\'s going on read/update. If you will be at #cni19f I hope to see you at my session w @thecorkboard on privacy in learning analytics!\n\nhttps://t.co/cjQtPk700C",
               "Whether you can attend in person or not, the CNI mtg roadmap is always a great what\'s going on read/update. If you will be at #cni19f I hope to see you at my session w @thecorkboard on privacy in learning analytics!\n\nhttps://t.co/cjQtPk700C",
               "Whether you can attend in person or not, the CNI mtg roadmap is always a great what\'s going on read/update. If you will be at #cni19f I hope to see you at my session w @thecorkboard on privacy in learning analytics!\n\nhttps://t.co/cjQtPk700C"]
for i in range(4,len(tweetlist)):
    refined_list.append(re.findall(r'\"(.+?)\"',tweetlist[i]))
len(refined_list)
refined_list.insert(33, tlinex32)
'''