import reddit_data as reddit


redditdata = reddit.Reddit()
redditdata.push_to_excel()
redditdata.load_data()
redditdata.push_to_s3()