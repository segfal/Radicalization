
import json
import time
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
from dags.pgresload import LoadData

table = [] ## all json data will be here
def create_row(date,postid,title,text,upvote,subreddit): ##Row for every post
    return {
        "Date" : date,
        "PostID" : postid,
        "Subreddit" : subreddit,
        "Title" : title,
        "Text" : text,
        "UpVote" : upvote,
    }

# Load environment variables
dotenv.load_dotenv()
reddit_key = os.getenv("REDDIT_KEY")
reddit_secret = os.getenv("REDDIT_SECRET")





reddit = praw.Reddit(
    client_id=reddit_key,
    client_secret=reddit_secret
    , user_agent= "radical"
    , username= "segfal32"
    )
'''
subreddit = reddit.subreddit("compsci")

x = ""
for submission in reddit.subreddit("compsci").hot(limit=25):
    #print(submission.title)
    #submission.public_description
    sub = "compsci"
    #x = submission.selftext
    x = int(submission.created_utc)
    x = datetime.utcfromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S')
    for comments in submission.comments:
        time = datetime.utcfromtimestamp(comments.created_utc).strftime('%Y-%m-%d %H:%M:%S')
        postid = comments.id
        title = comments.submission.title
        text = comments.body
        upvote = comments.score
        



        table.append(create_row(time,postid,title,text,upvote,sub))
        



#print(subreddit.public_description)
'''

'''
for submission in reddit.subreddit("compsci").new(limit=10):
    print(submission.title)
    print(submission.selftext)
''' #prints new posts


##turn table to json
#arr = json.dumps(table)


def get_reddit_thread(subreddit = "compsci",range = 3):
    """
    Get the latest posts from a subreddit
    :param subreddit: The subreddit to get the posts from
    :param range: The range of posts to get
    :return: A list of posts
    """
    sub = subreddit
    subreddit = reddit.subreddit(subreddit)
    posts = []
    for submission in subreddit.new(limit=range):
        title = submission.title
        text = submission.selftext
        upvote = submission.score
        time = datetime.utcfromtimestamp(submission.created_utc).strftime('%Y-%m-%d %H:%M:%S')
        postid = submission.id
        posts.append(create_row(time,postid,title,text,upvote,sub))
    return posts


    
import pgresload as pg
import abc

class Reddit_Posts(LoadData):
    def create_row(self,date,postid,title,text,upvote,subreddit):
        return {
            "Date" : date,
            "PostID" : postid,
            "Subreddit" : subreddit,
            "Title" : title,
            "Text" : text,
            "UpVote" : upvote,
            "Sentiment" : "",
        }