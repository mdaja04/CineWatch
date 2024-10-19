import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
from config import TMDB_API_KEY, TMDB_ACCESS_TOKEN

app = Flask(__name__)
CORS(app)

movies = pickle.load(open("movies_list.pkl", 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))


def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/images"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {TMDB_ACCESS_TOKEN}"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()

            # Check if 'posters' exists and is not empty
            if 'posters' in data and len(data['posters']) > 0:
                # Get the first poster image from the list
                poster_path = data['posters'][0]['file_path']  # Access the first poster's file path
                full_poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"  # TMDB image base URL with size w500

                return full_poster_url  # Return the full poster URL
            else:
                return None  # No poster found
        else:
            return None  # Handle non-200 responses
    except requests.exceptions.RequestException as e:
        print(f"Error fetching poster: {e}")
        return None


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


        for i in distances[1:10]:
            movie_id = movies.iloc[i[0]].id
            recommended_movies.append(movies.iloc[i[0]].title)
            recommended_posters.append(fetch_poster(movie_id))


        return jsonify({
            'movies': recommended_movies,
            'posters': recommended_posters
        })
    return jsonify({'error': 'No movie title provided'}), 400


if __name__ == '__main__':
    app.run(debug=True)
