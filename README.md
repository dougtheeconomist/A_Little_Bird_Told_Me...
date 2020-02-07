# Fall_19_CNI_Member_conference_tweets
Natural language processing analysis of fall membership conference tweets for CNI


The Coalition for Networked Information(CNI) is an organization formed by two other IT focused associations to promote the use of digital information technology. CNI hosts semi-annual membership conferences to serve their members. 
CNI has provided me with twitter data from their most recent fall conference to analyze and extract any insights that may help them provide subsequent conferences to maximize the value of these conferences to their attending members. 

EDA
The provided data includes over 2,000 tweets with the hashtag CNI19f. It contains time, location and hashtag information in addition to the content of the tweets themselves.
Upon visual examination of a sample of the tweets provided, I see that while many of them appear to be complete, some have been cut short and followed by an html link to the complete tweet. A significant number of datapoints are also retweets of other tweets with the hashtag, and denoted by placing “RT” in front of the body of the tweet. As most of the location data points to places outside of Washington D.C. where the conference is located, it is my assumption that this information points to the users listed “home ” location rather than their geographical position at the time of the tweet. 

The basic look at the data brings up several questions. First, what to do with retweets? Should they be left in the model to capture the fact that people thought the sentiment worth sharing, or excluded to simply capture the width of topics being tweeted about without skewing results by popularity? Second, how to handle the fact that some of the tweets are incomplete? The last parts of these tweets may contain insightful information. Thirdly, there are duplicate tweets within the data, one in particular that repeats many times. Should these be treated as spam, even though their topic is tangential to the conference? There are also several tweets that are spam, and these I remove prior to conducting any analysis. I also remove tweets made by CNI itself, as these would not reflect member sentiment, though these only comprise less than one percent of the collection. 

I first address the second question as it is easier to do. The obvious way to handle these tweets is simply to collect each tweet in its entirety and use this to replace the partial tweet within the data. Since there are 589 incomplete tweets within the dataframe, the most efficient method of accessing all of these tweet is web scraping. This automates the process of accessing the provided urls and extracting the data from them into a database, from which the body of the tweets can be extracted into a list. I then replace the original partial tweets with the tweets from this list to form a more complete picture from which to draw insights. 

In order to scrape the tweets that I need from the provided urls, I set up a mongo database within a docker instance, with which to execute the actual scraping and then use Beautiful Soup to extract the actual body of the tweets from entirety of scraped json encoding. I then use a regular expression to further clean the tweets of their twitter handles and merge these back into the original data using the flagged index values. 

The next question to address is that of the 39% of the tweets within the data that are actually retweets of other tweets within the dataset. I choose to first model the data without the retweets in order to get a sense of the topics that are being highlighted without weighting them by popularity, just to get a sense of what seems to be relevant. Then I go back and include retweets to capture more of a sense of common consensus on relevancy. 

# Analysis

The first major exploration that I make of the collection is topic modeling. Essentially I group the tweets into categories using non-negative matrix factorization and examine the most frequently occurring words in each category to get a sense of the topic of discussion that this category represents. The following sub-section will delve into the details of how I specify my model to achieve my output, but for the reader who is more interested in the actual results of this modeling than the under-the-hood mechanics of it, this sub-section may be safely skipped over. 

## Model Specification
In building my nmf model, I first create my bag of words, or a listing of all of the words used in any of the tweets. I then filter out English stop words, or words that are commonly used like “a” or “the”, as well as punctuation characters and the hashtag used to find the tweets; “cni19f”. I then perform vectorization on the remaining words across the body of the tweets using the tf-idf method to obtain my word matrix. Once vectorized I perform nmf upon this matrix to converge onto the groupings of words that best fit the data. Once this is done, I convert vectors back into words to get categorized word groupings which from which topicality can be gleaned. 

# Word groupings 


