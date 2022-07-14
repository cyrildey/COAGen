from owlready2 import *
from regex import P
onto_path.append('onto_path')
from text_preprocessing import *
'''from sklearn.feature_extraction.text import TfidfVectorizer
import nltk, string

stemmer = nltk.stem.porter.PorterStemmer()
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)

def stem_tokens(tokens):
    return [stemmer.stem(item) for item in tokens]

'''#remove punctuation, lowercase, stem
'''
def normalize(text):
    return stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))

vectorizer = TfidfVectorizer(tokenizer=normalize, stop_words='english')
    

def cosine_sim(text1, text2):
    text1 = str(text1)
    text2 = str(text2)
    tfidf = vectorizer.fit_transform([text1, text2])
    return ((tfidf * tfidf.T).A)[0,1]
'''
onto = get_ontology("./onto_path/service_onto.owl").load()

sentence = 'bac'
results=[]
PoM = []
answers = []

a_full = onto.search(has_all_data='*'+sentence+'*')

words = sentence.split(' ')
words=stemming(words)
for word in words:
    results = set(results).union(onto.search(has_all_data='*'+word+'*'))

for r in results:
    data = str(r.has_label)
    data =data.split(' ')
    data = stemming(data)
    data = remove_punct(data)
    data = remove_urls(data)
    P = 100*len(set(words).intersection(data))/len(words)
    #P = cosine_sim(words, data)
    input(P)
    if(P>=33):
        r.has_PoM = P
        answers.append(r)



for r in a_full:
    r.has_PoM = 100
    answers.append(r)

#input('start others')
for r in answers:
    print(r.has_label) 
    print(r.has_PoM)




'''result = dict()
ind = onto.individuals()
wd = 'sacs à dos'
wd = wd.split(' ')
wd=remove_punct(wd)
wd=remove_urls(wd)
wd=tokenize(wd)
wd=remove_stopwords(wd)
wd=remove_whitespace(wd)
wd=stemming(wd)
#input(str(wd))
for i in ind:
    lb=str(i.has_label[0])
    lb = lb.split(' ')
    lb=remove_punct(lb)
    lb=remove_urls(lb)
    lb=tokenize(lb)
    lb=remove_stopwords(lb)
    lb=remove_whitespace(lb)
    lb=stemming(lb)
    x=len(set(wd).intersection(lb))
    if (x>0):
        print(lb)
        try:
            result[x].append(i.has_label)
        except KeyError:
            result[x]=[i.has_label]
l=sorted(result.keys())
input('done')
for i in range(len(l)-1,-1,-1):
    print(l[i])
'''
'''
label =  composer uniquement du mot
avoir le mot 

'''

