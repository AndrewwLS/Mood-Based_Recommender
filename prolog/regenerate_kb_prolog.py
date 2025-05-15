"""
Modulo per la generazione automatica di una knowledge base Prolog
a partire dal file CSV `clean_tracks.csv`.

Ogni riga del dataset viene trasformata in un fatto Prolog del tipo:
track(Name, Artist, Genre, Danceability, Energy, Valence, Tempo, Mood).

Le stringhe vengono sanificate per garantire compatibilità con la sintassi di Prolog.
L'output viene scritto nel file `knowledge_base.pl` all'interno della cartella `prolog/`.
"""

import os
import re
import unicodedata
import pandas as pd

# Percorsi input/output
INPUT_CSV = "dataset/data/clean_tracks.csv"
OUTPUT_PL = "prolog/knowledge_base.pl"

# Funzione per sanificare le stringhe Prolog-friendly
def sanitize(s):
    """
    Pulisce una stringa rimuovendo caratteri incompatibili con la sintassi Prolog.

    Applica:
    - normalizzazione Unicode in ASCII (es. lettere accentate),
    - rimozione di caratteri speciali non alfanumerici,
    - riduzione di spazi multipli,
    - trim degli spazi iniziali/finali.

    Args:
        s (str): Stringa da sanificare.

    Returns:
        str: Stringa compatibile con Prolog.
    """
    # Normalizza caratteri Unicode in ASCII
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode('utf-8')
    # Rimuove simboli speciali non ammessi
    s = re.sub(r'[^\w\s\-.,!?]', '', s)
    # Rimuove spazi multipli
    s = re.sub(r'\s+', ' ', s)
    return s.strip()

def main():
    """
    Legge il file `clean_tracks.csv`, elabora ogni traccia e genera i fatti Prolog corrispondenti.

    Ogni riga valida viene trasformata in un fatto Prolog della forma:
    track(Name, Artist, Genre, Danceability, Energy, Valence, Tempo, Mood).

    L'output viene scritto nel file `prolog/knowledge_base.pl`. Le righe con titoli vuoti o
    non validi vengono ignorate.

    Returns:
        None
    """
    df = pd.read_csv(INPUT_CSV)

    os.makedirs(os.path.dirname(OUTPUT_PL), exist_ok=True)

    with open(OUTPUT_PL, "w", encoding="utf-8") as f:
        f.write("%% Knowledge base generata automaticamente da clean_tracks.csv\n\n")

        for _, row in df.iterrows():
            track_name = sanitize(str(row["track_name"]))
            if not track_name.strip() or track_name.strip() in ["-", "_"]:
                continue  # Salta brani senza nome valido

            artist = sanitize(str(row["artists"]))
            genre = sanitize(str(row["track_genre"]))
            danceability = round(row["danceability"], 3)
            energy = round(row["energy"], 3)
            valence = round(row["valence"], 3)
            tempo = round(row["tempo"], 2)
            mood = sanitize(str(row["mood"]))

            fact = (
                f'track("{track_name}", "{artist}", "{genre}", '
                f'{danceability}, {energy}, {valence}, {tempo}, "{mood}").\n'
            )

            f.write(fact)

    print(f"Knowledge base Prolog scritta in: {OUTPUT_PL}")

if __name__ == "__main__":
    main()
