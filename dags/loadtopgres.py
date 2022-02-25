import psycopg2 as pgres
import pandas as pd
import os
import datetime



class LoadData:
    def __init__(self):
        self.host = "host.docker.internal"
        #self.host = "localhost"
        self.conn = pgres.connect(database="social_network", user="airflow", password="airflow", host=self.host, port="5432")
        self.curr = self.conn.cursor()
        self.curr.execute("CREATE TABLE IF NOT EXISTS reddit_posts (Date text, PostID text, Title text, Text text, UpVote text , Sentiment text)")
        self.conn.commit()
        self.curr.close()
        self.conn.close()
    def load_data(self,data):
        pass
    
        