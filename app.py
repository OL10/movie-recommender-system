"""
Streamlit App for Hybrid Movie Recommendation System
"""

import streamlit as st
import pandas as pd
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from recommender import HybridRecommender

# Page configuration
st.set_page_config(
    page_title="Movie Recommender System",
    page_icon="🎬",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
    }
    .movie-card {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f0f2f6;
        margin: 0.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Title
st.title("🎬 Hybrid Movie Recommendation System")
st.markdown("Get personalized movie recommendations using AI-powered hybrid filtering!")

# Sidebar
st.sidebar.header("Configuration")
recommendation_type = st.sidebar.selectbox(
    "Recommendation Type",
    ["Content-Based", "Collaborative", "Hybrid"]
)

n_recommendations = st.sidebar.slider(
    "Number of Recommendations",
    min_value=5,
    max_value=20,
    value=10
)

# Load model and data
@st.cache_resource
def load_model_and_data():
    """Load the trained model and datasets"""
    try:
        # Try to load pre-trained model
        model = HybridRecommender.load_model('models/hybrid_recommender.pkl')
        movies = pd.read_csv('data/movies.csv')
        return model, movies, True
    except:
        # Return None if model not found
        return None, None, False

model, movies_df, model_loaded = load_model_and_data()

if not model_loaded:
    st.warning("⚠️ Model not loaded. Please train the model first using `train.py`")
    st.info("""
    To train the model:
    1. Download TMDB and MovieLens datasets
    2. Place them in the `data/` folder
    3. Run: `python train.py`
    """)
    st.stop()

# Main content
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📝 Input")
    
    if recommendation_type in ["Content-Based", "Hybrid"]:
        movie_title = st.selectbox(
            "Select a Movie",
            options=movies_df['title'].unique() if movies_df is not None else [],
            help="Choose a movie you like to get similar recommendations"
        )
    
    if recommendation_type in ["Collaborative", "Hybrid"]:
        user_id = st.number_input(
            "User ID",
            min_value=1,
            max_value=1000,
            value=1,
            help="Enter your user ID"
        )
    
    # Weights for hybrid
    if recommendation_type == "Hybrid":
        st.markdown("---")
        st.subheader("⚖️ Hybrid Weights")
        content_weight = st.slider(
            "Content-Based Weight",
            min_value=0.0,
            max_value=1.0,
            value=0.5,
            step=0.1
        )
        collab_weight = 1.0 - content_weight
        st.text(f"Collaborative Weight: {collab_weight:.1f}")
        
        model.content_weight = content_weight
        model.collab_weight = collab_weight
    
    get_recommendations = st.button("Get Recommendations 🎯", type="primary")

with col2:
    st.subheader("🎯 Recommendations")
    
    if get_recommendations:
        with st.spinner("Finding the best movies for you..."):
            try:
                # Get recommendations based on type
                if recommendation_type == "Content-Based":
                    recommendations = model.get_content_recommendations(
                        movie_title,
                        n_recommendations=n_recommendations
                    )
                    score_col = 'similarity_score'
                    
                elif recommendation_type == "Collaborative":
                    recommendations = model.get_collaborative_recommendations(
                        user_id,
                        n_recommendations=n_recommendations
                    )
                    score_col = 'predicted_rating'
                    
                else:  # Hybrid
                    recommendations = model.get_hybrid_recommendations(
                        user_id=user_id,
                        movie_title=movie_title,
                        n_recommendations=n_recommendations
                    )
                    score_col = 'hybrid_score'
                
                if recommendations.empty:
                    st.warning("No recommendations found. Try different inputs.")
                else:
                    # Display recommendations
                    for idx, row in recommendations.iterrows():
                        with st.container():
                            st.markdown(f"""
                                <div class="movie-card">
                                    <h3>🎬 {row['title']}</h3>
                                    <p><strong>Genres:</strong> {row['genres']}</p>
                                    <p><strong>Score:</strong> {row[score_col]:.3f}</p>
                                </div>
                            """, unsafe_allow_html=True)
                    
                    # Download recommendations
                    csv = recommendations.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Recommendations",
                        data=csv,
                        file_name="movie_recommendations.csv",
                        mime="text/csv"
                    )
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center'>
        <p>Built with ❤️ using Python, Scikit-learn, and Streamlit</p>
        <p>Data from TMDB and MovieLens | Hybrid Algorithm: TF-IDF + SVD</p>
    </div>
    """, unsafe_allow_html=True)

# Sidebar info
with st.sidebar:
    st.markdown("---")
    st.subheader("ℹ️ About")
    st.info("""
    This hybrid recommender system combines:
    
    **Content-Based Filtering**
    - Uses TF-IDF on movie metadata
    - Finds similar movies based on genres, plot, keywords
    
    **Collaborative Filtering**
    - Uses SVD matrix factorization
    - Learns from user rating patterns
    
    **Hybrid Approach**
    - Combines both methods
    - Balances content similarity and user preferences
    """)
    
    st.markdown("---")
    st.subheader("📊 System Stats")
    if model_loaded and movies_df is not None:
        st.metric("Total Movies", f"{len(movies_df):,}")
        if model.user_movie_matrix is not None:
            st.metric("Total Users", f"{len(model.user_movie_matrix):,}")
            st.metric("Total Ratings", f"{model.ratings_df.shape[0]:,}")
