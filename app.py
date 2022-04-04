import pickle
import streamlit as st
import requests

st.header('Movie Recommender System Using Machine Learning')
movies = pickle.load(open('artifacts/movie_list.pkl','rb'))
similarity = pickle.load(open('artifacts/similarity.pkl','rb'))


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url).json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500{}".format(poster_path)
    return full_path

def recommend(movie):
    index = movies[movies['title']==movie].index[0]
    distance = sorted(list(enumerate(similarity[index])),key=lambda x:x[1],reverse=True)
    recommended_movie_names = []
    recommended_movie_poster = []
    for i in distance[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]]['id']
        recommended_movie_poster.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]]['title'])
    return recommended_movie_names,recommended_movie_poster

movies_list = movies['title'].values
selected_movie = st.selectbox('Select or type a movie name',movies_list)

if st.button('Show Recommendations'):
    recommended_movie_names,recommended_movie_poster = recommend(selected_movie)
    col1,col2,col3,col4,col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_poster[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_poster[1])
    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_poster[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_poster[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_poster[4])