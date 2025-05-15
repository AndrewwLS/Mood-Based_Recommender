"""
Modulo per il caricamento di un'ontologia OWL RDF e l'esecuzione di una query SPARQL
che restituisce un insieme di tracce con mood 'felice'.

Utilizza `rdflib` per il parsing e l'interrogazione dell'ontologia.
"""

from rdflib import Graph

def load_ontology():
    """
    Carica l'ontologia musicale OWL dal file RDF/XML.

    Il file `sparql/mood_ontology.owl` deve esistere ed essere conforme al vocabolario RDF previsto.

    Returns:
        rdflib.Graph: Grafo RDF caricato.
    """
    g = Graph()
    g.parse("sparql/mood_ontology.owl", format="xml")
    return g

def run_query_felici(graph):
    """
    Esegue una query SPARQL per ottenere tracce con mood 'felice'.

    Estrae e stampa per ciascuna traccia:
    - Nome
    - Artista
    - Genere
    - Mood

    La query è limitata a 5 risultati.

    Args:
        graph (rdflib.Graph): Grafo RDF contenente l'ontologia caricata.

    Returns:
        None
    """
    query = """
    PREFIX : <http://example.org/mood#>

    SELECT ?name ?artist ?genre ?mood
    WHERE {
      ?track a :Track ;
             :hasMood "felice" ;
             :hasName ?name ;
             :hasArtist ?artist ;
             :hasGenre ?genre ;
             :hasMood ?mood .
    }
    LIMIT 5
    """
    results = graph.query(query)
    for row in results:
        print(f"'{row.name}' di {row.artist} | Genere: {row.genre} | Mood: {row.mood}")
