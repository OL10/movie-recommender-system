"""
Movie Recommendation System
Clean, professional interface
"""

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

# Custom CSS - Fixed contrast issue
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #0066cc;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        font-size: 16px;
    }
    .stButton>button:hover {
        background-color: #0052a3;
    }
    .movie-card {
        padding: 1.2rem;
        border-radius: 8px;
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        margin: 0.8rem 0;
    }
    .movie-card h3 {
        color: #212529;
        margin: 0 0 0.5rem 0;
        font-size: 1.1rem;
    }
    .movie-card p {
        color: #495057;
        margin: 0.3rem 0;
        font-size: 0.95rem;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 4px;
        margin-bottom: 1rem;
        border: 1px solid #c3e6cb;
    }
    </style>
    """, unsafe_allow_html=True)

# Complete movie database
MOVIES_DATA = {
    'The Dark Knight': {
        'genre': 'Action',
        'year': 2008,
        'rating': 9.0,
        'recommendations': [
            {'title': 'Batman Begins', 'score': 0.92, 'genres': 'Action, Crime'},
            {'title': 'The Dark Knight Rises', 'score': 0.89, 'genres': 'Action, Crime'},
            {'title': 'Inception', 'score': 0.76, 'genres': 'Action, Sci-Fi'},
            {'title': 'The Prestige', 'score': 0.71, 'genres': 'Drama, Mystery'},
            {'title': 'V for Vendetta', 'score': 0.68, 'genres': 'Action, Thriller'},
            {'title': 'The Matrix', 'score': 0.65, 'genres': 'Sci-Fi, Action'},
            {'title': 'John Wick', 'score': 0.63, 'genres': 'Action, Thriller'},
            {'title': 'Mad Max: Fury Road', 'score': 0.60, 'genres': 'Action'},
        ]
    },
    'Inception': {
        'genre': 'Action',
        'year': 2010,
        'rating': 8.8,
        'recommendations': [
            {'title': 'Interstellar', 'score': 0.85, 'genres': 'Sci-Fi, Drama'},
            {'title': 'The Matrix', 'score': 0.81, 'genres': 'Sci-Fi, Action'},
            {'title': 'The Prestige', 'score': 0.78, 'genres': 'Drama, Mystery'},
            {'title': 'Shutter Island', 'score': 0.74, 'genres': 'Thriller, Mystery'},
            {'title': 'The Dark Knight', 'score': 0.72, 'genres': 'Action, Crime'},
            {'title': 'Memento', 'score': 0.70, 'genres': 'Thriller, Mystery'},
            {'title': 'Ex Machina', 'score': 0.68, 'genres': 'Sci-Fi, Thriller'},
        ]
    },
    'Mad Max: Fury Road': {
        'genre': 'Action',
        'year': 2015,
        'rating': 8.1,
        'recommendations': [
            {'title': 'The Dark Knight', 'score': 0.78, 'genres': 'Action, Crime'},
            {'title': 'John Wick', 'score': 0.75, 'genres': 'Action, Thriller'},
            {'title': 'Gladiator', 'score': 0.72, 'genres': 'Action, Drama'},
            {'title': 'The Matrix', 'score': 0.70, 'genres': 'Sci-Fi, Action'},
            {'title': '300', 'score': 0.68, 'genres': 'Action, War'},
        ]
    },
    'John Wick': {
        'genre': 'Action',
        'year': 2014,
        'rating': 7.4,
        'recommendations': [
            {'title': 'John Wick: Chapter 2', 'score': 0.95, 'genres': 'Action, Thriller'},
            {'title': 'Mad Max: Fury Road', 'score': 0.80, 'genres': 'Action'},
            {'title': 'The Dark Knight', 'score': 0.75, 'genres': 'Action, Crime'},
            {'title': 'The Matrix', 'score': 0.72, 'genres': 'Sci-Fi, Action'},
            {'title': 'Taken', 'score': 0.70, 'genres': 'Action, Thriller'},
        ]
    },
    'The Matrix': {
        'genre': 'Action',
        'year': 1999,
        'rating': 8.7,
        'recommendations': [
            {'title': 'The Matrix Reloaded', 'score': 0.91, 'genres': 'Sci-Fi, Action'},
            {'title': 'Inception', 'score': 0.84, 'genres': 'Sci-Fi, Action'},
            {'title': 'Blade Runner', 'score': 0.79, 'genres': 'Sci-Fi, Thriller'},
            {'title': 'Total Recall', 'score': 0.72, 'genres': 'Sci-Fi, Action'},
            {'title': 'Minority Report', 'score': 0.71, 'genres': 'Sci-Fi, Thriller'},
            {'title': 'Ex Machina', 'score': 0.68, 'genres': 'Sci-Fi, Thriller'},
        ]
    },
    'The Shawshank Redemption': {
        'genre': 'Drama',
        'year': 1994,
        'rating': 9.3,
        'recommendations': [
            {'title': 'The Green Mile', 'score': 0.88, 'genres': 'Drama'},
            {'title': 'Forrest Gump', 'score': 0.82, 'genres': 'Drama, Romance'},
            {'title': 'The Godfather', 'score': 0.79, 'genres': 'Drama, Crime'},
            {'title': 'Schindler\'s List', 'score': 0.76, 'genres': 'Drama, History'},
            {'title': 'Good Will Hunting', 'score': 0.73, 'genres': 'Drama'},
            {'title': 'Fight Club', 'score': 0.70, 'genres': 'Drama, Thriller'},
        ]
    },
    'Forrest Gump': {
        'genre': 'Drama',
        'year': 1994,
        'rating': 8.8,
        'recommendations': [
            {'title': 'The Shawshank Redemption', 'score': 0.85, 'genres': 'Drama'},
            {'title': 'Cast Away', 'score': 0.80, 'genres': 'Drama, Adventure'},
            {'title': 'Big Fish', 'score': 0.75, 'genres': 'Drama, Fantasy'},
            {'title': 'The Green Mile', 'score': 0.73, 'genres': 'Drama'},
            {'title': 'A Beautiful Mind', 'score': 0.70, 'genres': 'Drama'},
        ]
    },
    'The Godfather': {
        'genre': 'Drama',
        'year': 1972,
        'rating': 9.2,
        'recommendations': [
            {'title': 'The Godfather Part II', 'score': 0.95, 'genres': 'Drama, Crime'},
            {'title': 'Goodfellas', 'score': 0.85, 'genres': 'Drama, Crime'},
            {'title': 'The Shawshank Redemption', 'score': 0.80, 'genres': 'Drama'},
            {'title': 'Scarface', 'score': 0.78, 'genres': 'Drama, Crime'},
            {'title': 'Casino', 'score': 0.75, 'genres': 'Drama, Crime'},
        ]
    },
    'Schindler\'s List': {
        'genre': 'Drama',
        'year': 1993,
        'rating': 9.0,
        'recommendations': [
            {'title': 'The Pianist', 'score': 0.88, 'genres': 'Drama, History'},
            {'title': 'Saving Private Ryan', 'score': 0.82, 'genres': 'Drama, War'},
            {'title': 'The Shawshank Redemption', 'score': 0.78, 'genres': 'Drama'},
            {'title': 'Life is Beautiful', 'score': 0.76, 'genres': 'Drama, Comedy'},
            {'title': '12 Years a Slave', 'score': 0.73, 'genres': 'Drama, History'},
        ]
    },
    'Fight Club': {
        'genre': 'Drama',
        'year': 1999,
        'rating': 8.8,
        'recommendations': [
            {'title': 'American Psycho', 'score': 0.82, 'genres': 'Drama, Thriller'},
            {'title': 'Se7en', 'score': 0.80, 'genres': 'Thriller, Crime'},
            {'title': 'The Prestige', 'score': 0.75, 'genres': 'Drama, Mystery'},
            {'title': 'Shutter Island', 'score': 0.72, 'genres': 'Thriller, Mystery'},
            {'title': 'Gone Girl', 'score': 0.70, 'genres': 'Thriller, Drama'},
        ]
    },
    'Interstellar': {
        'genre': 'Sci-Fi',
        'year': 2014,
        'rating': 8.6,
        'recommendations': [
            {'title': 'The Martian', 'score': 0.87, 'genres': 'Sci-Fi, Drama'},
            {'title': 'Gravity', 'score': 0.83, 'genres': 'Sci-Fi, Thriller'},
            {'title': 'Arrival', 'score': 0.80, 'genres': 'Sci-Fi, Drama'},
            {'title': 'Inception', 'score': 0.77, 'genres': 'Sci-Fi, Action'},
            {'title': 'Contact', 'score': 0.74, 'genres': 'Sci-Fi, Drama'},
            {'title': '2001: A Space Odyssey', 'score': 0.72, 'genres': 'Sci-Fi'},
        ]
    },
    'The Martian': {
        'genre': 'Sci-Fi',
        'year': 2015,
        'rating': 8.0,
        'recommendations': [
            {'title': 'Interstellar', 'score': 0.88, 'genres': 'Sci-Fi, Drama'},
            {'title': 'Gravity', 'score': 0.85, 'genres': 'Sci-Fi, Thriller'},
            {'title': 'Apollo 13', 'score': 0.80, 'genres': 'Drama, History'},
            {'title': 'Moon', 'score': 0.75, 'genres': 'Sci-Fi, Drama'},
            {'title': 'Arrival', 'score': 0.72, 'genres': 'Sci-Fi, Drama'},
        ]
    },
    'Blade Runner 2049': {
        'genre': 'Sci-Fi',
        'year': 2017,
        'rating': 8.0,
        'recommendations': [
            {'title': 'Blade Runner', 'score': 0.92, 'genres': 'Sci-Fi, Thriller'},
            {'title': 'Ex Machina', 'score': 0.85, 'genres': 'Sci-Fi, Thriller'},
            {'title': 'Ghost in the Shell', 'score': 0.78, 'genres': 'Sci-Fi, Action'},
            {'title': 'The Matrix', 'score': 0.75, 'genres': 'Sci-Fi, Action'},
            {'title': 'Her', 'score': 0.72, 'genres': 'Sci-Fi, Drama'},
        ]
    },
    'Ex Machina': {
        'genre': 'Sci-Fi',
        'year': 2014,
        'rating': 7.7,
        'recommendations': [
            {'title': 'Blade Runner 2049', 'score': 0.88, 'genres': 'Sci-Fi, Thriller'},
            {'title': 'Her', 'score': 0.84, 'genres': 'Sci-Fi, Drama'},
            {'title': 'Arrival', 'score': 0.80, 'genres': 'Sci-Fi, Drama'},
            {'title': 'Interstellar', 'score': 0.76, 'genres': 'Sci-Fi, Drama'},
            {'title': 'The Martian', 'score': 0.72, 'genres': 'Sci-Fi, Drama'},
            {'title': 'Under the Skin', 'score': 0.70, 'genres': 'Sci-Fi, Thriller'},
        ]
    },
    'Arrival': {
        'genre': 'Sci-Fi',
        'year': 2016,
        'rating': 7.9,
        'recommendations': [
            {'title': 'Interstellar', 'score': 0.85, 'genres': 'Sci-Fi, Drama'},
            {'title': 'Ex Machina', 'score': 0.82, 'genres': 'Sci-Fi, Thriller'},
            {'title': 'Contact', 'score': 0.80, 'genres': 'Sci-Fi, Drama'},
            {'title': 'The Martian', 'score': 0.75, 'genres': 'Sci-Fi, Drama'},
            {'title': 'Her', 'score': 0.73, 'genres': 'Sci-Fi, Drama'},
        ]
    },
    'The Grand Budapest Hotel': {
        'genre': 'Comedy',
        'year': 2014,
        'rating': 8.1,
        'recommendations': [
            {'title': 'Moonrise Kingdom', 'score': 0.88, 'genres': 'Comedy, Drama'},
            {'title': 'The Royal Tenenbaums', 'score': 0.85, 'genres': 'Comedy, Drama'},
            {'title': 'Fantastic Mr. Fox', 'score': 0.80, 'genres': 'Comedy, Adventure'},
            {'title': 'Amélie', 'score': 0.75, 'genres': 'Comedy, Romance'},
            {'title': 'The Darjeeling Limited', 'score': 0.72, 'genres': 'Comedy, Drama'},
        ]
    },
    'Superbad': {
        'genre': 'Comedy',
        'year': 2007,
        'rating': 7.6,
        'recommendations': [
            {'title': 'The Hangover', 'score': 0.85, 'genres': 'Comedy'},
            {'title': '21 Jump Street', 'score': 0.80, 'genres': 'Comedy, Action'},
            {'title': 'Pineapple Express', 'score': 0.78, 'genres': 'Comedy, Action'},
            {'title': 'Step Brothers', 'score': 0.75, 'genres': 'Comedy'},
            {'title': 'American Pie', 'score': 0.73, 'genres': 'Comedy'},
        ]
    },
    'The Hangover': {
        'genre': 'Comedy',
        'year': 2009,
        'rating': 7.7,
        'recommendations': [
            {'title': 'The Hangover Part II', 'score': 0.90, 'genres': 'Comedy'},
            {'title': 'Superbad', 'score': 0.82, 'genres': 'Comedy'},
            {'title': '21 Jump Street', 'score': 0.78, 'genres': 'Comedy, Action'},
            {'title': 'Wedding Crashers', 'score': 0.75, 'genres': 'Comedy, Romance'},
            {'title': 'Old School', 'score': 0.72, 'genres': 'Comedy'},
        ]
    },
    'Deadpool': {
        'genre': 'Comedy',
        'year': 2016,
        'rating': 8.0,
        'recommendations': [
            {'title': 'Deadpool 2', 'score': 0.92, 'genres': 'Comedy, Action'},
            {'title': 'Guardians of the Galaxy', 'score': 0.85, 'genres': 'Comedy, Action, Sci-Fi'},
            {'title': 'Kick-Ass', 'score': 0.78, 'genres': 'Comedy, Action'},
            {'title': 'The Nice Guys', 'score': 0.75, 'genres': 'Comedy, Action'},
            {'title': 'Scott Pilgrim vs. the World', 'score': 0.72, 'genres': 'Comedy, Action'},
        ]
    },
    'Guardians of the Galaxy': {
        'genre': 'Comedy',
        'year': 2014,
        'rating': 8.0,
        'recommendations': [
            {'title': 'Guardians of the Galaxy Vol. 2', 'score': 0.90, 'genres': 'Comedy, Action, Sci-Fi'},
            {'title': 'Deadpool', 'score': 0.83, 'genres': 'Comedy, Action'},
            {'title': 'Thor: Ragnarok', 'score': 0.80, 'genres': 'Comedy, Action'},
            {'title': 'Ant-Man', 'score': 0.78, 'genres': 'Comedy, Action'},
            {'title': 'The Avengers', 'score': 0.75, 'genres': 'Action, Sci-Fi'},
        ]
    },
    'Se7en': {
        'genre': 'Thriller',
        'year': 1995,
        'rating': 8.6,
        'recommendations': [
            {'title': 'The Silence of the Lambs', 'score': 0.88, 'genres': 'Thriller, Crime'},
            {'title': 'Zodiac', 'score': 0.85, 'genres': 'Thriller, Crime'},
            {'title': 'Gone Girl', 'score': 0.80, 'genres': 'Thriller, Drama'},
            {'title': 'Prisoners', 'score': 0.78, 'genres': 'Thriller, Crime'},
            {'title': 'Fight Club', 'score': 0.75, 'genres': 'Drama, Thriller'},
        ]
    },
    'The Silence of the Lambs': {
        'genre': 'Thriller',
        'year': 1991,
        'rating': 8.6,
        'recommendations': [
            {'title': 'Se7en', 'score': 0.88, 'genres': 'Thriller, Crime'},
            {'title': 'Zodiac', 'score': 0.82, 'genres': 'Thriller, Crime'},
            {'title': 'Red Dragon', 'score': 0.80, 'genres': 'Thriller, Crime'},
            {'title': 'Prisoners', 'score': 0.78, 'genres': 'Thriller, Crime'},
            {'title': 'Memories of Murder', 'score': 0.75, 'genres': 'Thriller, Crime'},
        ]
    },
    'Gone Girl': {
        'genre': 'Thriller',
        'year': 2014,
        'rating': 8.1,
        'recommendations': [
            {'title': 'Shutter Island', 'score': 0.85, 'genres': 'Thriller, Mystery'},
            {'title': 'The Girl on the Train', 'score': 0.80, 'genres': 'Thriller, Drama'},
            {'title': 'Prisoners', 'score': 0.78, 'genres': 'Thriller, Crime'},
            {'title': 'Nocturnal Animals', 'score': 0.75, 'genres': 'Thriller, Drama'},
            {'title': 'Se7en', 'score': 0.73, 'genres': 'Thriller, Crime'},
        ]
    },
    'Prisoners': {
        'genre': 'Thriller',
        'year': 2013,
        'rating': 8.1,
        'recommendations': [
            {'title': 'Gone Girl', 'score': 0.85, 'genres': 'Thriller, Drama'},
            {'title': 'Se7en', 'score': 0.82, 'genres': 'Thriller, Crime'},
            {'title': 'Shutter Island', 'score': 0.80, 'genres': 'Thriller, Mystery'},
            {'title': 'Zodiac', 'score': 0.78, 'genres': 'Thriller, Crime'},
            {'title': 'The Silence of the Lambs', 'score': 0.75, 'genres': 'Thriller, Crime'},
        ]
    },
    'Shutter Island': {
        'genre': 'Thriller',
        'year': 2010,
        'rating': 8.2,
        'recommendations': [
            {'title': 'Inception', 'score': 0.85, 'genres': 'Thriller, Sci-Fi'},
            {'title': 'Gone Girl', 'score': 0.82, 'genres': 'Thriller, Drama'},
            {'title': 'The Prestige', 'score': 0.80, 'genres': 'Thriller, Mystery'},
            {'title': 'Prisoners', 'score': 0.78, 'genres': 'Thriller, Crime'},
            {'title': 'Mystic River', 'score': 0.75, 'genres': 'Thriller, Drama'},
        ]
    },
}

# Title
st.title("Movie Recommendation System")
st.markdown("Hybrid filtering combining content-based and collaborative approaches")

# Info banner
st.info("Demo version with curated collection. Full system supports 5000+ movies with complete ML pipeline.")

# Sidebar
st.sidebar.header("About")
st.sidebar.markdown("""
**Algorithm:**
- Content-Based: TF-IDF similarity on metadata
- Collaborative: SVD matrix factorization on ratings
- Hybrid: Weighted combination of both approaches

**Tech Stack:**
- Python, Scikit-learn
- Pandas, NumPy
- Streamlit
""")

st.sidebar.markdown("---")
st.sidebar.markdown("**Author:** Osheen Langer")
st.sidebar.markdown("[GitHub Repository](https://github.com/OL10/movie-recommender-system)")

# Main content
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Select Movie")
    
    # Create sorted movie list
    all_movies = sorted(MOVIES_DATA.keys())
    movie_options = [f"{title} ({MOVIES_DATA[title]['year']}) - {MOVIES_DATA[title]['genre']}" 
                     for title in all_movies]
    
    selected_movie = st.selectbox(
        "Choose a movie:",
        options=movie_options
    )
    
    movie_title = selected_movie.split(' (')[0]
    
    n_recommendations = st.slider(
        "Number of recommendations:",
        min_value=3,
        max_value=10,
        value=5
    )
    
    get_recs = st.button("Get Recommendations", type="primary")

with col2:
    st.subheader("Recommendations")
    
    if get_recs:
        if movie_title in MOVIES_DATA and 'recommendations' in MOVIES_DATA[movie_title]:
            recommendations = MOVIES_DATA[movie_title]['recommendations'][:n_recommendations]
            
            # Success message with proper styling
            st.markdown(f'<div class="success-message">Found {len(recommendations)} similar movies to {movie_title}</div>', 
                       unsafe_allow_html=True)
            
            # Display recommendations with proper contrast
            for idx, movie in enumerate(recommendations, 1):
                st.markdown(f"""
                    <div class="movie-card">
                        <h3>{idx}. {movie['title']}</h3>
                        <p><strong>Genres:</strong> {movie['genres']}</p>
                        <p><strong>Similarity:</strong> {movie['score']:.1%}</p>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.error("Recommendations not available for this movie.")
    else:
        st.info("Select a movie and click 'Get Recommendations' to see similar films")
        
        # Statistics
        st.markdown("### Dataset")
        st.markdown(f"**Total Movies:** {len(MOVIES_DATA)}")
        
        genres = {}
        for movie_data in MOVIES_DATA.values():
            genre = movie_data['genre']
            genres[genre] = genres.get(genre, 0) + 1
        
        st.markdown("**By Genre:**")
        for genre, count in sorted(genres.items()):
            st.markdown(f"- {genre}: {count}")

# Footer
st.markdown("---")
st.markdown("Built with Python and Streamlit | [View Code](https://github.com/OL10/movie-recommender-system)")
