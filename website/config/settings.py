# Configuration settings for the Streamlit app

PAGE_CONFIG = {
    "page_title": "AnimeNinja - Smart Recommendations",
    "page_icon": "🎌",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Default preferences
DEFAULT_PREFERENCES = {
    'rec_type': 'Hybrid (Best)',
    'num_recs': 10,
    'min_score': 7.0,
    'min_episodes': 1,
    'max_episodes': 500,
    'preferred_genres': []
}

# Available genres for filtering
AVAILABLE_GENRES = [
    "Action", "Adventure", "Comedy", "Drama", "Fantasy", "Horror", 
    "Mystery", "Romance", "Sci-Fi", "Slice of Life", "Sports", "Thriller",
    "Supernatural", "School", "Military", "Historical", "Music", "Psychological"
]

# Recommendation method options
RECOMMENDATION_METHODS = [
    "Hybrid (Best)", 
    "Content-Based", 
    "Collaborative Filtering"
]

# Default anime image URL for missing images
DEFAULT_ANIME_IMAGE = "https://via.placeholder.com/150x200?text=No+Image"

# Maximum number of recommendations
MAX_RECOMMENDATIONS = 20
MIN_RECOMMENDATIONS = 5

# History settings
MAX_HISTORY_ITEMS = 50
