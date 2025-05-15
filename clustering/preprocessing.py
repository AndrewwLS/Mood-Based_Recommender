"""
Modulo per il preprocessing di un dataset musicale.

Effettua:
- selezione e pulizia delle colonne numeriche rilevanti,
- rimozione di duplicati sulla base del nome della traccia,
- normalizzazione delle feature numeriche con StandardScaler,
- salvataggio del dataset normalizzato su file.
"""

import pandas as pd
from sklearn.preprocessing import StandardScaler

def preprocess_dataset(path_csv: str = "dataset/data/dataset.csv",
                       save_to: str = "dataset/data/normalized_dataset.csv") -> pd.DataFrame:
    """
    Preprocessa un dataset musicale: seleziona colonne rilevanti, normalizza le feature
    numeriche e salva il risultato su file.

    Il dataset risultante conterrà solo tracce non duplicate (per nome) e con valori validi
    nelle colonne specificate. Le feature numeriche vengono scalate tramite StandardScaler.

    Args:
        path_csv (str): Percorso al file CSV di input.
        save_to (str): Percorso dove salvare il file CSV normalizzato.

    Returns:
        pd.DataFrame: DataFrame contenente i dati normalizzati.
    """

    # Caricamento dati
    df = pd.read_csv(path_csv)

    # Colonne da mantenere
    columns_to_keep = [
        'track_name',
        'danceability', 'energy', 'valence',
        'acousticness', 'instrumentalness', 'liveness',
        'speechiness', 'tempo'
    ]

    # Filtro e pulizia
    df_filtered = df[columns_to_keep].dropna()

    # Rimozione dei track_name duplicati (mantiene la prima occorrenza)
    df_filtered = df_filtered.drop_duplicates(subset='track_name', keep='first')

    # Normalizzazione delle feature
    features = df_filtered.drop(columns=['track_name'])
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)

    # Creazione del DataFrame normalizzato
    df_scaled = pd.DataFrame(scaled_features, columns=features.columns)
    df_scaled.insert(0, 'track_name', df_filtered['track_name'].values)

    # Salvataggio su file
    df_scaled.to_csv(save_to, index=False)

    return df_scaled

# Test manuale
if __name__ == "__main__":
    df_scaled = preprocess_dataset()
    print("Dataset normalizzato e deduplicato salvato in 'dataset/data/normalized_dataset.csv'")
    print(df_scaled.head())
