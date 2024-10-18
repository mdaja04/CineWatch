import pickle
from tmdb import fetch_poster

movies = pickle.load(open("movies_list.pkl", 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

def get_movies_list():
    return movies['title'].values

def get_recommendations(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])

    recommended_movies = []
    recommended_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters



