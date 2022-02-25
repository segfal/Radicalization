FROM apache/airflow:2.2.3
USER root
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         build-essential 
 
USER airflow
COPY stopwords.txt stopwords.txt
COPY amazon_cells_labelled.txt amazon_cells_labelled.txt
COPY imdb_labelled.txt imdb_labelled.txt 
COPY yelp_labelled.txt yelp_labelled.txt
COPY downloads.py downloads.py


RUN pip3 install --no-cache-dir --user nltk python-dotenv openpyxl praw tweepy
RUN python3 downloads.py


