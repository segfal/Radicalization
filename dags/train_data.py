##Credit https://www.digitalocean.com/community/tutorials/how-to-perform-sentiment-analysis-in-python-3-using-the-natural-language-toolkit-nltk#step-3-normalizing-the-data


import spacy
import nltk
import re
import os
import numpy as np
import pandas as pd ## organize data
##AccuracyScore
from sklearn.metrics import accuracy_score
#CountVectorizer
from sklearn.feature_extraction.text import CountVectorizer
#TfidfVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
#train_test_split
from sklearn.model_selection import train_test_split
#TransformerMixin
from sklearn.base import TransformerMixin
#LinearSVC
from sklearn.svm import LinearSVC
#Pipeline
from sklearn.pipeline import Pipeline
import random
import re,string 



yelp = pd.read_table('yelp_labelled.txt')
amazon = pd.read_table('amazon_cells_labelled.txt')
imdb = pd.read_table('imdb_labelled.txt')


dataframes = [yelp, amazon, imdb] ## list of dataframes


for column in dataframes:
    column.columns = ["message", "target"] ## rename columns

keys = ['Yelp','IMDB','Amazon'] # labels


df = pd.concat(dataframes, keys=keys) ## combine dataframes
#print(df.head())
sp = spacy.load('en_core_web_sm') ## load spacy model to get stopwords

all_stopwords = sp.Defaults.stop_words ## get stopwords from spacy


#print(df.head())
#print(df['message'])



def remove_stopwords(text):
    tokens = [word for word in text.split() if word not in all_stopwords] ## remove stopwords
    return " ".join(tokens) ## join tokens into string


for i in df['message']:
    i = remove_stopwords(i)
    #print(i)










''' Testing
#print(df)



x = list(df['message'])
y = list(df['target'])


for i in range(0,3):
    print(x[i],y[i])

print(len(x),len(y))


3/4 of the data will be training and 1/4 will be for testing
'''





negative = []
positive = []


for i in range(len(df)):
    if df['target'][i] == 0:
        negative.append(df['message'][i])
    else:
        positive.append(df['message'][i])


nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')







def tokenme(arr): #Tokenize the list
    return list(map(str.split,arr))

#a = tokenme(positive)
#b = tokenme(negative)
#print(a)
##print(pos_tag(a[0]))

pos_words = tokenme(positive)
neg_words = tokenme(negative)
from nltk.corpus import stopwords
stop_words = stopwords.words('english')


nltk.download('omw-1.4') # Lemmatize the sentence
from nltk.tag import pos_tag 
from nltk.stem.wordnet import WordNetLemmatizer
nltk.download('stopwords')


def lemmatize_sentence(tokens):
    lemmatizer = WordNetLemmatizer() ## lemmatize the sentence
    lemmatized_sentence = [] ## lemmatized sentence
    for word, tag in pos_tag(tokens):## tag the sentence
        if tag.startswith('NN'):## if the tag starts with NN
            pos = 'n'## noun
        elif tag.startswith('VB'): ## if the tag starts with VB
            pos = 'v'## verb
        else:
            pos = 'a'## adjective
        lemmatized_sentence.append(lemmatizer.lemmatize(word, pos))
    return lemmatized_sentence## return the lemmatized sentence


def remove_noise(review_tokens, stop_words = ()):

    cleaned_tokens = [] ## cleaned tokens

    for token, tag in pos_tag(review_tokens):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token) 
        token = re.sub("(@[A-Za-z0-9_]+)","", token) 

        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
    return cleaned_tokens


positive_reviews_cleaned_tokens = []
positive_reviews_cleaned_tokens = []


positive_cleaned_tokens_list = []
negative_cleaned_tokens_list = []

for tokens in pos_words: ## for each tweet
    positive_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

for tokens in neg_words:
    negative_cleaned_tokens_list.append(remove_noise(tokens, stop_words))



def get_all_words(cleaned_tokens_list):
    for tokens in cleaned_tokens_list:
        for token in tokens:
            yield token

all_pos_words = get_all_words(positive_cleaned_tokens_list)


from nltk import FreqDist

freq_dist_pos = FreqDist(all_pos_words)
#print(freq_dist_pos.most_common(10)) ## most common words



def get_reviews_for_model(cleaned_tokens_list):
    for review_tokens in cleaned_tokens_list:
        yield dict([token, True] for token in review_tokens)

positive_tokens_for_model = get_reviews_for_model(positive_cleaned_tokens_list)
negative_tokens_for_model = get_reviews_for_model(negative_cleaned_tokens_list)





import random

positive_dataset = [(tweet_dict, "Positive")
                     for tweet_dict in positive_tokens_for_model]

negative_dataset = [(tweet_dict, "Negative")
                     for tweet_dict in negative_tokens_for_model]

dataset = positive_dataset + negative_dataset

random.shuffle(dataset)


#print(len(dataset))
train_data = dataset[:2745]
test_data = dataset[2745:]

from nltk import classify
from nltk import NaiveBayesClassifier

classifier = NaiveBayesClassifier.train(train_data)

#print("Accuracy is:", classify.accuracy(classifier, test_data))

#print(classifier.show_most_informative_features(10))


from nltk.tokenize import word_tokenize






from nltk.tokenize import word_tokenize

custom_tweet = "I ordered just once from TerribleCo, they screwed up, never used the app again."

custom_tokens = remove_noise(word_tokenize(custom_tweet))

#print(classifier.classify(dict([token, True] for token in custom_tokens)))




custom_tweet = '''
Awesome product

'''
custom_tokens = remove_noise(word_tokenize(custom_tweet))

#print(classifier.classify(dict([token, True] for token in custom_tokens)))


def insert_sentiment(review):
    review_processed = remove_noise(word_tokenize(review))
    return classifier.classify(dict([token, True] for token in review_processed))





import abc



    