from pendulum import datetime
import train_data as train  # import train_data.py
import pull_data as pull  # import pull_data.py`
import pandas as pd

import time
import datetime
sub = "doomer" # subreddit name
reddit_posts = pull.get_reddit_thread(subreddit=sub,range=10)




for i in reddit_posts:
    scorecard = train.insert_sentiment(i["Text"])
    if scorecard == "Positive":
        i["Sentiment"] = 1
    elif scorecard == "Negative":
        i["Sentiment"] = -1
    else:
        continue

datepulled = datetime.datetime.now().strftime('%Y-%m-%d')


##check if excel sheet exists
import os
if os.path.exists(f"reddit_posts_{datepulled}.xlsx"):
    pd.read_excel(f"reddit_posts_{datepulled}.xlsx")
    ##add more data to excel sheet
    df = pd.read_excel(f"reddit_posts_{datepulled}.xlsx")
    df = df.append(reddit_posts, ignore_index=True)
    df.to_excel(f"reddit_posts_{datepulled}.xlsx", index=False)
else:
    pd.DataFrame(reddit_posts).to_excel(f"reddit_posts_{datepulled}.xlsx")
