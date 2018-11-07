import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
import numpy
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def preprocess(sentence):
    sentence = sentence.lower()
    tokenizer = RegexpTokenizer(r'[a-zA-Z]+')
    words = tokenizer.tokenize(sentence)
    lemmatizer = WordNetLemmatizer()
    filtered_words = [lemmatizer.lemmatize(w) for w in words if w not in stopwords.words('english')]
    return ' '.join(filtered_words)

with open('processed_documents.pickle','rb') as proc_docs:
    docs = pickle.load(proc_docs)
    corpus = numpy.array([x['doc'] for x in docs])
    urls = [x['url'] for x in docs]
    
vectorizer = TfidfVectorizer(use_idf=True)
doc_vecs = vectorizer.fit_transform(corpus).toarray()

#print(doc_vecs)
#print(vectorizer.get_feature_names())
vocab = vectorizer.get_feature_names()
#df= pd.DataFrame(doc_vecs,index = corpus,columns =vocab)

query = [preprocess(input())]
#print(query)

#mapping = dict(zip(vocab,vectorizer))
#print(mapping)
cv = CountVectorizer()
vecs = cv.fit_transform(corpus)
print(cv.vocabulary_)

#print(vectorizer.vocabulary_)
new_vectorizer = TfidfVectorizer(vocabulary = vocab,use_idf=True)
query_vec = new_vectorizer.fit_transform(query)

similarity = zip(urls,cosine_similarity(doc_vecs,query_vec))

similarity = sorted(similarity,reverse=True,key=lambda x: x[1])

#print(similarity)