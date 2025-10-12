import json
import streamlit as st
from omdb_utils import get_movie_details
from recommend import df,recommend_movies

config=json.load(open("config.json"))

OMDB_API_KEY=config["OMDB_API_KEY"]

st.set_page_config(
    page_title="CineScout-Movie Recomendation System",
    page_icon="🎬",
    layout="centered"
)

st.title("CineScout")

movie_list=sorted(df['title'].dropna().unique())
selected_movie=st.selectbox("🎬 Select a movie:",movie_list)

if(st.button,"🚀 Recommend Similar Movies"):
    with st.spinner("Finding Similar Movies ....."):
        recommendations=recommend_movies(selected_movie)
        if recommendations is None or recommendations.empty:
            st.warning("Sorry,No Recommendation Found.")
        else:
            st.success("Top Similar Movies:")
            for _,row in recommendations.iterrows():
                movie_title=row['title']
                plot,poster=get_movie_details(movie_title,OMDB_API_KEY)

                with st.container():
                    coll,col2=st.columns([1,3])
                    with coll:
                        if poster != "N/A":
                            st.image(poster,width=100)
                        else:
                            st.write("❌ No Poster Found")
                    
                    with col2:

                        st.markdown(f"###{movie_title}")
                        st.markdown(f"*{plot}*" if plot != "N/A" else "_Plot not available")