# -*- coding: utf-8 -*-
'''

Other links:
https://pypi.org/project/spacy-dbpedia-spotlight/
'''
from SPARQLWrapper import SPARQLWrapper, JSON
from pprint import pprint
import wikipediaapi,wikipedia


def format_query_term(term):
    return '_'.join(word.capitalize() for word in term.split())


def get_closest_wikipedia_page(search_term):
    # this is to match the correct term from wiki
    wikipedia.set_lang("en")
    print (search_term)
    search_results = wikipedia.search(search_term)
    if search_results:
        # Get the page for the top search result
        try:
            page = wikipedia.page(search_results[0])
            return page.title  # Return the title of the page
        except wikipedia.exceptions.DisambiguationError as e:
            # If a disambiguation page is encountered, return the title of the first option
            print ("Can't match any page in wiki...")
            return e.options[0]
    else:
        return None




def get_dbpedia_properties(entity):
    # search the properties of the entity
    formatted_entity = format_query_term(entity)
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(f"""
    SELECT ?property ?value
    WHERE {{
      dbr:{formatted_entity} ?property ?value .
       FILTER (
            ?property != <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> &&
             ?property != <http://www.w3.org/2000/01/rdf-schema#label> &&
            langMatches(lang(?value), "en") )
    }}
    LIMIT 20
    """)

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    relations = []
    for result in results["results"]["bindings"]:
        relations.append((formatted_entity, result['property']['value'], result['value']['value']))

    return relations


def get_entity_abstract(entity_name):
    formatted_entity = '_'.join(word.capitalize() for word in entity_name.split())
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(f"""
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX dbr: <http://dbpedia.org/resource/>

    SELECT ?abstract
    WHERE {{
      dbr:{formatted_entity} dbo:abstract ?abstract .
      FILTER (lang(?abstract) = 'en')
    }}
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    if results["results"]["bindings"]:
        return results["results"]["bindings"][0]["abstract"]["value"]
    else:
        return "No abstract found."



def get_dbpedia_relation(entity,relation):
    # search the properties of the entity
    formatted_entity = format_query_term(entity)
    formatted_relation = format_query_term(relation).lower()
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(f"""
        SELECT ?entityType
        WHERE {{
          dbr:{formatted_entity} dbo:{formatted_relation} ?entityType .
        }}
        LIMIT 20
        """)

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    relations = []
    for result in results["results"]["bindings"]:
        relations.append((formatted_entity, formatted_relation, result['entityType']['value']))

    return relations


def get_relations(src_name,tgt_name):
    # src_name = get_closest_wikipedia_page(src)
    # tgt_name = get_closest_wikipedia_page(tgt)
    relations = []

    print (src_name,tgt_name)
    if src_name and tgt_name:

        sparql = SPARQLWrapper("http://dbpedia.org/sparql")
        sparql.setQuery(f"""
       SELECT ?relationship
        WHERE {{
          <http://dbpedia.org/resource/{src_name}> 
          ?relationship 
          <http://dbpedia.org/resource/{tgt_name}>
        }}
        LIMIT 4
        """)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        for result in results["results"]["bindings"]:
            relations.append(result['relationship']['value'])

    return relations



def describe_entity(entity_name):
    formatted_entity = '_'.join(word.capitalize() for word in entity_name.split())
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(f"""
    DESCRIBE dbr:{formatted_entity}
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    return results


def construct_query_entity(entity_name, limit=100):
    formatted_entity = '_'.join(word.capitalize() for word in entity_name.split())
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(f"""
    CONSTRUCT {{
      dbr:{formatted_entity} ?property ?value
    }}
    WHERE {{
      dbr:{formatted_entity} ?property ?value
    }}
    LIMIT {limit}
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    return results

print ('Serch relations:')
searched_relations = get_relations("Thierry_Henry", "Arsenal_F.C.")
print (searched_relations)

print ('\n------'*3)
print ('Match Wiki name:')
# Example usage
search_term = "einstein"
wiki_page_title = get_closest_wikipedia_page(search_term)
print("Closest Wikipedia page:", wiki_page_title)

print ('\n------'*3)
print ('Property search:')
entity_name = wiki_page_title
related_entities = get_dbpedia_properties(entity_name)
pprint(related_entities)

print ('\n------'*3)
print ('Relation search:')
entity_name = wiki_page_title
relation_name= "spouse"
related_entities = get_dbpedia_relation(entity_name,relation_name)
pprint(related_entities)
print ('\n------'*3)
print ('Entity abstract:')
entity_name = wiki_page_title
abstract = get_entity_abstract(entity_name)
print(abstract)


print ('\n------'*3)
print ('Describe entity:')
# Example usage
entity_name = "Albert Einstein"  # Replace with your entity of interest
# description = describe_entity(entity_name)
description = construct_query_entity(entity_name, 20)
print(description)
