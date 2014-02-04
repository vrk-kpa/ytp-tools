#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This script parses Excel spreadsheets into RDF/SKOS vocabularies

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

    uri = uri_prefix + vocab['vocabulary_name']

    parse_concepts_from_sheet(graph, uri+uri_common_part, pandas.read_excel(filename, vocab['sheet'], index_col='ID'))
    parse_metadata_from_sheet(graph, uri, pandas.read_excel(filename, vocab['metadata_sheet']))

    serialize_vocab_into_file(graph, vocab['vocabulary_name'])

  return


# Parse vocabulary concepts from spreadsheet and into a graph
def parse_concepts_from_sheet(graph, uri, sheet_data):

  for index, row in sheet_data.iterrows():

    subject = URIRef(uri + str(index))
    graph.add((subject, RDF.type, SKOS.Concept))
    graph.add((subject, SKOS.prefLabel, Literal(row['Suomeksi'], lang='fi')))
    graph.add((subject, SKOS.prefLabel, Literal(row['Englanniksi'], lang='en')))
    graph.add((subject, SKOS.prefLabel, Literal(row['Ruotsiksi'], lang='sv')))

    if pandas.notnull(row[u'Synonyymi (YSO)']):
      graph.add((subject, SKOS.exactMatch, URIRef(str(row['Synonyymi (YSO)']))))

    if pandas.notnull(row[u'Läheinen käsite']):
      graph.add((subject, SKOS.closeMatch, URIRef(str(row[u'Läheinen käsite']))))

  return

# Parse metadata regarding the SKOS vocabulary itself from a spreadsheet and into a graph
def parse_metadata_from_sheet(graph, uri, sheet_data):

  subject = URIRef(uri+"#conceptscheme")
  graph.add((subject, RDF.type, SKOS.ConceptScheme))

  meta_to_triples(graph, subject, DC.publisher, 'Publisher', sheet_data)
  meta_to_triples(graph, subject, DC.title, 'Title/label', sheet_data)
  meta_to_triples(graph, subject, SKOS.prefLabel, 'Title/label', sheet_data)
  meta_to_triples(graph, subject, DC.description, 'Description', sheet_data)

  graph.add((subject, DC.license, URIRef(str(sheet_data.ix['License','SUOMI']))))

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
