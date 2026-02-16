"""
Hybrid Movie Recommendation Engine
Combines Content-Based Filtering (TF-IDF) and Collaborative Filtering (SVD)
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse.linalg import svds
import pickle
import warnings
warnings.filterwarnings('ignore')


class HybridRecommender:
    """
    Hybrid recommendation system combining:
    1. Content-based filtering using TF-IDF on movie metadata
    2. Collaborative filtering using SVD on user ratings
    """
    
    def __init__(self, content_weight=0.5, collab_weight=0.5):
        """
        Initialize the hybrid recommender
        
        Args:
            content_weight (float): Weight for content-based recommendations
            collab_weight (float): Weight for collaborative filtering recommendations
        """
        self.content_weight = content_weight
        self.collab_weight = collab_weight
        self.tfidf_matrix = None
        self.tfidf_vectorizer = None
        self.movies_df = None
        self.ratings_df = None
        self.user_movie_matrix = None
        self.svd_predictions = None
        
    def fit_content_based(self, movies_df, features=['genres', 'overview', 'keywords']):
        """
        Fit content-based model using TF-IDF
        
        Args:
            movies_df (DataFrame): Movie metadata with features
            features (list): Column names to use for content features
        """
        self.movies_df = movies_df.copy()
        
        # Combine features into single text column
        self.movies_df['combined_features'] = ''
        for feature in features:
            if feature in self.movies_df.columns:
                self.movies_df['combined_features'] += self.movies_df[feature].fillna('') + ' '
        
        # Create TF-IDF matrix
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(
            self.movies_df['combined_features']
        )
        
        print(f"Content-based model fitted with {self.tfidf_matrix.shape[0]} movies")
        
    def fit_collaborative(self, ratings_df, n_factors=50):
        """
        Fit collaborative filtering model using SVD
        
        Args:
            ratings_df (DataFrame): User ratings with columns [userId, movieId, rating]
            n_factors (int): Number of latent factors for SVD
        """
        self.ratings_df = ratings_df.copy()
        
        # Create user-movie matrix
        self.user_movie_matrix = self.ratings_df.pivot_table(
            index='userId',
            columns='movieId',
            values='rating'
        ).fillna(0)
        
        # Normalize by subtracting row mean
        user_ratings_mean = np.mean(self.user_movie_matrix.values, axis=1)
        ratings_normalized = self.user_movie_matrix.values - user_ratings_mean.reshape(-1, 1)
        
        # Perform SVD
        U, sigma, Vt = svds(ratings_normalized, k=n_factors)
        sigma = np.diag(sigma)
        
        # Generate predictions
        self.svd_predictions = np.dot(np.dot(U, sigma), Vt) + user_ratings_mean.reshape(-1, 1)
        self.svd_predictions = pd.DataFrame(
            self.svd_predictions,
            columns=self.user_movie_matrix.columns,
            index=self.user_movie_matrix.index
        )
        
        print(f"Collaborative model fitted with {len(self.user_movie_matrix)} users")
        
    def get_content_recommendations(self, movie_title, n_recommendations=10):
        """
        Get content-based recommendations for a given movie
        
        Args:
            movie_title (str): Title of the movie
            n_recommendations (int): Number of recommendations to return
            
        Returns:
            DataFrame: Recommended movies with similarity scores
        """
        if self.tfidf_matrix is None:
            raise ValueError("Content-based model not fitted. Call fit_content_based first.")
        
        # Find movie index
        idx = self.movies_df[self.movies_df['title'].str.lower() == movie_title.lower()].index
        
        if len(idx) == 0:
            return pd.DataFrame()
        
        idx = idx[0]
        
        # Calculate similarity scores
        cosine_sim = cosine_similarity(self.tfidf_matrix[idx], self.tfidf_matrix).flatten()
        
        # Get top recommendations (excluding the input movie)
        similar_indices = cosine_sim.argsort()[::-1][1:n_recommendations+1]
        
        recommendations = self.movies_df.iloc[similar_indices].copy()
        recommendations['similarity_score'] = cosine_sim[similar_indices]
        
        return recommendations[['title', 'genres', 'similarity_score']]
    
    def get_collaborative_recommendations(self, user_id, n_recommendations=10):
        """
        Get collaborative filtering recommendations for a user
        
        Args:
            user_id (int): User ID
            n_recommendations (int): Number of recommendations to return
            
        Returns:
            DataFrame: Recommended movies with predicted ratings
        """
        if self.svd_predictions is None:
            raise ValueError("Collaborative model not fitted. Call fit_collaborative first.")
        
        if user_id not in self.svd_predictions.index:
            return pd.DataFrame()
        
        # Get user's predictions
        user_predictions = self.svd_predictions.loc[user_id]
        
        # Get movies user hasn't rated
        rated_movies = self.user_movie_matrix.loc[user_id]
        rated_movies = rated_movies[rated_movies > 0].index
        
        # Filter out already rated movies
        user_predictions = user_predictions[~user_predictions.index.isin(rated_movies)]
        
        # Get top recommendations
        top_recommendations = user_predictions.nlargest(n_recommendations)
        
        # Merge with movie details
        recommendations = pd.DataFrame({
            'movieId': top_recommendations.index,
            'predicted_rating': top_recommendations.values
        })
        
        recommendations = recommendations.merge(
            self.movies_df,
            left_on='movieId',
            right_on='movieId',
            how='left'
        )
        
        return recommendations[['title', 'genres', 'predicted_rating']]
    
    def get_hybrid_recommendations(self, user_id=None, movie_title=None, n_recommendations=10):
        """
        Get hybrid recommendations combining content-based and collaborative filtering
        
        Args:
            user_id (int): User ID for collaborative filtering
            movie_title (str): Movie title for content-based filtering
            n_recommendations (int): Number of recommendations to return
            
        Returns:
            DataFrame: Hybrid recommendations with combined scores
        """
        content_recs = pd.DataFrame()
        collab_recs = pd.DataFrame()
        
        # Get content-based recommendations
        if movie_title:
            content_recs = self.get_content_recommendations(movie_title, n_recommendations * 2)
        
        # Get collaborative recommendations
        if user_id:
            collab_recs = self.get_collaborative_recommendations(user_id, n_recommendations * 2)
        
        # Combine recommendations
        if not content_recs.empty and not collab_recs.empty:
            # Normalize scores
            content_recs['content_score'] = (
                content_recs['similarity_score'] - content_recs['similarity_score'].min()
            ) / (content_recs['similarity_score'].max() - content_recs['similarity_score'].min())
            
            collab_recs['collab_score'] = (
                collab_recs['predicted_rating'] - collab_recs['predicted_rating'].min()
            ) / (collab_recs['predicted_rating'].max() - collab_recs['predicted_rating'].min())
            
            # Merge on movie title
            hybrid = pd.merge(
                content_recs[['title', 'genres', 'content_score']],
                collab_recs[['title', 'collab_score']],
                on='title',
                how='outer'
            ).fillna(0)
            
            # Calculate hybrid score
            hybrid['hybrid_score'] = (
                self.content_weight * hybrid['content_score'] +
                self.collab_weight * hybrid['collab_score']
            )
            
            # Sort and return top recommendations
            hybrid = hybrid.sort_values('hybrid_score', ascending=False).head(n_recommendations)
            return hybrid[['title', 'genres', 'hybrid_score']]
        
        elif not content_recs.empty:
            return content_recs.head(n_recommendations)
        
        elif not collab_recs.empty:
            return collab_recs.head(n_recommendations)
        
        else:
            return pd.DataFrame()
    
    def save_model(self, filepath):
        """Save the trained model"""
        with open(filepath, 'wb') as f:
            pickle.dump(self, f)
    
    @staticmethod
    def load_model(filepath):
        """Load a trained model"""
        with open(filepath, 'rb') as f:
            return pickle.load(f)


def evaluate_recommendations(recommender, test_ratings, k=10):
    """
    Evaluate recommendation quality using precision@k and recall@k
    
    Args:
        recommender: Trained HybridRecommender instance
        test_ratings: Test set ratings DataFrame
        k: Number of top recommendations to consider
        
    Returns:
        dict: Evaluation metrics
    """
    precisions = []
    recalls = []
    
    for user_id in test_ratings['userId'].unique()[:100]:  # Sample 100 users
        # Get actual relevant items (rated >= 4.0)
        relevant_items = set(
            test_ratings[(test_ratings['userId'] == user_id) & 
                        (test_ratings['rating'] >= 4.0)]['movieId']
        )
        
        if len(relevant_items) == 0:
            continue
        
        # Get recommendations
        recs = recommender.get_collaborative_recommendations(user_id, n_recommendations=k)
        
        if recs.empty:
            continue
        
        recommended_items = set(recs['movieId'] if 'movieId' in recs.columns else [])
        
        # Calculate precision and recall
        hits = len(relevant_items.intersection(recommended_items))
        precision = hits / k if k > 0 else 0
        recall = hits / len(relevant_items) if len(relevant_items) > 0 else 0
        
        precisions.append(precision)
        recalls.append(recall)
    
    return {
        'precision@k': np.mean(precisions) if precisions else 0,
        'recall@k': np.mean(recalls) if recalls else 0,
        'f1@k': 2 * np.mean(precisions) * np.mean(recalls) / (np.mean(precisions) + np.mean(recalls))
                if (np.mean(precisions) + np.mean(recalls)) > 0 else 0
    }
