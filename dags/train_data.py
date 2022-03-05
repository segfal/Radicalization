##Credit https://www.digitalocean.com/community/tutorials/how-to-perform-sentiment-analysis-in-python-3-using-the-natural-language-toolkit-nltk#step-3-normalizing-the-data
#import spacy
import nltk
import re
import os
import numpy as np
import pandas as pd ## organize data
##AccuracyScore
import random
import re,string 


from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag 
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import FreqDist


#nltk.download('stopwords')
#nltk.download('punkt')
#nltk.download('averaged_perceptron_tagger')
#nltk.download('wordnet')
#nltk.download('omw-1.4') 
global all_stopwords

with open('./stopwords.txt', 'r') as f:
    all_stop_words = f.read().split(',')

all_stopwords = set(all_stop_words)


class CleanData:
    def __init__(self):
        #self.nlp = spacy.load('en_core_web_sm')
        pass
        

    def remove_stopwords(self,text):
       
        tokens = [word for word in text.split() if word not in all_stopwords] ## remove stopwords
        return " ".join(tokens) ## join tokens into string

    def split(self,df):
        positive = []
        negative = []
        for i in range(len(df)):
            if df['target'][i] == 0:
                negative.append(df['message'][i])
            else:
                positive.append(df['message'][i])
        return [positive,negative]
    def tokenme(self,arr):
        return list(map(str.split,arr))
    
    def lemmatize(self,text):
        lemmatizer = WordNetLemmatizer()
        tokens = [lemmatizer.lemmatize(word) for word in text.split()]
        return " ".join(tokens)
    def remove_noise(self,review_tokens, stop_words = ()):

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


    def get_all_words(self,cleaned_tokens_list):
        for tokens in cleaned_tokens_list:
            for token in tokens:
                yield token
    
    def get_for_model(self,cleaned_tokens_list):
        for review_tokens in cleaned_tokens_list:
            yield dict([token, True] for token in review_tokens)
    

        
        
    




class Train():
    def __init__(self,input_data):
        self.cleaner = CleanData()
        self.input_data = input_data
        self.positive_tokens = []
        self.negative_tokens = []
        self.positive_cleaned_tokens_list = []
        self.negative_cleaned_tokens_list = []
        self.positive_tokens_for_model = []
        self.negative_tokens_for_model = []
        self.pos_words = []
        self.neg_words = []
    
    def train(self,text):
        for i in self.input_data['message']:
            i = self.cleaner.remove_stopwords(i)
        

        box = self.cleaner.split(self.input_data)
        positive = box[0]
        negative = box[1]

        pos_words = self.cleaner.tokenme(positive)
        neg_words = self.cleaner.tokenme(negative)


        from nltk.corpus import stopwords
        stop_words = stopwords.words('english')
        #nltk.download('omw-1.4') # Lemmatize the sentence
        from nltk.tag import pos_tag 
        from nltk.stem.wordnet import WordNetLemmatizer
        #nltk.download('stopwords')

        positive_cleaned_tokens_list = []
        negative_cleaned_tokens_list = []


        for tokens in pos_words:
            positive_cleaned_tokens_list.append(self.cleaner.remove_noise(tokens, stop_words))
        for tokens in neg_words:
            negative_cleaned_tokens_list.append(self.cleaner.remove_noise(tokens, stop_words))
        

        all_pos_words = self.cleaner.get_all_words(positive_cleaned_tokens_list)
        all_neg_words = self.cleaner.get_all_words(negative_cleaned_tokens_list)

        pos_word_counts = FreqDist(all_pos_words)
        neg_word_counts = FreqDist(all_neg_words)

        positive_tokens_for_model = self.cleaner.get_for_model(positive_cleaned_tokens_list)
        negative_tokens_for_model = self.cleaner.get_for_model(negative_cleaned_tokens_list)


        positive_dataset = [(t, "Positive") for t in positive_tokens_for_model]
        negative_dataset = [(t, "Negative") for t in negative_tokens_for_model]

        dataset = positive_dataset + negative_dataset

        random.shuffle(dataset)
        train_data = dataset[:2745]
        test_data = dataset[2745:]

        from nltk import NaiveBayesClassifier
        classifier = NaiveBayesClassifier.train(train_data)

        custom_token = self.cleaner.remove_noise(word_tokenize(text))

        return classifier.classify(dict([token, True] for token in custom_token))












     

    



        

        

        
    



        
        






    

##implementation

DataCleaning = CleanData()




yelp = pd.read_table('./yelp_labelled.txt')
amazon = pd.read_table('./amazon_cells_labelled.txt')
imdb = pd.read_table('./imdb_labelled.txt')


dataframes = [yelp, amazon, imdb] ## list of dataframes


for column in dataframes:
    column.columns = ["message", "target"] ## rename columns

keys = ['Yelp','IMDB','Amazon'] # labels


df = pd.concat(dataframes, keys=keys) ## combine dataframes



for i in df['message']:
    i = DataCleaning.remove_stopwords(i)







training = Train(df)
custom_msg = 'I hate this'
x = training.train(custom_msg)
print(x)
x = training.train('life is awesome')
print(x)

