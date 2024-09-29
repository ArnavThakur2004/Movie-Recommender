# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 09:15:21 2024

@author: arnav
"""

import pickle
import streamlit as st
import requests

# Function to fetch movie poster using the TMDB API
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
        data = requests.get(url).json()
        poster_path = data.get('poster_path', '')
        full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}" if poster_path else ""
        return full_path
    except:
        return ""

# Recommendation function to get movie names and posters
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    
    recommended_movie_names = []
    recommended_movie_posters = []
    
    for i in distances[1:6]:  # Recommend top 5 movies
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    
    return recommended_movie_names, recommended_movie_posters

# Streamlit app layout
st.title('Movie Recommender System')

# Load the pre-trained data from pickle files
movies = pickle.load(open('model/movie_list.pkl', 'rb'))
similarity = pickle.load(open('model/similarity.pkl', 'rb'))

movie_list = movies['title'].values

# Movie selection dropdown
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

# Display recommendations on button click
if st.button('Show Recommendation'):
    with st.spinner('Fetching recommendations...'):
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
        
        # Displaying movies in a more structured manner
        if recommended_movie_names:
            col1, col2, col3, col4, col5 = st.columns(5)
            cols = [col1, col2, col3, col4, col5]
            
            for idx, col in enumerate(cols):
                col.text(recommended_movie_names[idx])
                if recommended_movie_posters[idx]:
                    col.image(recommended_movie_posters[idx], use_column_width=True)
                else:
                    col.text("No Image Available")
        else:
            st.error('No recommendations found!')

# Footer section
st.write("Built with Streamlit by Arnav Thakur")
