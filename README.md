# Fall_19_CNI_Member_conference_tweets
Natural language processing analysis of fall membership conference tweets for CNI

# Introduction

How do you evaluate the success of your organization’s periodic conference or trade event? Do you try to gage the engagement of your audience during the event through observation? This may be hard to do, and may not give you much information about what is working and what’s not. Do you send out a questionnaire to attendees after the fact? This requires thoughtful survey design, and attendees may not have the energy/time to respond until well after the conference ends, if at all, and details or topics that may be important won’t be as fresh in the mind. Why not survey as the conference goes on? This seems like a good balance, but it risks detracting from the event itself, thus detracting from the value that attendees receive from attendance, and if your goal in evaluation is to maximize what attendees get out of your event then you are putting the cart before the horse. 
Fortunately, there is a way to get feedback from your audience in the moment without detracting from their valuable and limited time. Just look at what they’re saying on twitter! 
Any social media outlet may provide some meaningful information, but because of twitter’s position as being the place to quickly throw out an opinion to the world, and it’s use of the searchable hashtag pointing to the topic of the tweet (your event), it is the ideal searching ground for sentiment and topic analysis. In short, with the right analytical tools, twitter is a great place to turn to find out what your guests main take-away is from your gathering. Since twitter has an API for easy data gathering, this can be a good, and inexpensive way to add an extra dimension of in-the-moment for organization who already employ the use of surveys as well.  
In this study, I conduct just such an analysis to find out more about attendee take-aways from the Coalition for Networked Information’s most recent semiannual membership conference. CNI is a member organization formed by two other IT focused associations to promote the use of digital information technology, who has over 250 members around the globe. The goal of any member association is to maximize value for their members, and with attendees traveling from all over the world, making the best use of their time while at an event that only happens twice a year is important. It is the goal of this analysis to provide CNI with an extra assessment tool to be able to maintain or improve upon their members perceived value of subsequent events. 

# Exploratory Data Analysis

CNI has provided me with data that they have already gathered from twitter which includes over 2,000 tweets with the hashtag CNI19f. It contains timestamp, location and hashtag information in addition to the content of the tweets themselves.
Upon visual examination of a sample of the tweets provided, I see that while many of them appear to be complete, some have been cut short and followed by an html hyperlink to the complete tweet on twitter. A significant number of datapoints are also retweets of other tweets with the CNI19f hashtag, and denoted by placing “RT” in front of the body of the tweet. This is not the ideal way to track retweets from an analytical angle, but is something that I have seen previously when analyzing tweets, so is not unexpected. As most of the location data points to places outside of Washington D.C. where the conference is located, it is my assumption that this information points to the users listed “home ” location rather than their geographical position at the time of the tweet. 

The member conference took place  on the 9th and 10th of December, 2019. The earliest tweet is dated at November 27th, 2019, which is several weeks prior to the actual conference, and the latest tweet was on January 18th, 2020; more than a month later. The bulk of the tweets occur either during or on the a day after conference took place, with just 38 tweets prior to December 9th, and  only 90 tweets being posted after December 11th. This confirms that most of the sentiment being analyzed, specifically over 93% of it, comes either directly from, or on the heels of attending the conference. 

## About The Tweeters

This data contains 653 different twitter users, this includes anyone who retweeted, and the CNI twitter account. These twitter users have an average of 2,162 followers, however, how many of these followers are fellow conference attendees is unclear from this data. One way I can assess how connected they are to each other is to get a count of the times one of these users specifically mentions another one of these users. This I find that this occurs 1864 times, which means that each users is on average connected to roughly 3 other users within the dataset. When I recalculate this number while subtracting out mentions of the CNI twitter handle, I still see a number that rounds up to 3. These numbers do not reflect spammers, and if it can be assumed that a bot or spam tweeter is not mentioning or being mentioned by actual conference attendees, this means that the real average number of connections is actually higher. 

## Cleaning The Data

This first glance at the data brings up several questions. First, what to do with retweets? Should they be left in the model to capture the fact that people thought the sentiment worth sharing, or excluded to simply capture the width of topics being tweeted about without skewing results by popularity? Second, how to handle the fact that some of the tweets are incomplete? The last parts of these tweets may contain useful information. Thirdly, there are duplicate tweets within the data, one in particular that repeats many times. Should these be treated as spam, even though their topic is tangential to the conference? There are also several tweets that are definitely spam, and these I remove prior to conducting any analysis. I also remove tweets made by CNI itself, as these would not reflect member sentiment, the analysis of which is the goal of this study. It is of interest to note however, that the official CNI twitter account was retweeted 25 times. 

I first address the second question as it is easier to do. The obvious way to handle these tweets is simply to collect each tweet in its entirety and use this to replace the partial tweet within the data. Since there are 589 incomplete tweets within the dataframe, the most efficient method of accessing all of these tweet is web scraping. This automates the process of accessing the provided urls and extracting the data from them into a database, from which the body of the tweets can be extracted into a list. I then replace the original partial tweets with the tweets from this list to form a more complete picture from which to draw insights. 

In order to scrape the tweets that I need from the provided urls, I set up a Mongo database within a Docker instance, with which to execute the actual scraping and then use Beautiful Soup to extract the actual body of the tweets from entirety of scraped json encoding. I then use a regular expression to further clean the tweets of their twitter handles and merge these back into the original data using the flagged index values. 

The next question to address is that of the 39% of the tweets within the data that are actually retweets of other tweets within the dataset. I choose to first model the data without the retweets in order to get a sense of the topics that are being highlighted without weighting them by popularity, just to get a sense of what seems to be relevant. Then I go back and include retweets to capture more of a sense of common consensus on relevancy. 

# Analysis

The first major exploration that I make of the collection is topic modeling. Essentially I group the tweets into categories using non-negative matrix factorization and examine the most frequently occurring words in each category to get a sense of the topic of discussion that this category represents. The following sub-section will delve into the details of how I specify my model to achieve my output, but for the reader who is more interested in the actual results of this modeling than the under-the-hood mechanics of it, this sub-section may be safely skipped over. 

## Model Specification
In building my nmf model, I first create my bag of words, or a listing of all of the words used in any of the tweets. I then filter out English stop words, or words that are commonly used like “a” or “the”, as well as punctuation characters and the hashtag used to find the tweets; “cni19f”. I then perform vectorization on the remaining words across the body of the tweets using the tf-idf method to obtain my word matrix, as this method has the lowest reconstruction error of the ones I look at. Once vectorized I perform nmf upon this matrix to converge onto the groupings of words that best fit the data. Once this is done, I convert vectors back into words to get categorized word groupings which from which topicality can be gleaned. 

# Topics

In order to assess how many topics to categorize into, I run my model assuming several different numbers and view the 20 top scoring words in each category and make a judgement call from here based on how many of these categories seem cohesive vs a random jumble of words; it is my initial intention to default to ten categories, but when I do this several of them don’t make sense, leaving seven somewhat cohesive on-topic categories and one category that is obviously spam hashtags. When I narrow down to five categories I get a fairly clear sense of what they are about, and without the inclusion of a spam category 
5 Topics:
•	Digital preservation
•	Barriers to conference attendance and livestreaming
•	Quantum computing’s threat to data encryption
•	Data science, libraries and the need for diversity
•	Scholarly research and professional researchers



