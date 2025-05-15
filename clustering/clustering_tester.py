"""
Modulo per l'esecuzione e la valutazione di diversi algoritmi di clustering
(KMeans, DBSCAN, Gaussian Mixture Model, Agglomerative Clustering)
applicati a un sottoinsieme del dataset musicale Spotify.

Compie:
- Caricamento e preprocessamento del dataset normalizzato
- Campionamento di 30.000 tracce
- Applicazione di 4 algoritmi di clustering
- Calcolo delle metriche di valutazione (Silhouette, Calinski-Harabasz, Davies-Bouldin)
- Salvataggio dei risultati e dei grafici 2D (PCA) in output

Le metriche sono salvate in formato CSV e i plot sono esportati come immagini PNG.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.mixture import GaussianMixture
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
from sklearn.decomposition import PCA
from preprocessing import preprocess_dataset

# Cartelle di output
PLOTS_DIR = "clustering/outputs/plots"
SCORES_PATH = "clustering/outputs/scores.csv"
os.makedirs(PLOTS_DIR, exist_ok=True)

# Salva le metriche in un dizionario
metrics_list = []

def evaluate_clustering(model_name, labels, features):
    """
    Calcola e salva le metriche di valutazione per il clustering.
    """
    silhouette = silhouette_score(features, labels)
    calinski = calinski_harabasz_score(features, labels)
    davies = davies_bouldin_score(features, labels)

    metrics_list.append({
        "model": model_name,
        "silhouette": silhouette,
        "calinski_harabasz": calinski,
        "davies_bouldin": davies
    })

def plot_clusters(features, labels, model_name):
    """
    Riduce a 2D con PCA e salva il grafico in file.
    """
    pca = PCA(n_components=2)
    components = pca.fit_transform(features)
    df_plot = pd.DataFrame({
        'PCA1': components[:, 0],
        'PCA2': components[:, 1],
        'Cluster': labels
    })
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=df_plot, x='PCA1', y='PCA2', hue='Cluster', palette='Set2', s=50)
    plt.title(f'{model_name} Clustering')
    plt.legend(title='Cluster')
    plt.tight_layout()
    filepath = os.path.join(PLOTS_DIR, f"{model_name.lower().replace(' ', '_')}.png")
    plt.savefig(filepath)
    plt.close()

def run_clustering():
    """
    Esegue una pipeline completa di clustering su un campione del dataset musicale.

    Il dataset viene preprocessato, campionato e sottoposto a quattro algoritmi di clustering:
    - KMeans
    - DBSCAN
    - Gaussian Mixture Model (GMM)
    - Agglomerative Clustering

    Per ciascun modello:
    - calcola e registra le metriche di qualità del clustering 
    (silhouette, Calinski-Harabasz, Davies-Bouldin)
    - salva un grafico 2D dei cluster ottenuti (via PCA) in formato PNG

    Al termine, tutte le metriche vengono salvate in un file CSV.

    Returns:
        None
    """

    # Carica il dataset normalizzato e deduplicato
    df_scaled = preprocess_dataset()

    # Campionamento di 10.000 tracce
    df_sampled = df_scaled.sample(n=30000, random_state=42).reset_index(drop=True)

    # Feature da clusterizzare
    features = df_sampled.drop(columns=['track_name'])

    # KMeans
    print("Running KMeans...")
    kmeans = KMeans(n_clusters=5, random_state=42)
    kmeans_labels = kmeans.fit_predict(features)
    evaluate_clustering("KMeans", kmeans_labels, features)
    plot_clusters(features, kmeans_labels, "KMeans")

    # DBSCAN
    print("Running DBSCAN...")
    dbscan = DBSCAN(eps=0.5, min_samples=5)
    dbscan_labels = dbscan.fit_predict(features)
    evaluate_clustering("DBSCAN", dbscan_labels, features)
    plot_clusters(features, dbscan_labels, "DBSCAN")

    # GMM
    print("Running Gaussian Mixture...")
    gmm = GaussianMixture(n_components=5, random_state=42)
    gmm_labels = gmm.fit_predict(features)
    evaluate_clustering("GMM", gmm_labels, features)
    plot_clusters(features, gmm_labels, "GMM")

    # Agglomerative
    print("Running Agglomerative...")
    agglomerative = AgglomerativeClustering(n_clusters=5)
    agglomerative_labels = agglomerative.fit_predict(features)
    evaluate_clustering("Agglomerative", agglomerative_labels, features)
    plot_clusters(features, agglomerative_labels, "Agglomerative")

    # Salvataggio delle metriche in CSV
    df_metrics = pd.DataFrame(metrics_list)
    df_metrics.to_csv(SCORES_PATH, index=False)
    print(f"\nTutte le metriche salvate in: {SCORES_PATH}")
    print(f"Tutti i grafici salvati in: {PLOTS_DIR}")

if __name__ == "__main__":
    run_clustering()
