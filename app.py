import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
from config import TMDB_API_KEY, TMDB_ACCESS_TOKEN

app = Flask(__name__)
CORS(app)

movies = pickle.load(open("movies_list.pkl", 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

@app.route('/get-details', methods=['GET'])  # Make sure the route has a leading '/'
def get_details():
    title = request.args.get('title').lower()

    if title:
        try:
            # Find the movie ID by title
            index = movies[movies['title'].str.lower() == title].index[0]
            movie_id = movies.iloc[index].id
        except IndexError:
            return {'error': 'Movie not found'}, 404  # If no movie is found, return 404
    else:
        return {'error': 'No title provided'}, 400  # Return 400 if no title is provided

    # Fetch movie details from TMDB
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {TMDB_ACCESS_TOKEN}"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()  # Parse the response JSON
        print(data)
        return data  # Return the JSON data, Flask will convert it to a proper response
    else:
        return {'error': 'Failed to fetch movie details from TMDB'}, response.status_code


@app.route('/get-images', methods=['GET'])
def get_images():
    # Get the title from the request
    title = request.args.get('title', '').lower()

    # Find the movie ID using the title in the movies DataFrame
    if title:
        try:
            # Find the movie ID based on the title
            index = movies[movies['title'].str.lower() == title].index[0]
            movie_id = movies.iloc[index].id  # Get the movie ID for the matched title
        except IndexError:
            return {'error': 'Movie not found'}, 404  # If no movie is found, return 404
    else:
        return {'error': 'No title provided'}, 400  # Return 400 if no title is provided

    images = []
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/images?language=en"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {TMDB_ACCESS_TOKEN}"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()

            # Get poster image
            if 'posters' in data and len(data['posters']) > 0:
                poster_path = data['posters'][0]['file_path']
                full_poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
                images.append(full_poster_url)

                # Get backdrop image
            if 'backdrops' in data and len(data['backdrops']) > 0:
                backdrop_path = f"https://image.tmdb.org/t/p/w500{data['backdrops'][0]['file_path']}"
                images.append(backdrop_path)

            return {'images': images}, 200  # Return images as a JSON response
        else:
            return {'error': 'Failed to fetch images from TMDB'}, response.status_code
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}, 500


def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/images?language=en"
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
