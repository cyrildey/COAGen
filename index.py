import json
from text_preprocessing import *
import time
#from igraph import *
# function to take the services and return an array of words in each service
def json_to_list(json_file):
    serviceArray=[]
    with open(json_file, encoding="utf8") as jsonFile:
        jsonObject = json.load(jsonFile)
        jsonFile.close()
        for element in jsonObject:
            serviceArray.append(jsonObject[element])
    return serviceArray[2]['content']['services']

#remove sub arrays and list and convert to string
def remov_inner_arrays(jsonObject):
    for i in range(len(jsonObject)):
        for j in jsonObject[i]:
            temp_j=[]
            if (type(jsonObject[i][j]) is list) or (type(jsonObject[i][j]) is dict):
                temp=''
                for e in jsonObject[i][j]:
                    temp = temp + str(e)+', '
                temp_j=temp
            else:
                temp_j=jsonObject[i][j]
            jsonObject[i][j]=temp_j
    return jsonObject

#function to transform the object to array of arrays
def object_to_array(objects):
    result=[]
    for object in objects:
        sub_result=[]
        for attribute in object:
            sub_result.append(str(object[attribute]))
        result.append(sub_result)
    return result

#function to create a file and write inside
def write_in_file(content, file):
    myFile = open(file, "w+",encoding="utf8")
    myFile.write(str(content))
    myFile.close()

'''
    we construct and dict for identification ie
    1=>service_id1
    2=>service_id2
'''
def construct_identification(jsonobject):
    result=[]
    i=0
    for service in  jsonobject:
        el = (service['service_id'],i)
        result.append(el)
        i+=1
    return dict(result)
    
#calculate the maximum in a 2 d list and return the value and the position
def biggest(distance_matrix):
    (de,vers,maxi) = (None,None,-1)
    for i in distance_matrix:
        for j in distance_matrix[i]:
            if(distance_matrix[i][j] > maxi):
                (de,vers,maxi) = (i,j,distance_matrix[i][j])
    return (de,vers,maxi)

'''
main part of the program
'''
start= time.time()
'''
1. we do the preprocessing
'''
#jsonObject = json_to_list('elements to take from services.json')
jsonObject = json_to_list('all services of yowyob.json')
jsonObject_save = jsonObject
identification_of_services = construct_identification(jsonObject)

print('... printing identification matrix')
end= time.time()
print('Execution time:')
print(end-start)
start= time.time()

#print(identification_of_services)


jsonObject = remov_inner_arrays(jsonObject) 
jsonObject = object_to_array(jsonObject) 

print('... service file read successfuly ...')
end= time.time()
print('Execution time:')
print(end-start)
start= time.time()
print('... pretreatement started ...')

#size=len(jsonObject)
size=1000

for i in range(size):
    jsonObject[i]=remove_punct(jsonObject[i])
    jsonObject[i]=remove_urls(jsonObject[i])
    jsonObject[i]=tokenize(jsonObject[i])
    jsonObject[i]=remove_stopwords(jsonObject[i])
    jsonObject[i]=remove_whitespace(jsonObject[i])
    #jsonObject[i]=stemming(jsonObject[i])

print('... pretreatement done successfuly ...')
end= time.time()
print('Execution time:')
print(end-start)
start= time.time()
print('calculationg similarity matrix ...')

distace_matrix=dict()
#for i in range(size):
for i in range(size):
    #for j in range(size):
    distance_row=dict()
    for j in range(size):
        AnB= set(jsonObject[i]).intersection(jsonObject[j])
        AuB= set(jsonObject[i]).union(jsonObject[j])
        distance_row[jsonObject_save[j]['service_id']] = len(AnB)/len(AuB)
    distace_matrix[jsonObject_save[i]['service_id']] = distance_row
    #print(distance_row)
    #print(': ' + str(i) + str(j))


#fill put the distance from every service to itself to 0
for i in range(size):
    var=jsonObject_save[i]['service_id']
    distace_matrix[var][var]=0


print('... similarity matrix caculated successfuly ...')
end= time.time()
print('Execution time:')
print(end-start)
start= time.time()
'''
    we create the graph
    we represent it as a list of ajensence
    (A->B)
    (AB->C)
'''
print('... graph creation started ...')
graph = dict() #we initialise the graph

number=0
(de,vers,maxi) = biggest(distace_matrix) #take the maximum distance
while (maxi > 0):
    (de,vers,maxi) = biggest(distace_matrix) #take the maximum distance
    new_node= de+'++'+vers
    graph[de] = new_node #we add those 2 nodes in the graph
    graph[vers] = new_node #we add those 2 nodes in the graph

    #we create a new element with the maximum of the the previous
    news = dict()
    
    for i in distace_matrix:
        try:
            news[i]=((distace_matrix[de][i] + distace_matrix[vers][i])/2)
            distace_matrix[i][new_node]=((distace_matrix[de][i] + distace_matrix[vers][i])/2)
        except IndexError:
            pass
    distace_matrix[new_node] = news
    distace_matrix[new_node][new_node] = 0

    #we remove the already added lines
    try:
        for i in distace_matrix:
            del distace_matrix[i][de]
            del distace_matrix[i][vers]
        del distace_matrix[de]
        del distace_matrix[vers]
    except KeyError:
        pass
    print(number,' nodes created')
    #print(de,vers)
    #print('new graph')
    #print(graph) 
    write_in_file(distace_matrix,"distance_list.txt")
    write_in_file(graph,"graph.txt")
    #input('type enter to continue')
    number +=1

end= time.time()
print('Execution time:')
print(end-start)
start= time.time()

print('...graph created succesfuly...\n creating files')
write_in_file(graph,"graph.txt")
write_in_file(jsonObject,"service_list.txt")
write_in_file(distace_matrix,"distance_list.txt")
write_in_file(identification_of_services,"identification_of_services.txt")


'''
create graph using igraph

g = Graph(len(jsonObject)-1)
for i in range(len(distace_matrix[i])):
    for j in range(len(distace_matrix[i][j])):
        g.add_edges([(i,j), (j,i)])
layout = g.layout("kk")
plot(g, layout = layout)
'''


