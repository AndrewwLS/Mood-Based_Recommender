"""
Script per valutare l'efficacia del clustering KMeans su un dataset musicale
variando il numero di cluster (k) in un intervallo specificato.

Il codice calcola e salva le seguenti metriche per ciascun valore di k:
- Inertia
- Silhouette Score
- Calinski-Harabasz Index
- Davies-Bouldin Index

I risultati vengono salvati in CSV e visualizzati come grafici PNG.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score

# Percorsi
INPUT_PATH = "dataset/data/dataset.csv"
PLOTS_DIR = "clustering/outputs/plots"

# Flag di dimensione di campioni

os.makedirs(PLOTS_DIR, exist_ok=True)

def evaluate_kmeans_range(k_range=range(2, 11), sample_size=30000):
    """
    Valuta il clustering KMeans su un dataset musicale per un range di valori di k.

    Per ciascun valore di k nel range specificato, il dataset viene normalizzato e
    sottoposto a KMeans. Vengono calcolate quattro metriche di valutazione, salvate
    in CSV e visualizzate in grafici PNG.

    Args:
        k_range (iterable): Intervallo di valori per k (numero di cluster).
        sample_size (int): Numero massimo di tracce da campionare per la valutazione.

    Returns:
        None
    """

    # Caricamento e preparazione dati
    df = pd.read_csv(INPUT_PATH)

    columns_to_use = [
        'track_name',
        'danceability', 'energy', 'valence',
        'acousticness', 'instrumentalness', 'liveness',
        'speechiness', 'tempo'
    ]

    df = df[columns_to_use].dropna().drop_duplicates(subset='track_name')

    # Campionamento
    if sample_size < len(df):
        df = df.sample(n=sample_size, random_state=42).reset_index(drop=True)

    features = df.drop(columns=['track_name'])

    # Normalizzazione
    scaler = StandardScaler()
    x_scaled = scaler.fit_transform(features)

    # Liste metriche
    inertia_list = []
    silhouette_list = []
    calinski_list = []
    davies_list = []

    for k in k_range:
        print(f"Evaluating KMeans with k={k}...")
        kmeans = KMeans(n_clusters=k, random_state=42)
        labels = kmeans.fit_predict(x_scaled)

        inertia_list.append(kmeans.inertia_)
        silhouette_list.append(silhouette_score(x_scaled, labels))
        calinski_list.append(calinski_harabasz_score(x_scaled, labels))
        davies_list.append(davies_bouldin_score(x_scaled, labels))

    # Funzione salvataggio grafici
    def plot_metric(values, ylabel, filename):
        plt.figure(figsize=(8, 5))
        plt.plot(k_range, values, marker='o')
        plt.title(f'{ylabel} vs Number of Clusters (k)')
        plt.xlabel('k')
        plt.ylabel(ylabel)
        plt.xticks(k_range)
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(os.path.join(PLOTS_DIR, filename))
        plt.close()

    # Salva tutti i grafici
    plot_metric(inertia_list, "Inertia", "kmeans_inertia.png")
    plot_metric(silhouette_list, "Silhouette Score", "kmeans_silhouette.png")
    plot_metric(calinski_list, "Calinski-Harabasz Index", "kmeans_calinski.png")
    plot_metric(davies_list, "Davies-Bouldin Index", "kmeans_davies.png")

    # Stampa tabella risultati
    df_scores = pd.DataFrame({
        "k": list(k_range),
        "inertia": inertia_list,
        "silhouette": silhouette_list,
        "calinski_harabasz": calinski_list,
        "davies_bouldin": davies_list
    })

    print("\n=== Valutazione KMeans ===")
    print(df_scores.round(4))
    best_k = df_scores.loc[df_scores["silhouette"].idxmax(), "k"]
    print(f"\n→ Miglior k (silhouette score): {best_k}")

    # Salva CSV
    df_scores.to_csv("clustering/outputs/kmeans_scores.csv", index=False)

if __name__ == "__main__":
    evaluate_kmeans_range()
