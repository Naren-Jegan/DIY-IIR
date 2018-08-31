import requests
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from bs4 import BeautifulSoup as bs
import pickle
import re


def preprocess(sentence):
    sentence = sentence.lower()
    tokenizer = RegexpTokenizer(r'\w+')
    words = tokenizer.tokenize(sentence)
    lemmatizer = WordNetLemmatizer()
    filtered_words = [lemmatizer.lemmatize(w) for w in words if w not in stopwords.words('english')]
    return ' '.join(filtered_words)


with open("./relevant.txt", 'r') as f:
    for baseurl in f:
        print(baseurl)
        content = ''.join(['%s' % x.text for x in bs(requests.get(baseurl[:-1]).text, 'html.parser').find_all('p')])
        print(preprocess(content))
        exit(0)
