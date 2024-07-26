import praw
import pandas as pd
from praw.models import MoreComments
 
reddit_read_only = praw.Reddit(client_id="",		 # your client id
							client_secret="",	 # your client secret
							user_agent="")        # your user agent
 
# URL of the post
url = "https://www.reddit.com/r/RaidShadowLegends/comments/1e9c1xl/current_summon_pool_good_or_bad/"
 
# Creating a submission object
submission = reddit_read_only.submission(url=url)

 
post_comments = []
 
for comment in submission.comments:
    if type(comment) == MoreComments:
        continue
 
    post_comments.append(comment.body)
 
# creating a dataframe
comments_df = pd.DataFrame(post_comments, columns=['comment'])
comments_df.to_csv("Top Comments.csv", index=True)