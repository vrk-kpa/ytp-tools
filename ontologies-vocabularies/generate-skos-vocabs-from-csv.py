#
#

import csv
import sys
from rdflib import Graph, Literal, Namespace, RDF, RDFS, URIRef
from rdflib.namespace import RDF, RDFS, SKOS

uri_prefix = "http://avoindata.fi/onto/2014/01/"


g = Graph()


def parse_csv_file(filename, uri_concept):
  triple_id_counter = 0

  g.bind('skos', SKOS)

  uri = uri_prefix + uri_concept + "#p"
  
  with open(filename, 'rb') as csvfile:
      reader = csv.reader(csvfile, delimiter='\t', quotechar='|')
      for row in reader:
          subj = URIRef(uri + str(triple_id_counter))
          triple_id_counter = triple_id_counter + 1
          g.add((subj, RDF.type, SKOS.Concept))
          g.add((subj, SKOS.prefLabel, Literal(row[2], lang="fi")))

          if row[0]:
              g.add((subj, SKOS.related, URIRef(row[0])))
  return
        


if __name__ == "__main__":

  assert len(sys.argv) == 3

  parse_csv_file(sys.argv[1], sys.argv[2])

  print( g.serialize(format='pretty-xml') )

