"""
Script dimostrativo per interrogare l'ontologia musicale OWL
e visualizzare un sottoinsieme di tracce con mood 'felice'.

Carica l'ontologia RDF da file e lancia la query SPARQL definita in `ontology_module`.
"""

from ontology_module import load_ontology, run_query_felici

if __name__ == "__main__":
    print("Esecuzione query SPARQL sulle tracce 'felici'...")
    g = load_ontology()
    run_query_felici(g)
