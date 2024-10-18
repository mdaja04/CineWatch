from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle

app = Flask(__name__)
CORS(app)

movies = pickle.load(open("movies_list.pkl", 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))


@app.route('/titles-list', methods=['GET'])
def get_movie_titles():
    query = request.args.get('q', '').lower()
    if query:
        filtered_movies = [movie for movie in movies['title'].values if query in movie.lower()]
        filtered_movies = filtered_movies[:10]
    else:
        filtered_movies = []

    return jsonify(filtered_movies)

@app.route('/recommend', methods=['GET'])
def get_movie_recommendation():
    query = request.args.get('title', '').lower()
    if query:
        index = movies[movies['title'].str.lower() == query].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])

        recommended_movies = []
        recommended_posters = []

        for i in distances[1:6]:
            movie_id = movies.iloc[i[0]].id
            recommended_movies.append(movies.iloc[i[0]].title)
            #recommended_posters.append(fetch_poster(movie_id))

        return jsonify({
            'movies': recommended_movies,
            # 'posters': recommended_posters  # Include this if posters are being fetched
        })
    return jsonify({'error': 'No movie title provided'}), 400


if __name__ == '__main__':
    app.run(debug=True)
