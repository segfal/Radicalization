import train_data_new as train 
import datetime
import os
import numpy as np
import pandas as pd
import tweepy as tw
import requests as rq
from flask import Flask
import praw
import dotenv
from datetime import datetime
import json
import time
import datetime
from pendulum import datetime
import loadtopgres as pgres

class Reddit(train.Train, pgres.LoadData):
    def __init__(self):
        pass
        self.reddit_key = os.getenv('REDDIT_KEY')
        self.reddit_secret = os.getenv('REDDIT_SECRET')
        self.reddit = praw.Reddit(client_id=self.reddit_key, client_secret=self.reddit_secret, user_agent='radical',username = 'radical')
        self.post = []
        self.subreddit = ''
    

    def create_row(self,date,postid,title,text,upvote,subreddit):
        return{
            'date':date,
            'postid':postid,
            'subreddit':subreddit,
            'title':title,
            'text':text,
            'upvote':upvote,
            'sentiment':0,
        }
    def get_reddit_thread(self,subreddit = "compsci",range = 3):
        sub = subreddit
        self.subreddit = self.reddit.subreddit(sub)
        for submission in self.subreddit.top(limit=range):
            self.post.append(self.create_row(submission.created_utc,submission.id,submission.title,submission.selftext,submission.ups,sub))
        return self.post
    def push_to_excel(self,subreddit = "compsci",range = 3):
        self.get_reddit_thread(subreddit,range)
        for i in self.post:
            scorecard = self.implement(i['text'])
            if scorecard == "positive":
                i['sentiment'] = 1
            if scorecard == "negative":
                i['sentiment'] = -1
            else:
                continue
        datepulled = datetime.datetime.now().strftime('%Y-%m-%d')


        #check if sheet exists
        if os.path.exists(f"reddit_posts_{datepulled}.xlsx"):
            pd.read_excel(f"reddit_posts_{datepulled}.xlsx")
            ##add to existing sheet
            df = pd.read_excel(f"reddit_posts_{datepulled}.xlsx")
            df = df.append(self.post,ignore_index=True)
            df.to_excel(f"reddit_posts_{datepulled}.xlsx",index=False)
        else:
            pd.DataFrame(self.post).to_excel(f"reddit_posts_{datepulled}.xlsx",index=False)
        return None
        def find_sheet(self,datepulled):
            if os.path.exists(f"reddit_posts_{datepulled}.xlsx"):
                return pd.read_excel(f"reddit_posts_{datepulled}.xlsx")
            else:
                return None
        


    


    

