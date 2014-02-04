#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' This script parses Excel spreadsheets into RDF/SKOS vocabularies '''

import logging
import sys
import pandas
import numpy
from rdflib import Graph, Literal, Namespace, RDF, RDFS, URIRef
from rdflib.namespace import RDF, RDFS, SKOS, DC

logging.basicConfig()

uri_prefix = "http://avoindata.fi/onto/"
uri_common_part = "#p"

# Parse Excel spreadsheet and create SKOS vocabularies from each sheet
def convert_spreadsheet_into_vocabularies(filename):

  vocabs = [
    {'sheet': 'AIHE', 'vocabulary_name': 'topic', 'metadata_sheet':'Ontologian metatiedot'},
    {'sheet': u'SISÄLTÖTYYPPI', 'vocabulary_name': 'content_type', 'metadata_sheet':'Ontologian metatiedot'},
  ]
  
  for vocab in vocabs:

    graph = Graph()
    graph.bind('skos', SKOS)
    graph.bind('rdfs', RDFS)
    graph.bind('dc11', DC)

    base_uri = uri_prefix + vocab['vocabulary_name']
    parse_concepts_from_sheet(graph, base_uri, pandas.read_excel(filename, vocab['sheet'], index_col='ID'))
    parse_metadata_from_sheet(graph, base_uri, pandas.read_excel(filename, vocab['metadata_sheet']))

    serialize_vocab_into_file(graph, vocab['vocabulary_name'])

  return


# Parse vocabulary concepts from spreadsheet and into a graph
def parse_concepts_from_sheet(graph, base_uri, sheet_data):

  for index, row in sheet_data.iterrows():

    concept = URIRef(base_uri + uri_common_part + str(index))
    graph.add((concept, RDF.type, SKOS.Concept))
    graph.add((concept, SKOS.inScheme, URIRef(base_uri + '/conceptscheme')))

    graph.add((concept, SKOS.broader, URIRef(base_uri + '#term')))
    graph.add((URIRef(base_uri + '#term'), SKOS.narrower, concept))

    graph.add((concept, SKOS.prefLabel, Literal(row['Suomeksi'], lang='fi')))
    graph.add((concept, SKOS.prefLabel, Literal(row['Englanniksi'], lang='en')))
    graph.add((concept, SKOS.prefLabel, Literal(row['Ruotsiksi'], lang='sv')))

    if pandas.notnull(row[u'Synonyymi (YSO)']):
      graph.add((concept, SKOS.exactMatch, URIRef(str(row['Synonyymi (YSO)']))))

    if pandas.notnull(row[u'Läheinen käsite']):
      graph.add((concept, SKOS.closeMatch, URIRef(str(row[u'Läheinen käsite']))))

  return

# Parse metadata regarding the SKOS vocabulary itself from a spreadsheet and into a graph
def parse_metadata_from_sheet(graph, base_uri, sheet_data):

  concept_scheme = URIRef(base_uri + '/conceptscheme')
  graph.add((concept_scheme, RDF.type, SKOS.ConceptScheme))

  meta_to_triples(graph, concept_scheme, DC.publisher, 'Publisher', sheet_data)
  meta_to_triples(graph, concept_scheme, DC.title, 'Title/label', sheet_data)
  meta_to_triples(graph, concept_scheme, SKOS.prefLabel, 'Title/label', sheet_data)
  meta_to_triples(graph, concept_scheme, DC.description, 'Description', sheet_data)
  graph.add((concept_scheme, DC.license, URIRef(str(sheet_data.ix['License','SUOMI']))))

  # Create top concept that ties all terms together
  top_term = URIRef(base_uri + '#term')
  graph.add((top_term, RDF.type, SKOS.Concept))
  graph.add((top_term, SKOS.topConceptOf, concept_scheme))
  graph.add((concept_scheme, SKOS.hasTopConcept, top_term))
  graph.add((top_term, SKOS.prefLabel, Literal('olio', lang='fi')))
  graph.add((top_term, SKOS.prefLabel, Literal('object', lang='en')))
  graph.add((top_term, SKOS.prefLabel, Literal('entitet', lang='sv')))
  graph.add((top_term, SKOS.inScheme, concept_scheme))

  return

# Convert multilingual metadata fields into triples. This trims trailing whitespace from labels
def meta_to_triples(graph, subject, predicate, metafield, sheet_data):

  # Known issue: this does not handle correctly cells that have only whitespace in them
  if pandas.notnull(sheet_data.ix[metafield,'SUOMI']):
    graph.add((subject, predicate, Literal(sheet_data.ix[metafield,'SUOMI'].rstrip(), lang='fi')))
  if pandas.notnull(sheet_data.ix[metafield,'ENGLANTI']):
    graph.add((subject, predicate, Literal(sheet_data.ix[metafield,'ENGLANTI'].rstrip(), lang='en')))
  if pandas.notnull(sheet_data.ix[metafield,'RUOTSI']):
    graph.add((subject, predicate, Literal(sheet_data.ix[metafield,'RUOTSI'].rstrip(), lang='sv')))

  return

# Serialize vocabulary as RDF/XML into a file
def serialize_vocab_into_file(graph, vocabulary_name):
  filename = 'avoindatafi_' + vocabulary_name + '.rdf'
  graph.serialize(filename, format='pretty-xml')
  print "Wrote file", filename
  return


if __name__ == "__main__":
  # Must get filename as arg
  assert len(sys.argv) == 2
  convert_spreadsheet_into_vocabularies(sys.argv[1])
