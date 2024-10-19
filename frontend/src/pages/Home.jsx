import React, { useState } from 'react';
import './Home.css'

const Home = () => {
    const [searchQuery, setSearchQuery] = useState('');
    const [titles, setMovieTitles] = useState([]);
    const [recommendations, setRecommendations] = useState({ movies: [], posters: [] });
    const [showRecommendations, setShowRecommendations] = useState(false);

    // Fetch movie titles based on the search query
    const handleSearch = async (query) => {
        setSearchQuery(query);
        if (query.length > 0) {
            try {
                const response = await fetch(`http://127.0.0.1:5000/titles-list?q=${query}`);
                const data = await response.json();
                setMovieTitles(data);  // Set the fetched movie titles
            } catch (error) {
                console.error('Error fetching movie titles:', error);
            }
        } else {
            setMovieTitles([]);
        }
    };

    // Fetch recommendations based on selected movie and hide search results
    const handleMovieSelect = async (movie) => {
        try {
            const response = await fetch(`http://127.0.0.1:5000/recommend?title=${movie}`);
            const data = await response.json();
            setRecommendations({
                movies: data.movies || [],  // Set movie titles
                posters: data.posters || []  // Set movie posters
            });
            setShowRecommendations(true);  // Hide search results and show recommendations
        } catch (error) {
            console.error('Error fetching recommendations:', error);
        }
    };

    return (
        <div className="page-container">
            <div className="inner-container">
                <h1>CineWatch</h1>

                <div className="search-container">
                    <input
                        type="search"
                        className="search-input"
                        placeholder="Search for movies ..."
                        value={searchQuery}
                        onChange={(e) => handleSearch(e.target.value)}
                    />

                    {
                        <div className="search-results">
                            {titles.map((title, index) => (
                                <li key={index} onClick={() => handleMovieSelect(title)}>
                                    {title}
                                </li>
                            ))}
                        </div>
                    }
                </div>

                {showRecommendations && recommendations.movies.length > 0 && (
                    <div className="recommendations-container">
                        {recommendations.movies.map((movie, index) => (
                            <div key={index} className="movie-card">
                                <img
                                    src={recommendations.posters[index]}
                                    alt={movie}
                                    className="movie-poster"
                                />
                                <h2>{movie}</h2>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
};

export default Home;
