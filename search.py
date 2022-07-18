from owlready2 import *
from regex import P
onto_path.append('onto_path')
from text_preprocessing import *
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk, string
from  rdflib import Graph  # using rdflib to mange the ontology ////

print('start')
g=Graph().parse('onto_path/service_onto.owl')
print('1')

search_input = 'sac a dos'
sentence = search_input


words = sentence.split(' ')
words=stemming(words)
'''for word in words:
    results = set(results).union(onto.search(has_all_data='*'+word+'*'))'''

subq2 = '|'.join(words)
q2='''
    prefix ab:<http://yowyob.org/service_onto.owl#>
    SELECT distinct ?subject ?label
    WHERE {
    ?subject ab:has_label ?label
    FILTER regex(?object, sac, "i")
}
'''

q1='''
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ab: <http://yowyob.org/service_onto.owl#>
SELECT ?sub  ?obj 
WHERE {
 ?sub ab:has_label ?obj
FILTER regex(?obj, "'''+subq2+'''", "i").
} 

'''
print('2')

#execute query
results = g.query(q1)
for r in results:
    print(r['obj'])
quit()
