'''
this file is to insert a new node in the ontology
'''
#input : the node to be inserted (in JSON format)
import time
from owlready2 import *
import json
import types
from text_preprocessing import *

onto_path.append('onto_path')

# load the ontology
onto = get_ontology("./onto_path/service_onto.owl").load()

# select all the individuals
individuals = onto.individuals()

#function to calculate the pearson similarity between two lists
def person_sim(A,B):
    AnB= set(A).intersection(set(B))
    AuB= set(A).union(set(B))
    return len(AnB)/len(AuB)

#function to prepare nodes data
def pre(data):
    #data=data.replace(' ','')
    data=data.replace('null','none')
    data=data.replace("\'", "")
    data=data.split(',')
    a=[]
    for d in data:
        d=d.split(':')
        try:
            a.append(d[1])
        except IndexError:
            pass
    data=a
    data=remove_punct(data)
    data=remove_urls(data)
    data=tokenize(data)
    data=remove_stopwords(data)
    data=remove_whitespace(data)
    data=stemming(data)
    return data

# calculate their similarty with the node to be insert an select the max
def best_family(new_node):
    # select all the individuals
    individuals = onto.individuals()
    
    #do some pretreatment on the nodes
    new_node= pre(new_node)
    #input(new_node)
    max = -1
    service = None
    print('insertion started....')
    i=0
    for ind in individuals:
        data = pre(ind.has_all_data[0])
        sim = person_sim(new_node,data)
        #print(i,' treated')
        if (sim > max):
            max=sim
            service=ind
        i+=1
        #print(sim)
    #input(new_node)
    #print(pre(ind.has_all_data[0]))
    #input('maxi')
    #input(max)
    #print(service.has_label)
    #we return the best service
    return service

# create a class for the new node and connect it to the class of the max
def New_node(new_node):

    #i=len(individuals)+1
    start = time.time()

    best_famil = best_family(new_node).is_a[0]

    best_famil1 = best_famil.is_a[0]

    new_node=str(new_node).strip("'<>() ").replace('\'', '\"')
    
    new_node = json.loads(new_node)

    x ='new_family'+str(new_node['service_id'])

    Node1 = types.new_class(x, (best_famil1,))

    Node = types.new_class('new_service_family_'+ str(new_node['service_label']), (Node1,))

    best_famil.is_a = [Node1]

    # create an instance with the new node and attache  to the new class
    instance = Node('new_service')

    instance.has_all_data.append(str(new_node))

    instance.has_domain_id.append(str(new_node['service_domain_id']))

    instance.has_id.append(str(new_node['service_id']))
    
    instance.has_label.append(str(new_node['service_label']))
    
    instance.has_description.append(str(new_node['service_description']))
    
    #instance.has_images.append(service['service_images']]
    
    instance.has_model.append(str(new_node['service_model']))
    
    instance.has_unity.append(str(new_node['service_unity']))
    
    instance.has_color.append(str(new_node['service_color']))
    
    instance.has_height.append(int(new_node['service_height']))

    instance.has_weight.append(int(new_node['service_weight']))

    instance.has_dimension.append(str(new_node['service_dimension']))
    
    instance.has_code.append(str(new_node['service_code']))
    
    instance.has_publication_date.append(str(new_node['service_publication_date']))
    
    instance.has_selling_price.append(int(new_node['service_selling_price']))

    instance.has_promotional_price.append(int(new_node['service_promotional_price']))
    
    instance.has_selling_currency.append(new_node['service_selling_currency'])
    
    instance.has_status.append(str(new_node['service_status']))
    
    instance.is_in_promotion.append(str(new_node['service_in_promotion']))
    
    instance.has_manufacturer_id.append(str(new_node['service_manufacturer_id']))
    
    instance.has_manufacturer_label.append(str(new_node['service_manufacturer_label']))

    onto.save("./onto_path/service_onto.owl")

    end = time.time()

    print('execution time: ',end-start)

#delete an individual
def delete_node(node_id):
    # select all the individuals
    individuals = onto.individuals()
    
    for individual in individuals:
        if individual.has_id[0] == node_id:
            #print(individual.has_label[0])
            destroy_entity(individual.is_a[0])
            destroy_entity(individual)
            onto.save("./onto_path/service_onto.owl")
            return 'success'
    return 'not found'

#update an element in the ontology 
#inpput: node data should be in the form of a json containing all the fields
def update_node(node_data):
    # select all the individuals
    individuals = onto.individuals()
    
    node_data=str(node_data).strip("'<>() ").replace('\'', '\"')
    
    node_data = json.loads(node_data)

    for individual in individuals:
        if individual.has_id[0] == node_data['service_id']:
            #print(individual.has_label[0])

            if not (node_data==None): individual.has_all_data=[(str(node_data))]

            if not (node_data['service_domain_id']==None): individual.has_domain_id=[(str(node_data['service_domain_id']))]
            
            if not (node_data['service_label']==None): individual.has_label=[(str(node_data['service_label']))]
            
            if not (node_data['service_description']==None): individual.has_description=[(str(node_data['service_description']))]
            
            #if not (node_data['service_images']==None): individual.has_images=[(service['service_images']]
            
            if not (node_data['service_model']==None): individual.has_model=[(str(node_data['service_model']))]
            
            if not (node_data['service_unity']==None): individual.has_unity=[(str(node_data['service_unity']))]
            
            if not (node_data['service_color']==None): individual.has_color=[(str(node_data['service_color']))]
            
            if not (node_data['service_height']==None): individual.has_height=[(int(node_data['service_height']))]

            if not (node_data['service_weight']==None): individual.has_weight=[(int(node_data['service_weight']))]

            if not (node_data['service_dimension']==None): individual.has_dimension=[(str(node_data['service_dimension']))]
            
            if not (node_data['service_code']==None): individual.has_code=[(str(node_data['service_code']))]
            
            if not (node_data['service_publication_date']==None): individual.has_publication_date=[(str(node_data['service_publication_date']))]
            
            if not (node_data['service_selling_price']==None): individual.has_selling_price=[(int(node_data['service_selling_price']))]

            if not (node_data['service_promotional_price']==None): individual.has_promotional_price=[(int(node_data['service_promotional_price']))]
            
            if not (node_data['service_selling_currency']==None): individual.has_selling_currency=[(node_data['service_selling_currency'])]
            
            if not (node_data['service_status']==None): individual.has_status=[(str(node_data['service_status']))]
            
            if not (node_data['service_in_promotion']==None): individual.is_in_promotion=[(str(node_data['service_in_promotion']))]
            
            if not (node_data['service_manufacturer_id']==None): individual.has_manufacturer_id=[(str(node_data['service_manufacturer_id']))]
            
            if not (node_data['service_manufacturer_label']==None): individual.has_manufacturer_label=[(str(node_data['service_manufacturer_label']))]

            onto.save("./onto_path/service_onto.owl")
            return 'success'
    return 'not found'
#tests
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

#New_node(new_node)