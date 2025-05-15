"""
Script per l'esecuzione automatica dei test definiti in Prolog.

Richiama `swipl` per caricare ed eseguire il file `prolog_demo.pl`,
lanciando il predicato `run_all_tests` e terminando con `halt`.
"""
import subprocess

def run_prolog_tests():
    """
    Esegue i test Prolog definiti in `prolog/prolog_demo.pl` tramite SWI-Prolog.

    Utilizza `subprocess.run` per avviare `swipl` in modalità silenziosa (`-q`),
    carica il file, esegue `run_all_tests`, e termina con `halt`.

    In caso di errore, stampa il messaggio di eccezione.

    Returns:
        None
    """
    print("\n=== ESECUZIONE TEST PROLOG ===")
    try:
        subprocess.run([
            "swipl", "-q", "-s", "prolog/prolog_demo.pl", "-g", "run_all_tests", "-t", "halt"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Errore durante i test Prolog: {e}")

if __name__ == "__main__":
    run_prolog_tests()
