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

'''
the thing that lagged me down was 
list(pages.find({}))