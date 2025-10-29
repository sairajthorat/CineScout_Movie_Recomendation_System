import json
import streamlit as st
from omdb_utils import get_movie_details
from style_loader import load_css, truncate_to_words
import os
import pandas as pd
import re
import nltk
import joblib
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import logging

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s]%(levelname)s-%(message)s',
    handlers=[
        logging.FileHandler("preprocess.log",encoding="utf-8"),
        logging.StreamHandler()
    ]
)

nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')

stop_words=set(stopwords.words('english'))

try:
    df=pd.read_csv('movies.csv')
except Exception as e:
    raise e

def preprocess_text(text):
    text=re.sub(r"[^a-zA-Z\s]","",str(text))
    text=text.lower()
    tokens=word_tokenize(text)
    tokens=[word for word in tokens if word not in stop_words]
    return " ".join(tokens)

requried_columns=["genres","keywords","overview","title"]

df=df[requried_columns]

df=df.dropna().reset_index(drop=True)

df["combined"]=df['genres']+' '+df['keywords']+' '+df['overview']

df['cleaned_text']=df['combined'].apply(preprocess_text)

tfidf=TfidfVectorizer(max_features=5000)
tfidf_matrix=tfidf.fit_transform(df['cleaned_text'])

cosine_sim=cosine_similarity(tfidf_matrix,tfidf_matrix)


joblib.dump(df,'df_cleaned.pkl')
joblib.dump(tfidf_matrix,'tfidf_matrix.pkl')
joblib.dump(cosine_sim,'cosine_sim.pkl')



try:
    df=joblib.load('df_cleaned.pkl')
    cosine_sim=joblib.load('cosine_sim.pkl')
except Exception as e:
    raise e

def recommend_movies(movie_name,top_n=20):
    idx=df[df['title'].str.lower()==movie_name.lower()].index
    if len(idx)==0:
        return None
    idx=idx[0]

    sim_score=list(enumerate(cosine_sim[idx]))
    sim_score=sorted(sim_score,key=lambda x:x[1],reverse=True)[1:top_n+1]
    movie_indices=[i[0] for i in sim_score]

    result_df=df[['title']].iloc[movie_indices].reset_index(drop=True)
    result_df.index=result_df.index+1
    result_df.index.name="Sr.No."

    return result_df

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