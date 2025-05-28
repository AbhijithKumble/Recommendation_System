import streamlit as st
import requests
from PIL import Image
from io import BytesIO
from typing import Dict, Any
from config.settings import AVAILABLE_GENRES, RECOMMENDATION_METHODS, DEFAULT_ANIME_IMAGE, MAX_RECOMMENDATIONS, MIN_RECOMMENDATIONS


def display_header():
    """Display the main header of the application"""
    st.markdown("""
    <div class="main-header">
        <h1>🎌 AnimeNinja</h1>
        <p>Discover your next favorite anime with AI-powered recommendations</p>
    </div>
    """, unsafe_allow_html=True)


def display_sidebar():
    """Display sidebar with user preferences and return preferences dict"""
    st.sidebar.markdown(
        '<div class="sidebar-header"><h3>🎯 Preferences</h3></div>', unsafe_allow_html=True)

    # Recommendation type
    rec_type = st.sidebar.selectbox(
        "🔍 Recommendation Method",
        RECOMMENDATION_METHODS,
        help="Choose your preferred recommendation approach"
    )

    # Number of recommendations
    num_recs = st.sidebar.slider(
        "📊 Number of Recommendations",
        min_value=MIN_RECOMMENDATIONS,
        max_value=MAX_RECOMMENDATIONS,
        value=10,
        help="How many anime recommendations do you want?"
    )

    # Filters
    with st.sidebar.expander("🎨 Advanced Filters"):
        min_score = st.slider("Minimum Score", 0.0, 10.0, 7.0, 0.1)
        min_episodes = st.number_input("Minimum Episodes", 0, 2000, 1)
        max_episodes = st.number_input("Maximum Episodes", 1, 2000, 500)

        # Genre preferences
        preferred_genres = st.multiselect(
            "Preferred Genres",
            AVAILABLE_GENRES
        )

    return {
        'rec_type': rec_type,
        'num_recs': num_recs,
        'min_score': min_score,
        'min_episodes': min_episodes,
        'max_episodes': max_episodes,
        'preferred_genres': preferred_genres
    }


def display_anime_card(anime_data: Dict[str, Any], show_details: bool = True):
    """Display anime information in a beautiful card format"""
    with st.container():
        col1, col2 = st.columns([1, 3])

        with col1:
            image_url = anime_data.get('image_url', DEFAULT_ANIME_IMAGE)
            if image_url and image_url != DEFAULT_ANIME_IMAGE:
                try:
                    response = requests.get(image_url, timeout=10)
                    img = Image.open(BytesIO(response.content))
                    st.image(img, width=150)
                except Exception as e:
                    st.image(DEFAULT_ANIME_IMAGE, width=150)
            else:
                st.image(DEFAULT_ANIME_IMAGE, width=150)

        with col2:
            title = anime_data.get('title', 'Unknown Title')
            st.markdown(f"### {title}")

            if show_details:
                # Score badge
                score = anime_data.get('score', 0)
                if score and score > 0:
                    st.markdown(f'<span class="score-badge">⭐ {score:.1f}</span>',
                                unsafe_allow_html=True)

                # Basic info
                col2a, col2b, col2c = st.columns(3)
                with col2a:
                    episodes = anime_data.get('episodes', 'N/A')
                    st.metric("Episodes", episodes if episodes else 'N/A')
                with col2b:
                    year = anime_data.get('year', 'N/A')
                    st.metric("Year", year if year else 'N/A')
                with col2c:
                    status = anime_data.get('status', 'N/A')
                    st.metric("Status", status if status else 'N/A')

                # Genres
                genres = anime_data.get('genres', [])
                if genres:
                    st.markdown("**Genres:**")
                    genres_html = ""
                    for genre in genres[:5]:  # Limit to 5 genres
                        genres_html += f'<span class="genre-tag">{genre}</span>'
                    st.markdown(genres_html, unsafe_allow_html=True)

                # Synopsis
                synopsis = anime_data.get('synopsis', '')
                if synopsis:
                    with st.expander("📖 Synopsis"):
                        synopsis_text = synopsis[:300] + \
                            "..." if len(synopsis) > 300 else synopsis
                        st.write(synopsis_text)


def display_loading_message(message: str = "Loading..."):
    """Display a loading message with spinner"""
    return st.spinner(message)


def display_success_message(message: str):
    """Display a success message"""
    st.markdown(
        f'<div class="success-message">{message}</div>', unsafe_allow_html=True)


def display_error_message(message: str):
    """Display an error message"""
    st.markdown(
        f'<div class="error-message">{message}</div>', unsafe_allow_html=True)


def display_info_message(message: str):
    """Display an info message"""
    st.info(message)


def display_warning_message(message: str):
    """Display a warning message"""
    st.warning(message)


def display_metric_card(title: str, value: str, description: str = ""):
    """Display a metric in a card format"""
    st.markdown(f'''
    <div class="metric-card">
        <h3>{value}</h3>
        <p>{title}</p>
        {f"<small>{description}</small>" if description else ""}
    </div>
    ''', unsafe_allow_html=True)


def display_footer():
    """Display the footer of the application"""
    st.markdown("---")
    st.markdown("""
    <div class="footer">
        <p>Made with ❤️ using Streamlit | Powered by AI & MyAnimeList API</p>
        <p><small>AnimeNinja - Your personal anime discovery companion</small></p>
    </div>
    """, unsafe_allow_html=True)
