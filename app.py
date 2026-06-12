import streamlit as st
import pickle
import pandas as pd


# def fetch_poster(movie_id):
#     response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=691efba03d2b449792789ad52b8ff4ae=en-US'.format(movie_id))
#     data=response.json()
#     #return "https://image.tmdb.org/t/p/w500/"+ data['poster_path'] # not a complete path
#     return "https://image.tmdb.org/t/p/original"+ data['poster_path']
import requests

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=691efba03d2b449792789ad52b8ff4ae"

    response = requests.get(url)
    data = response.json()

    poster_path = data.get('poster_path')

    if poster_path:
        return f"https://image.tmdb.org/t/p/w500{data['poster_path']}"
    else:
        return "https://via.placeholder.com/500x750?text=No+Poster"
def recommend(movie):
    movies_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movies_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies=[]
    recommended_movies_posters=[]
    for i in movies_list:
        #movie_id=i[0]
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters
movies_dict=pickle.load(open('movies_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)
similarity=pickle.load(open('similarity.pkl','rb'))
st.title('Movie Recommended System')
selected_movie_name=st.selectbox(
    'What would you like to?',
    movies['title'].values)

if st.button('Recommend'):
    names,posters=recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])

