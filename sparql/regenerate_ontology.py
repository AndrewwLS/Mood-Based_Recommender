"""
Script per la generazione di un'ontologia OWL a partire dal dataset musicale `clean_tracks.csv`.

Il file genera una rappresentazione RDF/XML contenente entità di tipo `Track`, con proprietà come:
- Nome, artista, genere, mood
- Valori numerici: valence, energy, danceability, tempo

L'ontologia risultante viene salvata in `sparql/mood_ontology.owl`.
"""
import os
import pandas as pd
from rdflib import Graph, Literal, RDF, Namespace, XSD

df = pd.read_csv("dataset/data/clean_tracks.csv")
df.columns = df.columns.str.strip()
df = df.head(1000)

EX = Namespace("http://example.org/mood#")
g = Graph()
g.bind("ex", EX)

for i, row in df.iterrows():
    track_uri = EX["Track" + str(i)]
    g.add((track_uri, RDF.type, EX.Track))
    g.add((track_uri, EX.hasName, Literal(row["track_name"])))
    g.add((track_uri, EX.hasArtist, Literal(row["artists"])))
    g.add((track_uri, EX.hasGenre, Literal(row["track_genre"])))
    g.add((track_uri, EX.hasMood, Literal(row["mood"])))

    g.add((track_uri, EX.hasValence, Literal(row["valence"], datatype=XSD.float)))
    g.add((track_uri, EX.hasEnergy, Literal(row["energy"], datatype=XSD.float)))
    g.add((track_uri, EX.hasDanceability, Literal(row["danceability"], datatype=XSD.float)))
    g.add((track_uri, EX.hasTempo, Literal(row["tempo"], datatype=XSD.float)))

os.makedirs("sparql", exist_ok=True)
g.serialize(destination="sparql/mood_ontology.owl", format="xml")
print("Ontologia salvata in 'sparql/mood_ontology.owl'")
