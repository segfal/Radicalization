import psycopg2 as pgres
import pandas as pd
#import reddit_posts as rp
import os
import datetime



reddit_posts = pd.read_excel("reddit_posts_2022-02-22.xlsx")
#print(reddit_posts.keys())


del reddit_posts["Unnamed: 0"]


#print(len(reddit_posts.keys()))


column = reddit_posts.keys()

rows = len(reddit_posts.keys()[0])

#print(rows)

#print(reddit_posts[reddit_posts.keys()[0]][1])
test = {}
post_list = []
for i in range(rows):
    for j in reddit_posts.keys():
        test[j] = str(reddit_posts[j][i])
    post_list.append(test)
    test = {}
#print(post_list[0])


#j = post_list[0].keys()
#print(j)



'''

{
        "Date" : date,
        "PostID" : postid,
        "Title" : title,
        "Text" : text,
        "UpVote" : upvote
        "Sentiment" : sentiment
    }
'''

##auth


conn = pgres.connect(database="social_network", user="airflow", password="airflow", host="0.0.0.0", port="5432")
curr = conn.cursor()
## Create a table
curr.execute("CREATE TABLE IF NOT EXISTS reddit_posts (Date text, PostID text, Title text, Text text, UpVote text , Sentiment text)")
for i in post_list:
    curr.execute("INSERT INTO reddit_posts (Date, PostID, Title, Text, UpVote, Sentiment ) VALUES (%s, %s, %s, %s, %s , %s)", (i['Date'], i['PostID'], i['Title'], i['Text'], i['UpVote'], i['Sentiment'] ))
conn.commit()
curr.close()
conn.close()


import abc


class LoadData:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def load_data(self):
        pass

    @abc.abstractmethod
    def findexcelsheet(self):
        pass
    
    @abc.abstractmethod
    def createexcelsheet(self):
        pass
    
