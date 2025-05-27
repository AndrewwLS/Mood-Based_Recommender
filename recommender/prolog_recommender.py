"""
Modulo di raccomandazione simbolica basato su regole Prolog.

Funzionalità principali:
- Caricamento delle regole e della knowledge base Prolog
- Interfaccia CLI per l'interrogazione del motore logico
- Raccomandazione simbolica in base a:
    - mood
    - energia (alta/bassa)
    - valence
    - danceability
- Stampa dei risultati in forma leggibile
"""

from pyswip import Prolog
import os
import random

# Inizializzazione motore Prolog
prolog = Prolog()

# Caricamento della knowledge base e delle regole
kb_path = os.path.abspath("prolog/knowledge_base.pl").replace("\\", "/")
rules_path = os.path.abspath("prolog/rules.pl").replace("\\", "/")

list(prolog.query(f"consult('{kb_path}')"))
list(prolog.query(f"consult('{rules_path}')"))

# --- Utility per decodifica ---
def decode_if_bytes(val):
    """Converte valori in stringa se in formato bytes."""
    return val.decode("utf-8") if isinstance(val, bytes) else val

# --- Raccomandazioni simboliche (Track, Artist) ---

def recommend_by_mood(mood, limit=10):
    """
    Restituisce tracce con artista per il mood specificato.

    Args:
        mood (str): Mood richiesto (es. 'felice', 'triste').
        limit (int): Numero massimo di tracce (default: 10).

    Returns:
        list[tuple[str, str]]: Lista di (Track, Artist)
    """
    query = f'recommend_by_mood({mood}, Track, Artist)'
    results = [
        (decode_if_bytes(sol['Track']), decode_if_bytes(sol['Artist']))
        for sol in prolog.query(query)
    ]
    random.shuffle(results)
    return results[:limit]

def relaxing_tracks(limit=10):
    """
    Restituisce tracce rilassanti (energia ≤ 0.5) con artista.
    """
    query = 'is_relaxing(Track, Artist)'
    results = [
        (decode_if_bytes(sol['Track']), decode_if_bytes(sol['Artist']))
        for sol in prolog.query(query)
    ]
    random.shuffle(results)
    return results[:limit]

def energetic_tracks(limit=10):
    """
    Restituisce tracce energetiche (energia ≥ 0.75) con artista.
    """
    query = 'is_energetic(Track, Artist)'
    results = [
        (decode_if_bytes(sol['Track']), decode_if_bytes(sol['Artist']))
        for sol in prolog.query(query)
    ]
    random.shuffle(results)
    return results[:limit]

def danceable_tracks(limit=10):
    """
    Restituisce tracce danceable (danceability ≥ 0.7) con artista.
    """
    query = 'is_danceable(Track, Artist)'
    results = [
        (decode_if_bytes(sol['Track']), decode_if_bytes(sol['Artist']))
        for sol in prolog.query(query)
    ]
    random.shuffle(results)
    return results[:limit]

def happy_tracks_high_valence(limit=10):
    """
    Restituisce tracce felici con valence > 0.8 e artista.
    """
    query = 'happy_track_with_high_valence(Track, Artist)'
    results = [
        (decode_if_bytes(sol['Track']), decode_if_bytes(sol['Artist']))
        for sol in prolog.query(query)
    ]
    random.shuffle(results)
    return results[:limit]

# --- Stampa ordinata dei risultati ---

def stampa_elenco(titolo, lista):
    """
    Stampa una lista numerata con titolo.
    Accetta sia stringhe che tuple (track, artist).
    """
    print(f"\n=== {titolo} ===")
    if not lista:
        print("Nessun risultato trovato.")
    else:
        for i, item in enumerate(lista, start=1):
            if isinstance(item, tuple) and len(item) == 2:
                print(f"{i}. {item[0]} — {item[1]}")
            else:
                print(f"{i}. {item}")

# --- Interfaccia CLI ---

def main():
    """
    Interfaccia a riga di comando per l'utente.

    Consente di interrogare il sistema simbolico su base mood, energia, valence, danceability.
    """
    while True:
        print("\n=== Menu Raccomandatore Simbolico ===")
        print("1. Raccomanda per mood")
        print("2. Tracce rilassanti (energia ≤ 0.5)")
        print("3. Tracce energetiche (energia ≥ 0.75)")
        print("4. Tracce danceable (danceability ≥ 0.7)")
        print("5. Tracce felici con valence > 0.8")
        print("0. Esci")
        choice = input("Scegli un'opzione: ")

        if choice == "1":
            mood = input("Inserisci il mood (es. felice, triste): ")
            stampa_elenco(f"Tracce per mood '{mood}'", recommend_by_mood(mood))
        elif choice == "2":
            stampa_elenco("Tracce rilassanti", relaxing_tracks())
        elif choice == "3":
            stampa_elenco("Tracce energetiche", energetic_tracks())
        elif choice == "4":
            stampa_elenco("Tracce danceable", danceable_tracks())
        elif choice == "5":
            stampa_elenco("Tracce felici con valence alto", happy_tracks_high_valence())
        elif choice == "0":
            break
        else:
            print("Scelta non valida, riprova.")

if __name__ == "__main__":
    main()
