import psycopg2
import sys
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import requests
import json
import os
import requests
from flask import jsonify
import json


url = "http://172.26.0.2:5100/"

reddit_dumps = requests.get(url)
apicall = reddit_dumps.json()

'''

{
        "Date" : date,
        "PostID" : postid,
        "Title" : title,
        "Text" : text,
        "UpVote" : upvote
    }

'''
##auth


conn = psycopg2.connect(database="social_network", user="postgres", password="H5pME2DfJPtvuSJM", host="localhost", port="5432")
curr = conn.cursor()

## Create a table
curr.execute("CREATE TABLE IF NOT EXISTS reddit_posts (Date text, PostID text, Title text, Text text, UpVote text)")
for i in apicall:
    curr.execute("INSERT INTO reddit_posts (Date, PostID, Title, Text, UpVote) VALUES (%s, %s, %s, %s, %s)", (i['Date'], i['PostID'], i['Title'], i['Text'], i['UpVote']))
conn.commit()
curr.close()
conn.close()
