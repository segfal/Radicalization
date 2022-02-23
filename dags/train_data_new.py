##Credit https://www.digitalocean.com/community/tutorials/how-to-perform-sentiment-analysis-in-python-3-using-the-natural-language-toolkit-nltk#step-3-normalizing-the-data
from scipy import rand
import spacy
import nltk
import re
import os
import numpy as np
import pandas as pd ## organize data
##AccuracyScore
import random
import re,string 
import abc
import json
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag 
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import FreqDist




class CleanData:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')
        self.stopwords = nltk.corpus.stopwords.words('english')
        self.amazon = ""
        self.yelp = ""
        self.imdb = ""
        self.yelp = pd.read_table('yelp_labelled.txt')
        self.amazon = pd.read_table('amazon_cells_labelled.txt')
        self.imdb = pd.read_table('imdb_labelled.txt')
        self.dataframes = [self.yelp, self.amazon, self.imdb] ## list of dataframes
        nltk.download('stopwords')
        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')
        nltk.download('wordnet')
        nltk.download('omw-1.4') # Lemmatize the sentence
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
        


    
    def tokenize(self,arr):
        return list(map(str.split,arr))
    


     


    def remove_noise(review_tokens,stop_words = ()):
        cleaned_tokens = []
        for token,tag in pos_tag(review_tokens):
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

        
        
    




class Train(CleanData):
    def __init__(self):
        super().__init__()
    



    def remove_noise(self,review_tokens,stop_words = ()):
        cleaned_tokens = []
        for token,tag in pos_tag(review_tokens):
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

            
    def lemmatize(self,text):
        return [word.lemma_ for word in self.nlp(text)]
    


    def get_words(self,cleaned_tokens_list):
        for tokens in cleaned_tokens_list:
            for token in tokens:
                yield token

    def get_for_model(self,cleaned_tokens_list):
        for tokens in cleaned_tokens_list:
            yield dict([token, True] for token in tokens)
    
    def implement(self,sentence):
        self.pos_words = self.tokenize(self.positive)
        self.neg_words = self.tokenize(self.negative)

        #from nltk.corpus import stopwords
        #stop_words = stopwords.words('english')


        positive_cleaned_tokens = []
        negative_cleaned_tokens = []

        for tokens in self.pos_words:
            positive_cleaned_tokens.append(self.remove_noise(tokens,self.stopwords))
        for tokens in self.neg_words:
            negative_cleaned_tokens.append(self.remove_noise(tokens,self.stopwords))
        
        all_pos_words = self.get_words(positive_cleaned_tokens)

        positive_tokens_for_model = self.get_for_model(positive_cleaned_tokens)
        negative_tokens_for_model = self.get_for_model(negative_cleaned_tokens)

        positive_dataset = [(tokens, "Positive") for tokens in positive_tokens_for_model]
        negative_dataset = [(tokens, "Negative") for tokens in negative_tokens_for_model]
        from nltk import FreqDist
        #print(positive_dataset)
        #print(negative_dataset)
        freq_dist_pos = FreqDist(all_pos_words)
        dataset = positive_dataset + negative_dataset
        
        random.shuffle(dataset)
        
        from nltk import classify
        from nltk import NaiveBayesClassifier
        train_data = dataset[:2745]
        test_data = dataset[2745:]
        #print(train_data)
        
        classifier = NaiveBayesClassifier.train(train_data)

        custom_token = self.remove_noise(word_tokenize(sentence))
        return classifier.classify(dict([token, True] for token in custom_token))
        #return None


    
    
    
    
        
    






    



Reddit = Train()
Reddit.implement("I hate this movie")


    







        
    










