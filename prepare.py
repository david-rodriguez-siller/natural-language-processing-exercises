import unicodedata
import re
import json
import nltk
import pandas as pd
import acquire

from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords

from time import strftime

def basic_clean(string):
    article = string.lower()
    article = unicodedata.normalize('NFKD', article)\
    .encode('ascii', 'ignore')\
    .decode('utf-8', 'ignore')
    article = re.sub(r"[^a-z0-9'\s]", '', article)
   
    return article

def tokenize(string):
    tokenizer = nltk.tokenize.ToktokTokenizer()
    print(tokenizer.tokenize(string, return_str = True))
    
def stem(string):
    ps = nltk.porter.PorterStemmer()
    stems = [ps.stem(word) for word in string.split()]
    article_stemmed = ' '.join(stems)
    print(article_stemmed)
    
def lemmatize(string):
    wnl = nltk.stem.WordNetLemmatizer()
    lemmas = [wnl.lemmatize(word) for word in string.split()]
    article_lemmatized = ' '.join(lemmas)
    print(article_lemmatized)
    
def remove_stopwords(string, extra_words = [], exclude_words = []):
    stopword_list = stopwords.words('english')
    stopword_list = set(stopword_list) - set(exclude_words)
    stopword_list = stopword_list.union(set(extra_words))
    words = string.split()
    filtered_words = [word for word in words if word not in stopword_list]
    string_wo_stopwords = ' '.join(filtered_words)
    
    return string_wo_stopwords