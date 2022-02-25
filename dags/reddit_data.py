import train_data as train
import datetime
import os
import pandas as pd
import praw
import dotenv
#import datetime
import loadtopgres as pgres
import s3 as s3boto
import nltk







class Reddit(pgres.LoadData , s3boto.PushToS3 , train.CleanData):
    def __init__(self):
        super().__init__()
        #inherit from Train class
        super(train.Train).__init__()
        #inherit from LoadData class
        super(pgres.LoadData).__init__()
        #inherit from PushToS3 class
        super(s3boto.PushToS3).__init__()
        #inherit from CleanData class
        super(train.CleanData).__init__()
        
        self.stopwords = nltk.corpus.stopwords.words('english')
        self.reddit_key = os.getenv('REDDIT_KEY')
        self.reddit_secret = os.getenv('REDDIT_SECRET')
        self.reddit = praw.Reddit(client_id=self.reddit_key, client_secret=self.reddit_secret, user_agent='radical',username = 'segfault')
        self.post = []
        self.subreddit = ''
        self.yelp = pd.read_table('yelp_labelled.txt')
        self.amazon = pd.read_table('amazon_cells_labelled.txt')
        self.imdb = pd.read_table('imdb_labelled.txt')
        self.dataframes = [self.yelp, self.amazon, self.imdb] ## list of dataframes
        for column in self.dataframes:
            column.columns = ["message", "target"]
        self.keys = ['Yelp','IMDB','Amazon'] # labels
        self.df = pd.concat(self.dataframes, keys=['Yelp','IMDB','Amazon']) ## combine dataframes
        self.negative = []
        self.positive = []
        self.pos_words = []
        self.neg_words = []
        self.cleaned_pos_words = []
        self.cleaned_neg_words = []
        for i in range(len(self.df)):
            if self.df['target'][i] == 0:
                self.negative.append(self.df['message'][i])
            else:
                self.positive.append(self.df['message'][i])
        


      
        
        
    

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
        for submission in self.subreddit.new(limit=range):
            title = submission.title
            text = submission.selftext
            upvote = submission.score
            time = datetime.datetime.utcfromtimestamp(submission.created_utc).strftime('%Y-%m-%d %H:%M:%S')
            postid = submission.id
            self.post.append(self.create_row(time,postid,title,text,upvote,sub))
        return self.post
            
        return self.post
    def push_to_excel(self,subreddit = "compsci",range = 3):
        self.post = self.get_reddit_thread(subreddit,range)
        for i in self.post:
            scorecard = train.training.train(i['text'])
            #print(scorecard,i['text'])
            if scorecard == "Positive":
                i['sentiment'] = "1"
            else:
                i['sentiment'] = "-1"
            
        datepulled = datetime.datetime.now().strftime("%Y-%m-%d")



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
    
    def load_data(self):
        #find excel spreadsheets for the past 30 days
        host = "host.docker.internal"
        #host = "localhost"
        conn = pgres.pgres.connect(database="social_network", user="airflow", password="airflow", host=self.host, port="5432")
        cur = conn.cursor()

         ##Find excel files in current directory
        year = datetime.datetime.now().strftime("%Y")
        month = datetime.datetime.now().strftime("%m")
        for i in range(0,30):
            ## get the file name
            filename = "" + str(year) + "-" + str(month) + "-" + str(i) + ".xlsx"
            ## check if file exists
            if os.path.isfile(filename):
                ## read the file
                df = pd.read_excel(filename)
                ## iterate through the rows
                for index,row in df.iterrows():
                    ## check if row is empty
                    if pd.isna(row['text']):
                        continue
                    else:
                        ## check if row is already in the database
                        cur.execute("SELECT * FROM reddit_posts WHERE postid = %s",(row['postid'],))
                        result = cur.fetchone()
                        if result == None:
                            ## insert row into database
                            cur.execute("INSERT INTO reddit_posts (date,postid,subreddit,title,text,upvote,sentiment) VALUES (%s,%s,%s,%s,%s,%s,%s)",(row['date'],row['postid'],row['subreddit'],row['title'],row['text'],row['upvote'],row['sentiment']))
                            conn.commit()
                            print(f"Added {row['postid']} to database")
                        else:
                            continue

                ##push to postgres
             
            
        
                
            
        else: pass
        conn.commit()
        conn.close()
        return None





    def push_to_s3(self):

        dotenv.load_dotenv()

        ## load aws credentials
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        aws_password = os.getenv("AWS_PASSWORD")
        aws_name = os.getenv("AWS_NAME")

        s3 = s3boto.boto3.resource(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name='us-east-1'
        )

        ##Find excel files in current directory
        year = datetime.datetime.now().strftime("%Y")
        month = datetime.datetime.now().strftime("%m")
        for i in range(0,30):
            ## get the file name
            filename = "" + str(year) + "-" + str(month) + "-" + str(i) + ".xlsx"
            ## check if file exists
            if os.path.isfile(filename):

                ## upload file to s3
                s3.push_to_s3(filename)
                print(filename)
                ## delete the file
                os.remove(filename)
                print("Deleted file: " + filename)
            else:
                continue

    

#reddit = Reddit()
#reddit.push_to_excel("doomer",10)


    

