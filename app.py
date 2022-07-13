'''
this file is the base of the API (flask)
'''
import os
import sys
#sys.path.append('../')
#from owlready2 import *
from flask import Flask, request, jsonify
#from text_preprocessing import *
from insert_delete_update import *
from  rdflib import Graph  # using rdflib to mange the ontology ////


#onto_path.append('onto_path')

# load the ontology
#onto = get_ontology("file://onto_path/service_onto.owl").load()


app = Flask(__name__)

#import the ontology
g=Graph().parse('onto_path/service_onto.owl')

def similar_service_of(g,service):
    service=str(service)
    query ='''
        prefix ab:<http://yowyob.org/service_onto.owl#>
        prefix ac:<http://www.w3.org/2002/07/owl#>
        prefix ad:<http://www.w3.org/2000/01/rdf-schema#>
        SELECT  ?new_service4_description ?new_service4_label  ?new_service4
        WHERE { 
        <'''+service+'''> a ?family .
        ?family ad:subClassOf ?family2 .
        ?family3 ad:subClassOf ?family2 .
        ?new_service2 ad:subClassOf ?family3 .
        ?new_service3 ad:subClassOf ?new_service2 .
        ?new_service4 a ?new_service3 .
        ?new_service4 ab:has_label ?new_service4_label .
        ?new_service4 ab:has_description ?new_service4_description .
        }
    '''
    query='''
        prefix ab:<http://yowyob.org/service_onto.owl#>
        prefix ac:<http://www.w3.org/2002/07/owl#>
        prefix ad:<http://www.w3.org/2000/01/rdf-schema#>
        SELECT distinct ?new_service4_description ?new_service4_label  ?new_service4
        WHERE { 
        <'''+service+'''> a ?family .
        ?family ad:subClassOf ?family2 .
        ?family3 ad:subClassOf ?family2 .
        ?new_service4 a ?family3 .
        ?new_service4 ab:has_label ?new_service4_label .
        ?new_service4 ab:has_description ?new_service4_description .
        }
    '''
    return (g.query(query))

@app.get('/')
def index():
    return {'error x002':'invalide endpoint! check the documentation'}

@app.get("/service/search")
def search_service():
    search_input = request.args.get('search_input')

    Result_services=[] # list of the services in decreasing order of pertinance
    similar_services=dict() # list of similar services 
    search_sentence =[]
    PoM =dict() #percentage of Matching (PoM)
    #search_sentence.append(#input('Entrez la phrase a chercher'))
    search_sentence.append(search_input)
    

    #create a liste of words
    word_list=search_sentence
    word_list=remove_punct(search_sentence)
    #word_list=remove_urls(word_list)
    word_list=tokenize(word_list)
    word_list=remove_stopwords(word_list)
    word_list=remove_whitespace(word_list)
    word_list=stemming(word_list)

    #print('the word list is')
    #print(word_list)
    #input('enter to continue')

    #construct queries
    ''''
    1- q1 search for the services having the complete word in one of it properties and take it as Result_services[0]
    2- divide the search_sentence into words (word_list) (excludig words like 'the','is' etc)
    3- q2 we select all the services related to one or many  of those word_list
    '''
    subq1 = search_sentence[0]
    q1='''
        prefix ab:<http://yowyob.org/service_onto.owl#>
        SELECT distinct ?subject ?subject_label ?subject_description
        WHERE {
        ?subject ?predicate ?object

        FILTER regex(?object, "''' + subq1 + '''", "i")
        ?subject ab:has_label ?subject_label .
        ?subject ab:has_description ?subject_description .
        }
        '''

    subq2 = '|'.join(word_list)
    q2='''
        prefix ab:<http://yowyob.org/service_onto.owl#>
        SELECT distinct ?subject ?subject_label ?subject_description
        WHERE {
        ?subject ?predicate ?object
        FILTER regex(?object, "''' + subq2 + '''", "i")
        ?subject ab:has_label ?subject_label .
        ?subject ab:has_description ?subject_description .
    }
    '''

    #execute query
    o1=g.query(q1)
    #print(str(len(o1))+' elements found with complete match')
    o2=g.query(q2)
    #print(str(len(o2))+' elements found with patial match')

    '''4- we calculate the percentage of Matching (PoM) as
            PoM=(number of word Matching) / (total number of words in word_list)

            **NB each word is counted only once
    '''
    for k in o1:
        similar_services[k['subject']]=k
        
    len_word_list = len(word_list)
    for r in o2:
        service = r['subject_label'] + r['subject_description']
        service = (service.replace("/", " ")).lower()
        service = service.split()
        #print(service)
        ##input()
        a=set(word_list).intersection(set(stemming(service)))
        #print(a)
        ##input()
        PoM[r] = (len(a)/len_word_list)*100
        #print((len(a)/len_word_list)*100)

    #sort the list in decreasing oder of PoM
    PoM={k: v for k, v in sorted(PoM.items(), key=lambda item: item[1], reverse=True)}
    for key in PoM:
        similar_services[key['subject']]=key
        #print (key['subject'])
        a = similar_service_of(g,key['subject'])
        #print('smilarity results')
        for i in a:
            similar_services[i['new_service4']]=i
        #input()

    #input()

    #content = {'PoM': PoM, 'similar_service':similar_services}
    return jsonify(similar_services),201


@app.get("/service")
def get_service():
    try: 
        service_id=request.args.get('service_id')
        if not (service_id==None):
            q2='''
            prefix ab:<http://yowyob.org/service_onto.owl#>
            PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX ac:<http://www.w3.org/2002/07/owl#>
            

            SELECT distinct ?subject ?subject_label ?subject_description
            WHERE {
            ?subject rdf:type ac:NamedIndividual .
            ?subject ab:has_id ?id.
            ?subject ab:has_label ?subject_label .
            ?subject ab:has_description ?subject_description .
            FILTER regex(?id, "'''+ service_id +'''", "i")
            }
        '''
        else:
            q2='''
            prefix ab:<http://yowyob.org/service_onto.owl#>
            PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX ac:<http://www.w3.org/2002/07/owl#>
            

            SELECT distinct ?subject ?subject_label ?subject_description
            WHERE {
            ?subject rdf:type ac:NamedIndividual .
            ?subject ab:has_label ?subject_label .
            ?subject ab:has_description ?subject_description .
            }
            '''
        #execute query
        o2=g.query(q2)
        
        result=dict()
        temp=dict()
        for key in o2:
            temp['label']=key['subject_label']
            temp['description']=key['subject_description']
            result[key['subject']]=temp
        return result
    except:
        return 'An unkwon error occured'

@app.post("/service/insert")
def add_service():
    
    #new_node=
    '''
            {
            "service_domain_id": "Pj8cBpY6aAfscq1wtRlkxvSwBfGJY6o9zg",
                    "service_domain_masked_id": "Pj8cBpY6aAfscq1wtRlkxvSwBfGJY6o9zg",
                    "service_domain_label": "FRANCAIS",
                    "service_domain_image": "1191347F727D0D118A403E758D6A2242.png",
                    "service_id": "tbQWljAlvSG8a5xdVA0WZOYMcX4D2NPgIg",
                    "service_masked_id": "tbQWljAlvSG8a5xdVA0WZOYMcX4D2NPgIg",
                    "service_index": "vL1HrZleXAyyajr_fFJBEteVVFi2bKM8Ng",
                    "service_label": "Panorama d’histoire littéraire 2de/1re",
                    "service_description": "20 cartes mentales et 100   quiz pour mémoriser et réviser les   repères historiques et littéraires",
                    "service_images": [
                        "0595BA96310A559735F6C2C27C443FB4.png"
                    ],
                    "service_model": "7545220",
                    "service_unity": "Pieces",
                    "service_color": ",blue",
                    "service_height": 9,
                    "service_weight": 9,
                    "service_dimension": "9*9*9",
                    "service_code": null,
                    "service_publication_date": null,
                    "service_selling_price": 0,
                    "service_promotional_price": 0,
                    "service_selling_currency": "XAF",
                    "service_rank": 0,
                    "service_status": false,
                    "service_in_promotion": false,
                    "service_manufacturer_id": "0NEvT8JXkOHz8LG4cip5TflxGgvIR-6WQA",
                    "service_manufacturer_label": "HATIER",
                    "service_images_sizes": null,
                    "service_packaging": [],
                    "service_created_at": 1619094649809,
                    "service_updated_at": 1619094649809,
                    "service_created_by": null,
                    "service_updated_by": null
            }    
            '''
    
    try:
        new_node = str(request.data,encoding='utf-8')
        New_node(new_node)
        return 'success',201
    except:
        return {"error": "Input data must be JSON"}, 415


@app.post("/service/update")
def update_service():
    
    try:
        new_node = str(request.data,encoding='utf-8')
        return update_node(new_node),201
    except:
        return {"error": "Input data must be JSON"}, 415


@app.get("/service/delete")
def delete_service():
    try:
        service_id=request.args.get('service_id')
        return delete_node(service_id),201
    except:
        return {"error": "An unkwon error occured"}, 415   


@app.post("/ontology/create")
def create_ontology():
    
    try:
        os.system('python index.py')
        os.system('python ontology_creation.py')
        return 'success',201
    except:
        return {"error": "Input data must be JSON"}, 415

if __name__ == '__main__':
    app.run(debug=True)  # run our Flask app