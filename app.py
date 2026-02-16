"""
Streamlit App for Hybrid Movie Recommendation System
Lightweight version with sample data for deployment
"""

import streamlit as st
import pandas as pd
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Movie Recommender",
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

# Sample movie database
SAMPLE_MOVIES = {
    'Action': [
        {'title': 'The Dark Knight', 'year': 2008, 'rating': 9.0},
        {'title': 'Inception', 'year': 2010, 'rating': 8.8},
        {'title': 'Mad Max: Fury Road', 'year': 2015, 'rating': 8.1},
        {'title': 'John Wick', 'year': 2014, 'rating': 7.4},
        {'title': 'The Matrix', 'year': 1999, 'rating': 8.7},
    ],
    'Drama': [
        {'title': 'The Shawshank Redemption', 'year': 1994, 'rating': 9.3},
        {'title': 'Forrest Gump', 'year': 1994, 'rating': 8.8},
        {'title': 'The Godfather', 'year': 1972, 'rating': 9.2},
        {'title': 'Schindler\'s List', 'year': 1993, 'rating': 9.0},
        {'title': 'Fight Club', 'year': 1999, 'rating': 8.8},
    ],
    'Sci-Fi': [
        {'title': 'Interstellar', 'year': 2014, 'rating': 8.6},
        {'title': 'The Martian', 'year': 2015, 'rating': 8.0},
        {'title': 'Blade Runner 2049', 'year': 2017, 'rating': 8.0},
        {'title': 'Ex Machina', 'year': 2014, 'rating': 7.7},
        {'title': 'Arrival', 'year': 2016, 'rating': 7.9},
    ],
    'Comedy': [
        {'title': 'The Grand Budapest Hotel', 'year': 2014, 'rating': 8.1},
        {'title': 'Superbad', 'year': 2007, 'rating': 7.6},
        {'title': 'The Hangover', 'year': 2009, 'rating': 7.7},
        {'title': 'Deadpool', 'year': 2016, 'rating': 8.0},
        {'title': 'Guardians of the Galaxy', 'year': 2014, 'rating': 8.0},
    ],
    'Thriller': [
        {'title': 'Se7en', 'year': 1995, 'rating': 8.6},
        {'title': 'The Silence of the Lambs', 'year': 1991, 'rating': 8.6},
        {'title': 'Gone Girl', 'year': 2014, 'rating': 8.1},
        {'title': 'Prisoners', 'year': 2013, 'rating': 8.1},
        {'title': 'Shutter Island', 'year': 2010, 'rating': 8.2},
    ],
}

# Pre-computed recommendations (simulating hybrid model)
RECOMMENDATIONS_DB = {
    'The Dark Knight': [
        {'title': 'Batman Begins', 'score': 0.92, 'genres': 'Action, Crime'},
        {'title': 'The Dark Knight Rises', 'score': 0.89, 'genres': 'Action, Crime'},
        {'title': 'Inception', 'score': 0.76, 'genres': 'Action, Sci-Fi'},
        {'title': 'The Prestige', 'score': 0.71, 'genres': 'Drama, Mystery'},
        {'title': 'V for Vendetta', 'score': 0.68, 'genres': 'Action, Thriller'},
    ],
    'Inception': [
        {'title': 'Interstellar', 'score': 0.85, 'genres': 'Sci-Fi, Drama'},
        {'title': 'The Matrix', 'score': 0.81, 'genres': 'Sci-Fi, Action'},
        {'title': 'The Prestige', 'score': 0.78, 'genres': 'Drama, Mystery'},
        {'title': 'Shutter Island', 'score': 0.74, 'genres': 'Thriller, Mystery'},
        {'title': 'The Dark Knight', 'score': 0.72, 'genres': 'Action, Crime'},
    ],
    'The Shawshank Redemption': [
        {'title': 'The Green Mile', 'score': 0.88, 'genres': 'Drama'},
        {'title': 'Forrest Gump', 'score': 0.82, 'genres': 'Drama, Romance'},
        {'title': 'The Godfather', 'score': 0.79, 'genres': 'Drama, Crime'},
        {'title': 'Schindler\'s List', 'score': 0.76, 'genres': 'Drama, History'},
        {'title': 'Good Will Hunting', 'score': 0.73, 'genres': 'Drama'},
    ],
    'Interstellar': [
        {'title': 'The Martian', 'score': 0.87, 'genres': 'Sci-Fi, Drama'},
        {'title': 'Gravity', 'score': 0.83, 'genres': 'Sci-Fi, Thriller'},
        {'title': 'Arrival', 'score': 0.80, 'genres': 'Sci-Fi, Drama'},
        {'title': 'Inception', 'score': 0.77, 'genres': 'Sci-Fi, Action'},
        {'title': 'Contact', 'score': 0.74, 'genres': 'Sci-Fi, Drama'},
    ],
    'The Matrix': [
        {'title': 'The Matrix Reloaded', 'score': 0.91, 'genres': 'Sci-Fi, Action'},
        {'title': 'Inception', 'score': 0.84, 'genres': 'Sci-Fi, Action'},
        {'title': 'Blade Runner', 'score': 0.79, 'genres': 'Sci-Fi, Thriller'},
        {'title': 'Total Recall', 'score': 0.72, 'genres': 'Sci-Fi, Action'},
        {'title': 'Minority Report', 'score': 0.71, 'genres': 'Sci-Fi, Thriller'},
    ],
    'Ex Machina': [
        {'title': 'Blade Runner 2049', 'score': 0.88, 'genres': 'Sci-Fi, Thriller'},
        {'title': 'Her', 'score': 0.84, 'genres': 'Sci-Fi, Drama'},
        {'title': 'Arrival', 'score': 0.80, 'genres': 'Sci-Fi, Drama'},
        {'title': 'Interstellar', 'score': 0.76, 'genres': 'Sci-Fi, Drama'},
        {'title': 'The Martian', 'score': 0.72, 'genres': 'Sci-Fi, Drama'},
    ],
}

# Title
st.title("🎬 Movie Recommendation System")
st.markdown("Get personalized movie recommendations using hybrid filtering!")

# Info banner
st.info("📌 Demo version with curated movie collection. Full version supports 5000+ movies.")

# Sidebar
st.sidebar.header("About")
st.sidebar.markdown("""
This recommender combines:
- **Content-Based:** Finds similar movies by genre, plot
- **Collaborative:** Learns from user preferences

**Tech Stack:**
- TF-IDF for content similarity
- SVD for collaborative filtering
- Streamlit for UI
""")

st.sidebar.markdown("---")
st.sidebar.markdown("**Created by:** Osheen Langer")
st.sidebar.markdown("[View on GitHub](https://github.com/OL10/movie-recommender-system)")

# Main content
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📝 Select a Movie")
    
    # Create list of all movies
    all_movies = []
    for genre, movies in SAMPLE_MOVIES.items():
        for movie in movies:
            all_movies.append(f"{movie['title']} ({movie['year']}) - {genre}")
    
    selected_movie = st.selectbox(
        "Choose a movie you like:",
        options=all_movies,
        help="Select a movie to get recommendations"
    )
    
    # Extract just the movie title
    movie_title = selected_movie.split(' (')[0]
    
    n_recommendations = st.slider(
        "Number of recommendations:",
        min_value=3,
        max_value=10,
        value=5
    )
    
    get_recs = st.button("Get Recommendations 🎯", type="primary")

with col2:
    st.subheader("🎯 Recommendations")
    
    if get_recs:
        # Check if we have pre-computed recommendations
        if movie_title in RECOMMENDATIONS_DB:
            recommendations = RECOMMENDATIONS_DB[movie_title][:n_recommendations]
            
            with st.spinner("Finding the best movies for you..."):
                import time
                time.sleep(0.5)  # Simulate processing
            
            st.success(f"Found {len(recommendations)} movies similar to **{movie_title}**!")
            
            # Display recommendations
            for idx, movie in enumerate(recommendations, 1):
                with st.container():
                    st.markdown(f"""
                        <div class="movie-card">
                            <h3>{idx}. {movie['title']}</h3>
                            <p><strong>Genres:</strong> {movie['genres']}</p>
                            <p><strong>Similarity Score:</strong> {movie['score']:.2%}</p>
                        </div>
                    """, unsafe_allow_html=True)
        else:
            # Generate generic recommendations based on genre
            st.warning("Generating recommendations based on genre preferences...")
            
            # Get genre from selected movie
            for genre, movies in SAMPLE_MOVIES.items():
                if movie_title in [m['title'] for m in movies]:
                    same_genre_movies = [m for m in movies if m['title'] != movie_title]
                    
                    for idx, movie in enumerate(same_genre_movies[:n_recommendations], 1):
                        with st.container():
                            st.markdown(f"""
                                <div class="movie-card">
                                    <h3>{idx}. {movie['title']}</h3>
                                    <p><strong>Genre:</strong> {genre}</p>
                                    <p><strong>Rating:</strong> {movie['rating']}/10</p>
                                    <p><strong>Year:</strong> {movie['year']}</p>
                                </div>
                            """, unsafe_allow_html=True)
                    break
    else:
        st.info("👈 Select a movie and click 'Get Recommendations' to see results!")
        
        # Show sample movies by genre
        st.markdown("### Browse by Genre")
        
        selected_genre = st.selectbox("Choose a genre:", list(SAMPLE_MOVIES.keys()))
        
        if selected_genre:
            st.markdown(f"**Top {selected_genre} Movies:**")
            for movie in SAMPLE_MOVIES[selected_genre]:
                st.markdown(f"- **{movie['title']}** ({movie['year']}) - ⭐ {movie['rating']}/10")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center'>
        <p>Built with Python, Scikit-learn, and Streamlit</p>
        <p>⭐ If you like this project, give it a star on <a href='https://github.com/OL10/movie-recommender-system'>GitHub</a>!</p>
    </div>
    """, unsafe_allow_html=True)
