import json
import streamlit as st
import os
from omdb_utils import get_movie_details
from recommend import df, recommend_movies
from style_loader import load_css, truncate_to_words
import os


if not os.path.exists('df_cleaned.pkl'):
    import preprocess

# Load configuration - use environment variable in production, fallback to config file locally
try:
    OMDB_API_KEY = os.environ.get("OMDB_API_KEY")
    if not OMDB_API_KEY:
        config = json.load(open("config.json"))
        OMDB_API_KEY = config["OMDB_API_KEY"]
except FileNotFoundError:
    OMDB_API_KEY = os.environ.get("OMDB_API_KEY", "your_api_key_here")

# Page configuration
st.set_page_config(
    page_title="CineScout-Movie Recommendation System",
    page_icon="🎬",
    layout="wide"
)

# Load custom CSS
load_css("styles.css")

# Main header with custom styling
st.markdown('<h1 class="main-header">🎬 CineScout</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666; margin-bottom: 2rem;">Discover your next favorite movie with AI-powered recommendations</p>', unsafe_allow_html=True)

# Movie selection with better styling
st.markdown("### 🎯 Choose Your Movie")
movie_list = sorted(df['title'].dropna().unique())
selected_movie = st.selectbox("Select a movie you enjoyed:", movie_list, help="Pick any movie from our database to get personalized recommendations")

# Center the button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    recommend_clicked = st.button("🚀 Get Recommendations", use_container_width=True)

# Handle recommendations outside the column layout for full width
if recommend_clicked:
    with st.spinner("🔍 Finding similar movies..."):
        recommendations = recommend_movies(selected_movie)
        if recommendations is None or recommendations.empty:
            st.error("😔 Sorry, no recommendations found for this movie.")
        else:
            st.balloons()  # Fun animation
            st.markdown("### 🌟 Movies You Might Love")
            
            # Create horizontal grid layout with 5 cards per row - full width
            recommendations_list = list(recommendations.iterrows())
            
            # Process movies in chunks of 5
            for i in range(0, len(recommendations_list), 5):
                chunk = recommendations_list[i:i+5]
                # Create 5 equal columns with small gaps for full width distribution
                cols = st.columns(5, gap="small")
                
                for j, (_, row) in enumerate(chunk):
                    movie_title = row['title']
                    plot, poster = get_movie_details(movie_title, OMDB_API_KEY)
                    truncated_plot = truncate_to_words(plot, 65)
                    
                    with cols[j]:
                        # Create movie card
                        if poster != "N/A":
                            poster_html = f'<img src="{poster}" class="movie-poster" alt="{movie_title}">'
                        else:
                            poster_html = '<div class="movie-poster-placeholder">🎬</div>'
                        
                        st.markdown(f"""
                        <div class="movie-card">
                            {poster_html}
                            <div class="movie-title">{movie_title}</div>
                            <div class="movie-plot">{truncated_plot}</div>
                        </div>
                        """, unsafe_allow_html=True)