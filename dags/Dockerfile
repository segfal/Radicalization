FROM apache/airflow:2.2.3
USER root
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         build-essential 
 


RUN pip3 install --no-cache-dir --user spacy nltk python-dotenv openpyxl praw tweepy

