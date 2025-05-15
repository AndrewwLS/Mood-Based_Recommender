"""
Script di utilità per ispezionare un dataset musicale clusterizzato per mood.

Permette di visualizzare un campione di tracce per ciascun mood presente nel dataset,
stampando le principali feature audio associate.
"""

import pandas as pd

# Percorso al file di input
INPUT_PATH = "dataset/data/clean_tracks.csv"

def inspect_clusters(n_samples=5):
    """
    Stampa a video un campione di tracce (per ciascun mood) dal dataset clusterizzato.

    Il campione è casuale ma riproducibile (random_state=42) e 
    mostra le feature musicali principali.
    Verifica anche che tutte le colonne necessarie siano presenti nel file CSV.

    Args:
        n_samples (int): Numero di tracce da mostrare per ciascun mood (default: 5).

    Raises:
        ValueError: Se mancano colonne essenziali nel file caricato.

    Returns:
        None
    """

    # Carica il dataset già clusterizzato e pulito
    df = pd.read_csv(INPUT_PATH)

    # Verifica colonne richieste
    required_cols = {"track_name", "mood", "danceability", "energy", "valence",
                     "acousticness", "instrumentalness", "liveness", "speechiness", "tempo"}
    if not required_cols.issubset(df.columns):
        raise ValueError("Il file non contiene tutte le colonne richieste.")

    # Raggruppa per mood
    moods = sorted(df["mood"].unique())

    for mood in moods:
        print(f"\n=== Mood: {mood.upper()} ===")
        mood_df = df[df["mood"] == mood]
        n_select = min(n_samples, len(mood_df))
        sample = mood_df.sample(n=n_select, random_state=42)

        print(sample[[
            "track_name", "danceability", "energy", "valence",
            "acousticness", "instrumentalness", "liveness",
            "speechiness", "tempo"
        ]].round(3).to_string(index=False))

if __name__ == "__main__":
    inspect_clusters(n_samples=5)
