"""
Modulo per l'applicazione del clustering KMeans su tracce musicali.

Il dataset viene caricato, normalizzato sulle audio features, e sottoposto a clustering.
Ogni cluster viene poi associato a un mood tramite una mappatura manuale.
Il risultato finale è salvato in un file CSV coerente, con statistiche stampate a video.

Output:
- File CSV con colonne selezionate e mood assegnato
- Distribuzione percentuale dei mood
- Media delle feature audio per ciascun cluster
"""

import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# Percorsi
INPUT_PATH = "dataset/data/dataset.csv"
OUTPUT_PATH = "dataset/data/clean_tracks.csv"

# Colonne da usare nel clustering
AUDIO_FEATURES = [
    'danceability', 'energy', 'valence',
    'tempo', 'acousticness', 'instrumentalness',
    'loudness', 'speechiness', 'liveness'
]

# Colonne finali richieste in output
OUTPUT_COLUMNS = [
    'track_id', 'track_name', 'artists', 'album_name', 'track_genre',
    'popularity', 'duration_ms', 'explicit',
    'danceability', 'energy', 'valence', 'tempo',
    'acousticness', 'instrumentalness', 'loudness',
    'speechiness', 'liveness', 'key', 'mode', 'time_signature',
    'mood'
]

# Mappatura manuale cluster → mood
MOOD_MAP = {
    0: "altro",
    1: "felice",
    2: "aggressivo",
    3: "energetico",
    4: "triste"
}

def run_kmeans_clustering(n_clusters=5):
    """
    Applica il clustering KMeans su un dataset musicale e assegna un mood a ciascuna traccia.

    Il dataset viene filtrato, normalizzato sulle feature audio, clusterizzato con KMeans,
    e i cluster risultanti sono mappati su etichette di mood predefinite.
    I risultati vengono salvati in un nuovo CSV, con stampa delle statistiche principali.

    Args:
        n_clusters (int): Numero di cluster da utilizzare (default: 5).

    Returns:
        None
    """
    # Carica dataset completo
    df = pd.read_csv(INPUT_PATH)

    # Rimuove righe con valori mancanti per le colonne richieste
    df = df.dropna(subset=AUDIO_FEATURES + ['track_name']).drop_duplicates(subset='track_name')

    # Normalizza solo le colonne audio per clustering
    scaler = StandardScaler()
    x_scaled = scaler.fit_transform(df[AUDIO_FEATURES])

    # KMeans clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    df['cluster'] = kmeans.fit_predict(x_scaled)

    # Assegna mood
    df['mood'] = df['cluster'].map(MOOD_MAP)

    # Seleziona e riordina le colonne finali richieste
    df_clean = df[OUTPUT_COLUMNS]

    # Salva CSV coerente
    df_clean.to_csv(OUTPUT_PATH, index=False, float_format='%.6g')
    print(f"File salvato come: {OUTPUT_PATH}")

    # Distribuzione dei mood
    print("\n=== Distribuzione percentuale dei mood ===")
    mood_pct = df_clean['mood'].value_counts(normalize=True) * 100
    print(mood_pct.round(2).to_string())

    # Medie per cluster
    print("\n=== Medie delle feature per cluster ===")
    means = df.groupby('cluster')[AUDIO_FEATURES].mean()
    print(means.round(3))

if __name__ == "__main__":
    run_kmeans_clustering()
