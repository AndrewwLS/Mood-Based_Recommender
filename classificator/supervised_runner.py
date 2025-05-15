"""
Modulo che contiene il test di:

- RandomForest 
- Decision Tree 
- NaiveBayes 
- K-Nearest Neighbors
- AdaBoost

Salva infine il file mood_classifier.pkl supervisionato
scegliendo il RandomForest
"""
import pickle
import warnings
import numpy as np
import pandas as pd
from sklearn.exceptions import UndefinedMetricWarning

from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
from sklearn.preprocessing import LabelEncoder

from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import AdaBoostClassifier

# Flag per il numero di tracce da utilizzare per i test
N = 50000

# Eliminazione warning
warnings.filterwarnings("ignore", category=UndefinedMetricWarning)

# Caricamento dati
df = pd.read_csv("dataset/data/clean_tracks.csv")
df = df.sample(N, random_state=42)

# Features e target
features = [
    "valence", "energy", "danceability", "tempo", "acousticness",
    "instrumentalness", "speechiness", "artists", "duration_ms", "track_genre"
]

# Codifica delle colonne categoriche
df["artists"] = LabelEncoder().fit_transform(df["artists"].astype(str))
df["track_genre"] = LabelEncoder().fit_transform(df["track_genre"].astype(str))

X = df[features]
y = df["mood"]

# Codifica target
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# Funzione di valutazione
def evaluate_model(name, model):
    """
    Valuta un modello di classificazione supervisionata usando 
    cross-validation stratificata a 5 fold.

    Per ogni fold, il modello viene addestrato e testato, e vengono calcolate le metriche:
    accuratezza, precisione, recall e F1-score (macro-averaged).

    Args:
        name (str): Nome descrittivo del modello (usato nella stampa a video).
        model (sklearn.base.BaseEstimator): Istanza del modello da addestrare e valutare.

    Returns:
        None: I risultati vengono stampati a video 
        (media e deviazione standard per ciascuna metrica).
    """
    kf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    acc_scores, prec_scores, rec_scores, f1_scores = [], [], [], []

    for train_idx, test_idx in kf.split(X, y_encoded):
        x_train, x_test = X.iloc[train_idx], X.iloc[test_idx]
        y_train, y_test = y_encoded[train_idx], y_encoded[test_idx]

        model.fit(x_train, y_train)
        y_pred = model.predict(x_test)

        acc_scores.append(accuracy_score(y_test, y_pred))
        prec_scores.append(precision_score(y_test, y_pred, average='macro', zero_division=0))
        rec_scores.append(recall_score(y_test, y_pred, average='macro', zero_division=0))
        f1_scores.append(f1_score(y_test, y_pred, average='macro', zero_division=0))

    print(f"=== {name} ===")
    print(f"Accuracy : {np.mean(acc_scores):.3f} ± {np.std(acc_scores):.3f}")
    print(f"Precision: {np.mean(prec_scores):.3f} ± {np.std(prec_scores):.3f}")
    print(f"Recall   : {np.mean(rec_scores):.3f} ± {np.std(rec_scores):.3f}")
    print(f"F1-score : {np.mean(f1_scores):.3f} ± {np.std(f1_scores):.3f}")
    print()

# Valutazione dei modelli
evaluate_model("Random Forest", RandomForestClassifier())
evaluate_model("Decision Tree", DecisionTreeClassifier())
evaluate_model("Naive Bayes", GaussianNB())
evaluate_model("K-Nearest Neighbors", KNeighborsClassifier())
evaluate_model("AdaBoost", AdaBoostClassifier())

# Addestramento e salvataggio del RandomForest
model_final = RandomForestClassifier()
model_final.fit(X, y_encoded)

with open("classificator/mood_classifier.pkl", "wb") as f:
    pickle.dump((model_final, le), f)
