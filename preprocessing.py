import requests
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from bs4 import BeautifulSoup as bs
from nltk import pos_tag
import pickle
import re
from os.path import isfile


def preprocess(sentence):
    sentence = sentence.lower()
    tokenizer = RegexpTokenizer(r'[a-zA-Z]+')
    words = tokenizer.tokenize(sentence)
    lemmatizer = WordNetLemmatizer()
    filtered_words = [lemmatizer.lemmatize(w) for w in words if w not in stopwords.words('english')]
    return ' '.join(filtered_words)


with open("./relevant.txt", 'r') as f:
    processed_documents = list(dict())
    if isfile('processed_documents.pickle'):
        with open('processed_documents.pickle', 'rb') as processed_documents_pickle:
            processed_documents = pickle.load(processed_documents_pickle)
    count = len(processed_documents)
    print(count)
    i = 0
    for baseurl in f:
        if i < count or (baseurl in [x['url'] for x in processed_documents]) or ('#' in baseurl and not baseurl.endswith('#')):
            i += 1
            continue
        try:
            content = ''.join(['%s' % x.text for x in bs(requests.get(baseurl[:-1]).text, 'html.parser').find_all('p')])
        except:
            print("couldn't reach\n")
            continue
        processed_document = preprocess(content)
        processed_documents.append({'url': baseurl, 'doc': processed_document})
        count += 1
        print(str(count) + '\r'),
        print(baseurl)
        with open('processed_documents.pickle', 'wb') as processed_documents_pickle:
            pickle.dump(processed_documents, processed_documents_pickle, protocol=-1)
