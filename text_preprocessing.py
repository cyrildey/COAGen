from unittest import result
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
import re

    
#Removing Extra Whitespaces and transform them into lowercase: takes a list and return a list
def remove_whitespace(text):
    result = []
    for word in text:
        result.append((" ".join(word.split())).lower())
    return  result

#Tokenization: takes lists and returns lists
def tokenize(text_array):
    result = []
    for text in text_array:
        result= result + word_tokenize(text)
    return  result

#Stopwords Removal: takes lists and returns lists
def remove_stopwords(text):
    en_stopwords = stopwords.words('english')
    fr_stopwords = stopwords.words('french')
    result = []
    for token in text:
        if (token not in en_stopwords) and (token not in fr_stopwords):
            result.append(token)
    return result

#Removing Punctuations: takes a list and returns a list
def remove_punct(text):
    tokenizer = RegexpTokenizer(r"\w+")
    lst=tokenizer.tokenize(' '.join(text))
    return lst


#Stemming: takes list and returns list
def stemming(text):
    porter = PorterStemmer()
    
    result=[]
    for word in text:
        result.append(porter.stem(word))
    return result

#Removal of URLs: takes list and return list
def remove_urls(text):
    result=[]
    for word in text:
        url_pattern = re.compile(r'https?://\S+|www\.\S+')
        result.append(url_pattern.sub(r'', word))
    return result

#Removal of HTML Tags: takes a list and returns a list
def remove_tag(text):
    result=[]
    for word in text:
        #word=' '.join(word)
        html_pattern = re.compile('<.*?>')
        result.append(html_pattern.sub(r'', word))
    return result

## reserved for tests
#text=['textO','one', 'LLLets  us do that']
#print(remove_whitespace(text))