import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=82483e0943ec19de5a6eb33f508796f1'.format(movie_id))
    data = response.json()
    full_path = "https://image.tmdb.org/t/p/w500/" + str(data['poster_path'])
    return full_path


def recommend(movie_name):
    movie_index = movies[movies['title'] == movie_name].index[0]
    distances = sorted(list(enumerate(similarity[movie_index])), reverse=True, key=lambda x: x[1])

    reco = []
    rec_posters = []

    for i in distances[1:6]:
        movie_number = movies.iloc[i[0]].movie_id
        reco.append(movies.iloc[i[0]].title)
        # fetching the poster from the api
        rec_posters.append(fetch_poster(movie_number))
    return reco, rec_posters

st.title('Movie Recommendation System')

movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))
simi = pd.DataFrame(similarity)


option = st.selectbox(
    'Select your movie',
    movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(option)
    st.text("  ")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        col1.markdown(names[0])
        st.image(posters[0])
    with col2:
        col2.markdown(names[1])
        st.image(posters[1])
    with col3:
        col3.markdown(names[2])
        st.image(posters[2])
    with col4:
        col4.markdown(names[3])
        st.image(posters[3])
    with col5:
        col5.markdown(names[4])
        st.image(posters[4])
