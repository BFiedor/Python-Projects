import praw
import pandas as pd
from praw.models import MoreComments

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
#Must Download each nltk dataset to perform Sentiment Analysis, easily could do 'all'
#Only needs downloaded once
#nltk.download('vader_lexicon')
 
# Read-only instance for Python bot
reddit_read_only = praw.Reddit(client_id="",		 # your client id
							client_secret="",	 # your client secret
							user_agent="")        # your user agent

#Subreddit to read through
subreddit = reddit_read_only.subreddit("<SUBREDDIT NAME HERE>")
 
# Scraping the top posts of the current month, can change time_filter to "all", "day", "hour", "month", "week", or "year"
#Can also adjust top to be any of the following "new", "hot", "Controversial", "Rising"
posts = subreddit.top(time_filter="month")

#Initialize Sentiment Analyzer from import to the sid variable
sid = SentimentIntensityAnalyzer()

#Extracting values from posts to append to dictionaries that will be printed out to CSV files
posts_dict = {"Title": [], "Post Text": [], "Polarity": []}
Polarity_scores = {"pos": 0, "neg": 0, "neu": 0}
for post in posts:
    # Title of each post
    posts_dict["Title"].append(post.title)
    Title_Sentiment_scores = sid.polarity_scores(post.title) #Prebuilt SentAnalyzer lists polarity scores of Neutral, Positive, Negative and Compound
    del Title_Sentiment_scores['compound'] #Ignore Compound value from Sentiment scores
    Keymax = max(zip(Title_Sentiment_scores.values(), Title_Sentiment_scores.keys()))[1] #Acquire the max key value from the sentiment scores
    
    
    # Text inside a post
    posts_dict["Post Text"].append(post.selftext)
    Text_Sentiment_scores = sid.polarity_scores(post.selftext)
    del Text_Sentiment_scores['compound']
    Keymax1 = max(zip(Text_Sentiment_scores.values(), Text_Sentiment_scores.keys()))[1]
    
    #If both the Title and Post Text are the same sentiment, append sentiment to posts dict and update the total polarity scores
    if Keymax == Keymax1:
        Polarity_scores[f"{Keymax}"] += 1
        posts_dict["Polarity"].append(Keymax)
    #Append the Polarity of the title or post text depending on which has the higher sentiment score if the polarity differs,
    elif Title_Sentiment_scores[Keymax] > Text_Sentiment_scores[Keymax1]:
        Polarity_scores[f"{Keymax}"] += 1
        posts_dict["Polarity"].append(Keymax)
    else:
        Polarity_scores[f"{Keymax1}"] += 1
        posts_dict["Polarity"].append(Keymax1)
 
# Saving the data in a pandas dataframe
top_posts = pd.DataFrame(posts_dict)
top_postsPolarity = pd.DataFrame([Polarity_scores])
# Saving the dataframes to CSV Files for easy viewing in Table Format
top_posts.to_csv("<INSERTNAMEHERE>.csv", index=True)
top_postsPolarity.to_csv("<INSERTNAMEHERE>SAPolarity.csv", index=True)