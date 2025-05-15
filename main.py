"""
main.py - Script di avvio per il progetto Mood-Based Music Recommender.

Questo modulo implementa una pipeline interattiva che consente all'utente di:
1. Rigenerare completamente il classificatore supervisionato.
2. Avviare il recommender offline basato sul classificatore salvato.
3. Lanciare una demo SPARQL con eventuale rigenerazione dell'ontologia OWL.
4. Lanciare una demo Prolog con eventuale rigenerazione della knowledge base simbolica.

L'utente può scegliere quali componenti eseguire tramite prompt interattivi.
"""

import os
import subprocess

def run_python(filepath):
    """
    Esegue uno script Python con path assoluto normalizzato.
    
    Args:
        filepath (str): Percorso relativo allo script Python da eseguire.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.normpath(os.path.join(base_dir, filepath))
    print(f"\nEsecuzione: {full_path}")
    subprocess.run(["python", full_path], check=True)

def run_swipl(filepath):
    """
    Esegue uno script Prolog con path assoluto normalizzato.

    Args:
        filepath (str): Percorso relativo allo script .pl da eseguire.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.normpath(os.path.join(base_dir, filepath))
    print(f"\nAvvio Prolog: {full_path}")
    subprocess.run(["swipl", "-q", "-s", full_path], check=True)

def prompt_yes(prompt):
    """
    Visualizza un prompt all'utente e restituisce True se la risposta è 's'.

    Args:
        prompt (str): Testo da visualizzare all'utente.

    Returns:
        bool: True se l'utente risponde 's', False altrimenti.
    """
    return input(f"{prompt} (s/n): ").strip().lower() == "s"

if __name__ == "__main__":
    print("=== AVVIO PIPELINE MOOD RECOMMENDER ===")

    # A) Rigenerazione del classificatore supervisionato
    if prompt_yes("Vuoi rigenerare il classificatore supervisionato? (Operazione lunga)"):
        run_python("clustering/preprocessing.py")
        run_python("clustering/kmeans_clustering.py")
        run_python("classificator/supervised_runner.py")

    # B) Avvio del recommender offline
    if prompt_yes("Vuoi avviare il recommender offline?"):
        print("Verifica che 'classificator/mood_classifier.pkl' sia presente.")
        run_python("recommender/offline_recommender.py")

    # C) Demo SPARQL con rigenerazione opzionale dell'ontologia
    if prompt_yes("Vuoi avviare la demo SPARQL?"):
        if prompt_yes("Vuoi rigenerare l'ontologia?"):
            run_python("sparql/regenerate_ontology.py")
        run_python("sparql/sparql_demo.py")

    # D) Demo Prolog con rigenerazione opzionale della KB simbolica
    if prompt_yes("Vuoi avviare la demo Prolog?"):
        if prompt_yes("Vuoi rigenerare la KB Prolog?"):
            run_python("prolog/regenerate_kb_prolog.py")
        run_python("prolog/prolog_demo_runner.py")

    print("=== PIPELINE COMPLETATA ===")
