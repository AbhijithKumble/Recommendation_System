import streamlit as st
import time
import pandas as pd
from typing import Dict, Any
from utils.jikan_api import fetch_anime_details_by_id
from utils.recommendation_handler import get_recommendations_by_method, apply_filters
from utils.analytics import (
    display_recommendation_statistics,
    create_genre_distribution_chart,
    create_score_distribution_chart,
    create_year_distribution_chart,
    analyze_user_history,
    create_history_charts
)
from ui.components import (
    display_anime_card,
    display_success_message,
    display_error_message,
    display_warning_message,
    display_info_message
)


def recommendations_tab(preferences: Dict[str, Any]):
    """
    Main recommendations tab

    Args:
        preferences: User preferences dictionary
    """
    st.markdown("## 🎯 Personalized Recommendations")

    # Input methods
    input_method = st.radio(
        "How would you like to get recommendations?",
        ["Enter Anime ID", "Search by Title", "Random Discovery"],
        horizontal=True
    )

    anime_input = None

    if input_method == "Enter Anime ID":
        anime_input = st.number_input(
            "Enter MyAnimeList ID:",
            min_value=1,
            help="You can find the ID in the URL of any anime on MyAnimeList"
        )

    elif input_method == "Search by Title":
        anime_input = st.text_input(
            "Enter anime title:",
            placeholder="e.g., Attack on Titan, Naruto, One Piece..."
        )

    else:  # Random Discovery
        if st.button("🎲 Discover Random Anime"):
            anime_input = "random"

    # Get recommendations button
    if st.button("🚀 Get Recommendations", type="primary"):
        if anime_input:
            with st.spinner("🔍 Finding perfect matches for you..."):
                try:
                    # Get models from session state
                    content_models = st.session_state.get('content_models')
                    collab_models = st.session_state.get('collab_models')

                    if not content_models or not collab_models:
                        display_error_message(
                            "❌ Models not loaded. Please refresh the page.")
                        return

                    # Get recommendations based on method
                    recommendations = get_recommendations_by_method(
                        preferences['rec_type'],
                        anime_input,
                        content_models,
                        collab_models,
                        preferences['num_recs']
                    )

                    if recommendations:
                        # Apply user filters
                        filtered_recs = apply_filters(
                            recommendations, preferences)

                        if filtered_recs:
                            display_success_message(
                                f"🎉 Found {len(filtered_recs)} perfect matches!")

                            # Display recommendations
                            for i, rec in enumerate(filtered_recs, 1):
                                with st.container():
                                    st.markdown(
                                        f'<div class="recommendation-card">', unsafe_allow_html=True)
                                    st.markdown(f"#### #{i} Recommendation")
                                    display_anime_card(rec)
                                    st.markdown(
                                        '</div>', unsafe_allow_html=True)

                            # Add to history
                            st.session_state.recommendation_history.append({
                                'timestamp': time.time(),
                                'input': str(anime_input),
                                'method': preferences['rec_type'],
                                'results': len(filtered_recs),
                                'total_found': len(recommendations)
                            })

                            # Display statistics
                            display_recommendation_statistics(filtered_recs)

                            # Display charts
                            col1, col2 = st.columns(2)

                            with col1:
                                genre_chart = create_genre_distribution_chart(
                                    filtered_recs)
                                if genre_chart:
                                    st.plotly_chart(
                                        genre_chart, use_container_width=True)

                            with col2:
                                score_chart = create_score_distribution_chart(
                                    filtered_recs)
                                if score_chart:
                                    st.plotly_chart(
                                        score_chart, use_container_width=True)
                        else:
                            display_warning_message(
                                "😅 No anime found matching your filters. Try adjusting your preferences!")

                            # Show what was filtered out
                            if recommendations:
                                st.info(
                                    f"Found {len(recommendations)} recommendations before filtering")
                    else:
                        display_error_message(
                            "❌ No recommendations found. Please try a different input.")

                except Exception as e:
                    display_error_message(
                        f"❌ Error getting recommendations: {str(e)}")
                    st.exception(e)  # For debugging
        else:
            display_warning_message(
                "⚠️ Please provide an input to get recommendations!")


def search_tab():
    """Search anime by ID tab"""
    st.markdown("## 🔍 Search & Explore")

    search_id = st.number_input(
        "Search by MyAnimeList ID:", min_value=1, value=1)

    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("🔍 Search Anime", type="primary"):
            with st.spinner("Fetching anime details..."):
                try:
                    anime_details = fetch_anime_details_by_id(search_id)
                    if anime_details:
                        display_success_message("✅ Anime found!")
                        st.markdown(
                            '<div class="recommendation-card">', unsafe_allow_html=True)
                        display_anime_card(anime_details)
                        st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        display_error_message(
                            "❌ Anime not found. Please check the ID.")
                except Exception as e:
                    display_error_message(f"❌ Error fetching anime: {str(e)}")

    with col2:
        if st.button("🎲 Random Anime"):
            import random
            random_id = random.randint(1, 50000)  # MyAnimeList ID range
            with st.spinner(f"Fetching random anime (ID: {random_id})..."):
                try:
                    anime_details = fetch_anime_details_by_id(random_id)
                    if anime_details:
                        display_success_message(
                            f"✅ Random anime found! (ID: {random_id})")
                        st.markdown(
                            '<div class="recommendation-card">', unsafe_allow_html=True)
                        display_anime_card(anime_details)
                        st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.info("Anime not found, trying another random ID...")
                        st.rerun()
                except Exception as e:
                    display_error_message(
                        f"❌ Error fetching random anime: {str(e)}")

    # Popular anime suggestions
    st.markdown("### 🌟 Popular Anime to Try")
    st.markdown("Here are some popular anime IDs you can search for:")

    popular_anime = {
        "Attack on Titan": 16498,
        "Death Note": 1535,
        "One Piece": 21,
        "Naruto": 20,
        "Dragon Ball Z": 813,
        "My Hero Academia": 31964,
        "Demon Slayer": 38000,
        "One Punch Man": 30276
    }

    cols = st.columns(4)
    for i, (title, anime_id) in enumerate(popular_anime.items()):
        with cols[i % 4]:
            if st.button(f"{title}\n(ID: {anime_id})", key=f"popular_{anime_id}"):
                st.session_state.search_id = anime_id
                st.rerun()


def analytics_tab():
    """Analytics and statistics tab"""
    st.markdown("## 📊 Recommendation Analytics")

    if st.session_state.recommendation_history:
        analysis = analyze_user_history(
            st.session_state.recommendation_history)

        # Overview metrics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Searches", analysis.get('total_searches', 0))

        with col2:
            avg_results = analysis.get('avg_results', 0)
            st.metric("Avg Results per Search", f"{avg_results:.1f}")

        with col3:
            method_dist = analysis.get('method_distribution', {})
            most_used_method = max(
                method_dist.keys(), key=lambda k: method_dist[k]) if method_dist else "N/A"
            st.metric("Most Used Method", most_used_method)

        with col4:
            date_range = analysis.get('date_range', {})
            if date_range.get('start') and date_range.get('end'):
                days_active = (date_range['end'] -
                               date_range['start']).days + 1
                st.metric("Days Active", days_active)
            else:
                st.metric("Days Active", 1)

        # Charts
        method_fig, activity_fig = create_history_charts(
            st.session_state.recommendation_history)

        col1, col2 = st.columns(2)

        with col1:
            if method_fig:
                st.plotly_chart(method_fig, use_container_width=True)

        with col2:
            if activity_fig:
                st.plotly_chart(activity_fig, use_container_width=True)

        # Detailed breakdown
        st.markdown("### 📈 Detailed Breakdown")

        history_df = pd.DataFrame(st.session_state.recommendation_history)
        history_df['datetime'] = pd.to_datetime(
            history_df['timestamp'], unit='s')
        history_df = history_df.sort_values('datetime', ascending=False)

        # Display recent activity table
        st.markdown("#### Recent Activity")
        display_df = history_df[['datetime',
                                 'input', 'method', 'results']].head(10)
        display_df['datetime'] = display_df['datetime'].dt.strftime(
            '%Y-%m-%d %H:%M:%S')
        st.dataframe(display_df, use_container_width=True)

    else:
        display_info_message(
            "📈 Start getting recommendations to see analytics here!")

        # Show sample analytics
        st.markdown("### 🔮 What You'll See Here")
        st.markdown("""
        Once you start using the recommendation system, you'll see:
        - **Usage Statistics**: Total searches, average results, most used methods
        - **Activity Charts**: Visual representation of your usage patterns
        - **Method Analysis**: Which recommendation methods work best for you
        - **Timeline**: Your recommendation history over time
        """)


def history_tab():
    """Recommendation history tab"""
    st.markdown("## 📝 Recommendation History")

    if st.session_state.recommendation_history:
        # Controls
        col1, col2, col3 = st.columns([2, 1, 1])

        with col1:
            show_all = st.checkbox("Show all history", value=False)

        with col2:
            if st.button("📊 Export History"):
                history_df = pd.DataFrame(
                    st.session_state.recommendation_history)
                csv = history_df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="anime_recommendation_history.csv",
                    mime="text/csv"
                )

        with col3:
            if st.button("🗑️ Clear History", type="secondary"):
                if st.button("⚠️ Confirm Clear", type="primary"):
                    st.session_state.recommendation_history = []
                    display_success_message("History cleared!")
                    st.rerun()

        # Display history
        history_to_show = st.session_state.recommendation_history if show_all else st.session_state.recommendation_history[
            -10:]

        for i, entry in enumerate(reversed(history_to_show), 1):
            timestamp = time.strftime(
                '%Y-%m-%d %H:%M:%S', time.localtime(entry['timestamp']))

            with st.expander(f"Search #{len(st.session_state.recommendation_history) - len(history_to_show) + i} - {timestamp}"):
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.write(f"**Input:** {entry['input']}")

                with col2:
                    st.write(f"**Method:** {entry['method']}")

                with col3:
                    st.write(f"**Results:** {entry['results']}")

                with col4:
                    total_found = entry.get('total_found', entry['results'])
                    if total_found != entry['results']:
                        st.write(f"**Total Found:** {total_found}")
                        st.write(
                            f"**Filtered:** {total_found - entry['results']}")

        if len(st.session_state.recommendation_history) > 10 and not show_all:
            st.info(
                f"Showing latest 10 entries. Total history: {len(st.session_state.recommendation_history)} entries")

    else:
        display_info_message("📝 Your recommendation history will appear here!")

        st.markdown("### 🎯 How History Works")
        st.markdown("""
        Every time you get recommendations, we'll save:
        - **Timestamp**: When you made the request
        - **Input**: What anime or criteria you used
        - **Method**: Which recommendation algorithm you chose
        - **Results**: How many recommendations were found
        
        You can export your history as CSV or clear it anytime.
        """)
