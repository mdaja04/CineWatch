import React, { useEffect, useState } from 'react';
import './Movie.css';
import { useLocation, useNavigate } from "react-router-dom";

const Movie = () => {
    const navigate = useNavigate();
    const { state } = useLocation();
    const { movie } = state || {};
    const [poster, setPoster] = useState(null);
    const [backdrop, setBackdrop] = useState(null);
    const [movieDetails, setMovieDetails] = useState(null);
    const [recommendations, setRecommendations] = useState({ movies: [], posters: [] });

    useEffect(() => {
        const fetchMovieData = async () => {
            try {
                const response = await fetch(`http://127.0.0.1:5000/get-details?title=${movie}`);
                const data = await response.json();
                setPoster(`https://image.tmdb.org/t/p/w500${data.poster_path}`);
                setBackdrop(`https://image.tmdb.org/t/p/w1280${data.backdrop_path}`);
                setMovieDetails(data);
            } catch (error) {
                console.error('Error fetching movie details:', error);
            }
        };

        const fetchRecommendations = async (movie) => {
            try {
                const response = await fetch(`http://127.0.0.1:5000/recommend?title=${movie}`);
                const data = await response.json();
                setRecommendations({
                    movies: data.movies || [],  // Set movie titles
                    posters: data.posters || []  // Set movie posters
                });
            } catch (error) {
                console.error('Error fetching recommendations:', error);
            }
        };

        if (movie) {
            fetchMovieData();
            fetchRecommendations(movie);  // Call this function with the movie title
        }
    }, [movie]);

    function openMoviePage(movie) {
        navigate(`/movie/${movie}`, { state: { movie, recommendations } });
    }

    const formatGenres = (genres) => genres ? genres.map(genre => genre.name).join(', ') : '';

    return (
        <div className="page-container">
            {backdrop && (
                <div className="background-container" style={{backgroundImage: `url(${backdrop})`}}>
                    <div className="content-container">
                        <div className="poster-container">
                            <img src={poster} alt={`${movieDetails?.title} Poster`} className="poster-image"/>
                        </div>
                        {movieDetails && (
                            <div className="details-container">
                                <h1 className="movie-title">{movieDetails.title}</h1>
                                <p className="movie-tagline">{movieDetails.tagline}</p>
                                <div className="movie-info">
                                    <span className="rating">★ {movieDetails.vote_average}</span>
                                    <span className="year">{new Date(movieDetails.release_date).getFullYear()}</span>
                                    <span className="runtime">{movieDetails.runtime} mins</span>
                                    <span className="genres">{formatGenres(movieDetails.genres)}</span>
                                </div>
                                <p className="movie-description">{movieDetails.overview}</p>
                                <div className="action-buttons">
                                    <button className="play-button">Where to Watch</button>
                                    <button className="watchlist-button">+ Add to Watchlist</button>
                                </div>
                            </div>
                        )}
                    </div>
                </div>
            )}

            {recommendations.movies.length > 0 && (
                <div className="recommendations-container">
                    {recommendations.movies.map((movie, index) => (
                        <div key={index} className="movie-card" onClick={() => openMoviePage(movie)}>
                            <img src={recommendations.posters[index]} alt={movie} className="movie-poster"/>
                            <h2>{movie}</h2>
                        </div>
                    ))}
                </div>
            )}
        </div>

    );
};

export default Movie;
