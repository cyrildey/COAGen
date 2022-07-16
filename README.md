# CAOGen: Company Automatic Ontology Creator
CAOGen API provides an acces to the most powerfull automatic ontology creator and manager. You can create, read, update and delete ontologies and its content through this API. 
If you get any difficulty using this API or hqve some propositions or reccommendations to do, please contact us at

## Requirements 
To use CAOGen, you need to have the following 
1. Python 3.x.x
2. pip3
## Installation
Install this library in a [virtualenv](https://virtualenv.pypa.io/en/latest/) using pip. [virtualenv](https://virtualenv.pypa.io/en/latest/) is a tool to create isolated Python environments. The basic problem it addresses is one of dependencies and versions, and indirectly permissions.

With [virtualenv](https://virtualenv.pypa.io/en/latest/), it's possible to install this library without needing system install permissions, and without clashing with the installed system dependencies.
Open a terminal and type the following to set every thing up

```
pip install virtualenv
virtualenv <your-env>
source <your-env>/bin/activate
pip install flask SPARQLWrapper owlready2 nltk rdflib 
python -m pip install sklearn 
sudo ufw allow 5000

```



## End point Example

SmartyPants converts ASCII punctuation characters into "smart" typographic punctuation HTML entities. For example:

|          HTTP Method: Endpoint     |            Parameter              |  Description                       |
|----------------|-------------------------------|-----------------------------|
|get: /service/search|search_input            |search services with a given match          |




## Next step

-   Go to [Official Documentation](www.ongo.cm/caodoc/) for full Documentation.

