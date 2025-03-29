#!/usr/bin/env python
# coding: utf-8

# In[5]:


import streamlit as st
import requests
import random

# API Key
API_KEY = "57583f37"
BASE_URL = "http://www.omdbapi.com/"

# Function to fetch movie details
def get_movie_details(title):
    url = f"{BASE_URL}?t={title}&apikey={API_KEY}"
    response = requests.get(url).json()
    return response if response.get("Response") == "True" else None

# Function to fetch recommended movies based on genre
def get_recommended_movies(genre):
    url = f"{BASE_URL}?s={genre}&apikey={API_KEY}"
    response = requests.get(url).json()
    movies = response.get("Search", [])  # Get movies list

    # Randomly shuffle and limit to 5 unique movies
    random.shuffle(movies)
    return movies[:5] if movies else []  

# Function to display movie details
def display_movie_details(movie):
    st.image(movie["Poster"], width=200)
    st.markdown(f"### {movie['Title']} ({movie['Year']})")
    st.write(f"**🎭 Genre:** {movie['Genre']}")
    st.write(f"**⭐ IMDb Rating:** {movie['imdbRating']}")
    st.write(f"**📜 Plot:** {movie['Plot']}")
    st.write(f"**🎬 Director:** {movie['Director']}")
    st.write(f"**✍ Writer:** {movie['Writer']}")
    st.write(f"**🎭 Actors:** {movie['Actors']}")

# Streamlit UI
st.title("🎬 Movie Recommendation System")
search_query = st.text_input("🔎 Search for a Movie")

# Handle user search input
if search_query:
    movie_details = get_movie_details(search_query)
    if movie_details:
        st.subheader("🎬 Searched Movie")
        display_movie_details(movie_details)

        # Fetch related movies based on the first genre (if available)
        genres = movie_details["Genre"].split(", ") if "Genre" in movie_details else []
        first_genre = genres[0] if genres else None

        if first_genre:
            recommended_movies = get_recommended_movies(first_genre)
            if recommended_movies:
                st.subheader("🎥 Recommended Movies (Different Each Search)")

                # Display recommended movies dynamically
                cols = st.columns(5)
                for i, movie in enumerate(recommended_movies):
                    with cols[i]:
                        if "Poster" in movie and movie["Poster"] != "N/A":
                            if st.button("🎬 " + movie["Title"], key=movie['imdbID']):
                                st.session_state["selected_movie"] = movie["Title"]
                            st.image(movie["Poster"], width=120)
                        else:
                            st.write(movie["Title"])  # If no poster is available, show only title

        # If a recommended movie is clicked, display its details
        if "selected_movie" in st.session_state:
            st.subheader("🎬 Selected Movie Details")
            selected_movie_details = get_movie_details(st.session_state["selected_movie"])
            if selected_movie_details:
                display_movie_details(selected_movie_details)
    else:
        st.error("❌ No movies found. Try another title.")


# In[ ]:




