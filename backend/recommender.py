import os
import joblib
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from preprocess import clean_text, create_combined_features

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")
VECTORIZER_PATH = os.path.join(os.path.dirname(__file__), "vectorizer.pkl")

class TFIDFRecommender:
    def __init__(self):
        self.vectorizer = None
        self.tfidf_matrix = None
        self.is_trained = False

    def train(self, df: pd.DataFrame):
        """Train TF-IDF Vectorizer on combined text features and save model/vectorizer."""
        print("Preprocessing combined feature text for TF-IDF training...")
        combined_text = create_combined_features(df)

        print("Fitting TF-IDF Vectorizer...")
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            min_df=2,
            max_df=0.85,
            stop_words='english'
        )
        self.tfidf_matrix = self.vectorizer.fit_transform(combined_text)
        self.is_trained = True

        # Save artifacts to disk
        try:
            joblib.dump(self.vectorizer, VECTORIZER_PATH)
            joblib.dump(self.tfidf_matrix, MODEL_PATH)
            print(f"Saved vectorizer to {VECTORIZER_PATH} and model to {MODEL_PATH}")
        except Exception as e:
            print(f"Warning: Could not save model pkl files: {e}")

    def load_or_train(self, df: pd.DataFrame):
        """Load precomputed matrix and vectorizer from pkl files if available, otherwise train."""
        if os.path.exists(VECTORIZER_PATH) and os.path.exists(MODEL_PATH):
            try:
                print("Loading cached vectorizer.pkl and model.pkl...")
                self.vectorizer = joblib.load(VECTORIZER_PATH)
                self.tfidf_matrix = joblib.load(MODEL_PATH)
                
                # Check matrix dimensions match DataFrame
                if self.tfidf_matrix.shape[0] == len(df):
                    self.is_trained = True
                    print(f"Loaded TF-IDF model successfully! Matrix shape: {self.tfidf_matrix.shape}")
                    return
                else:
                    print("Matrix shape mismatch with current dataset. Retraining...")
            except Exception as e:
                print(f"Failed to load pkl files ({e}). Retraining model...")
        
        self.train(df)

    def search_query(self, query: str, df: pd.DataFrame, top_n: int = 10, candidate_indices: list[int] = None) -> list[tuple[int, float]]:
        """
        Search recipes using TF-IDF cosine similarity for a user input text query.
        Returns list of tuples: (recipe_index, similarity_score)
        """
        if not self.is_trained or self.vectorizer is None or self.tfidf_matrix is None:
            raise RuntimeError("TF-IDF Recommender model is not trained.")

        cleaned_q = clean_text(query)
        if not cleaned_q:
            return []

        query_vec = self.vectorizer.transform([cleaned_q])
        
        if candidate_indices is not None and len(candidate_indices) > 0:
            sub_matrix = self.tfidf_matrix[candidate_indices]
            scores = cosine_similarity(query_vec, sub_matrix).flatten()
            
            # Map sub_matrix scores back to original dataset indices
            scored_candidates = [(candidate_indices[i], float(scores[i])) for i in range(len(scores))]
            # Sort by similarity score descending
            scored_candidates.sort(key=lambda x: x[1], reverse=True)
            return scored_candidates[:top_n]
        else:
            scores = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
            top_indices = np.argsort(scores)[::-1][:top_n]
            return [(int(idx), float(scores[idx])) for idx in top_indices if scores[idx] > 0.0]

    def recommend_similar(self, recipe_idx: int, df: pd.DataFrame, top_n: int = 6, candidate_indices: list[int] = None) -> list[tuple[int, float]]:
        """
        Recommend recipes similar to a given recipe index using cosine similarity.
        """
        if not self.is_trained or self.tfidf_matrix is None:
            raise RuntimeError("TF-IDF Recommender model is not trained.")

        if recipe_idx < 0 or recipe_idx >= self.tfidf_matrix.shape[0]:
            return []

        recipe_vec = self.tfidf_matrix[recipe_idx]
        scores = cosine_similarity(recipe_vec, self.tfidf_matrix).flatten()

        # Zero out the target recipe itself so it is not recommended to itself
        scores[recipe_idx] = -1.0

        if candidate_indices is not None and len(candidate_indices) > 0:
            candidate_set = set(candidate_indices)
            candidate_scores = [(idx, float(scores[idx])) for idx in candidate_indices if idx != recipe_idx]
            candidate_scores.sort(key=lambda x: x[1], reverse=True)
            return candidate_scores[:top_n]
        else:
            top_indices = np.argsort(scores)[::-1][:top_n]
            return [(int(idx), float(scores[idx])) for idx in top_indices if scores[idx] > -1.0]
