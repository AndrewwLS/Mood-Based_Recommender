"""
Modulo per la raccomandazione musicale basata su similarità audio e predizione del mood.

Funzionalità principali:
- Caricamento del dataset pulito e del classificatore preaddestrato
- Predizione del mood tramite modello supervisionato
- Raccomandazione di tracce simili secondo mood, genere e durata
- Calcolo della distanza pesata su feature audio
- Generazione di spiegazioni per ogni raccomandazione
"""

import pickle
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from dotenv import load_dotenv
import numpy as np

# Caricamento risorse
load_dotenv()

with open("classificator/mood_classifier.pkl", "rb") as f:
    model, mood_encoder = pickle.load(f)

df = pd.read_csv("dataset/data/clean_tracks.csv")
df["artists_name"] = df["artists"]  # salva nome originale

# Label encoding
artist_encoder = LabelEncoder()
df["artists"] = artist_encoder.fit_transform(df["artists"].astype(str))

genre_encoder = LabelEncoder()
df["track_genre"] = genre_encoder.fit_transform(df["track_genre"].astype(str))

# Feature e pesi
primary_filters = ["mood", "duration_ms", "track_genre"]
secondary_features = [
    "valence", "energy", "danceability", "tempo",
    "acousticness", "instrumentalness", "speechiness"
]
feature_weights = {
    "valence": 2.0,
    "energy": 2.0,
    "danceability": 1.0,
    "tempo": 1.0,
    "acousticness": 1.0,
    "instrumentalness": 1.0,
    "speechiness": 1.0,
}
features_model = [
    "valence", "energy", "danceability", "tempo", "acousticness",
    "instrumentalness", "speechiness", "artists", "duration_ms", "track_genre"
]

# Trova traccia
def trova_traccia(nome):
    """
    Cerca una traccia nel dataset dato un nome (parziale o completo).

    Se viene trovata una sola corrispondenza, la restituisce direttamente.
    Se ci sono più risultati, chiede all’utente quale selezionare.
    Se non trova nulla o l’input è invalido, restituisce None.

    Args:
        nome (str): Nome (o parte del nome) della traccia da cercare.

    Returns:
        pd.Series | None: Traccia selezionata o None.
    """
    risultati = df[df["track_name"].str.contains(nome, case=False, na=False)]
    if risultati.empty:
        print("Nessuna traccia trovata.")
        return None
    if len(risultati) == 1:
        return risultati.iloc[0]
    print("\nTrovate più tracce:")
    for i, row in risultati.iterrows():
        print(f"[{i}] {row['track_name']} di {row['artists_name']}")
    try:
        scelta = int(input("Seleziona l'indice della traccia: "))
        return risultati.loc[scelta]
    except:
        print("Selezione non valida.")
        return None

# Predizione mood
def predici_mood(traccia_originale):
    """
    Predice il mood di una traccia usando il classificatore supervisionato.

    Codifica le feature categoriali e applica il modello addestrato per stimare il mood.

    Args:
        traccia_originale (pd.Series): Rappresentazione della traccia.

    Returns:
        str: Etichetta del mood predetto.
    """
    traccia = traccia_originale.copy()
    if isinstance(traccia["artists"], str):
        traccia["artists"] = artist_encoder.transform([traccia["artists"]])[0]
    if isinstance(traccia["track_genre"], str):
        traccia["track_genre"] = genre_encoder.transform([traccia["track_genre"]])[0]
    features_df = pd.DataFrame([traccia[features_model]])
    return model.predict(features_df)[0]

# Spiegazione
def genera_spiegazione(base_row, candidate_row):
    """
    Genera una spiegazione testuale della raccomandazione basata sulla similarità tra tracce.

    La spiegazione include fattori come mood, genere, durata e la feature audio più simile
    secondo distanza pesata.

    Args:
        base_row (pd.Series): Traccia di riferimento.
        candidate_row (pd.Series): Traccia raccomandata.

    Returns:
        str: Motivazione testuale.
    """
    motivazioni = []

    if base_row["mood"] == candidate_row["mood"]:
        motivazioni.append("stesso mood")
    if base_row["track_genre"] == candidate_row["track_genre"]:
        motivazioni.append("genere musicale identico")
    if abs(base_row["duration_ms"] - candidate_row["duration_ms"]) <= 0.1 * base_row["duration_ms"]:
        motivazioni.append(
    f"durata simile ({abs(base_row['duration_ms'] - candidate_row['duration_ms']) / 1000:.1f}s)"
)


    # Similarità feature più forte
    differenze = {
        feat: abs(base_row[feat] - candidate_row[feat]) * feature_weights[feat]
        for feat in secondary_features
    }
    best_feat = min(differenze, key=differenze.get)
    motivazioni.append(f"{best_feat} simile (Δ={differenze[best_feat]:.3f})")

    return (
    "Motivazione principale: " + motivazioni[-1] + ". Altri fattori: " +
    ", ".join(motivazioni[:-1])
)


# Raccomandazione
def raccomanda_simili(traccia_originale, top_n=5):
    """
    Raccomanda le tracce più simili a quella data, utilizzando un filtro per mood,
    genere e durata, e una distanza pesata sulle feature audio secondarie.

    Se il filtro stretto restituisce zero risultati, esegue un fallback rilassando i vincoli.

    Args:
        traccia_originale (pd.Series): Traccia da cui partire.
        top_n (int): Numero di raccomandazioni da restituire (default: 5).

    Returns:
        None
    """
    traccia = traccia_originale.copy()
    mood_pred = predici_mood(traccia)
    mood_label = mood_encoder.inverse_transform([mood_pred])[0]
    base_durata = traccia["duration_ms"]
    base_genere = traccia["track_genre"]

    # Primo filtro
    df_filtrato = df[
        (df["mood"] == mood_label) &
        (df["track_genre"] == base_genere) &
        (df["duration_ms"].between(base_durata * 0.9, base_durata * 1.1)) &
        (df["track_id"] != traccia["track_id"])
    ].copy()

    # Fallback se vuoto
    if df_filtrato.empty:
        print("Nessuna raccomandazione stretta trovata, rilasso i filtri (solo stesso mood)...")
        df_filtrato = df[
            (df["mood"] == mood_label) &
            (df["track_id"] != traccia["track_id"])
        ].copy()
        if df_filtrato.empty:
            print("Nessuna raccomandazione possibile.")
            return

    # Calcolo distanza pesata
    x_input = traccia[secondary_features].values.reshape(1, -1)
    x_candidati = df_filtrato[secondary_features].values
    weights = np.array([feature_weights[feat] for feat in secondary_features])
    df_filtrato["distanza"] = ((x_candidati - x_input) ** 2 * weights).sum(axis=1) ** 0.5

    raccomandazioni = df_filtrato.sort_values(by="distanza").head(top_n)

    print(
    f"\nTracce consigliate simili a '{traccia['track_name']}' di "
    f"{traccia['artists_name']}' (mood: {mood_label}):\n"
)

    for _, row in raccomandazioni.iterrows():
        print(f"- {row['track_name']} di {row['artists_name']} [distanza: {row['distanza']:.3f}]")
        print(f"  {genera_spiegazione(traccia, row)}")

def main():
    """
    Punto di ingresso del programma.

    Chiede all'utente una traccia e avvia il processo di raccomandazione.
    """
    nome = input("Inserisci il nome (o parte del nome) di una traccia: ").strip()
    traccia = trova_traccia(nome)
    if traccia is not None:
        raccomanda_simili(traccia)

if __name__ == "__main__":
    main()
