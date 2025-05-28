import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import List, Dict, Any
from collections import Counter


def calculate_recommendation_stats(recommendations: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculate statistics for a list of recommendations

    Args:
        recommendations: List of recommendation dictionaries

    Returns:
        Dict: Statistics about the recommendations
    """
    if not recommendations:
        return {}

    # Calculate average score
    scores = [r.get('score', 0) for r in recommendations if r.get('score')]
    avg_score = sum(scores) / len(scores) if scores else 0

    # Get all genres
    all_genres = []
    for rec in recommendations:
        genres = rec.get('genres', [])
        if isinstance(genres, list):
            all_genres.extend(genres)

    # Most common genre
    genre_counts = Counter(all_genres)
    most_common_genre = genre_counts.most_common(
        1)[0][0] if genre_counts else "N/A"

    # Calculate average episodes
    episodes_list = [r.get('episodes', 0) for r in recommendations if r.get(
        'episodes') and r.get('episodes') > 0]
    avg_episodes = sum(episodes_list) / \
        len(episodes_list) if episodes_list else 0

    # Most common year
    years = [r.get('year') for r in recommendations if r.get('year')]
    year_counts = Counter(years)
    most_common_year = year_counts.most_common(
        1)[0][0] if year_counts else "N/A"

    return {
        'avg_score': avg_score,
        'most_common_genre': most_common_genre,
        'avg_episodes': avg_episodes,
        'most_common_year': most_common_year,
        'total_recommendations': len(recommendations),
        'genre_distribution': dict(genre_counts),
        'year_distribution': dict(year_counts)
    }


def display_recommendation_statistics(recommendations: List[Dict[str, Any]]):
    """
    Display recommendation statistics in a visually appealing way

    Args:
        recommendations: List of recommendation dictionaries
    """
    if not recommendations:
        st.info("📊 No recommendations available for analysis")
        return

    st.markdown("### 📊 Recommendation Analytics")

    stats = calculate_recommendation_stats(recommendations)

    # Display metric cards
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        avg_score = stats.get('avg_score', 0)
        st.markdown(f'''
        <div class="metric-card">
            <h3>{avg_score:.1f}</h3>
            <p>Avg Score</p>
        </div>
        ''', unsafe_allow_html=True)

    with col2:
        most_common_genre = stats.get('most_common_genre', 'N/A')
        st.markdown(f'''
        <div class="metric-card">
            <h3>{most_common_genre}</h3>
            <p>Top Genre</p>
        </div>
        ''', unsafe_allow_html=True)

    with col3:
        avg_episodes = stats.get('avg_episodes', 0)
        st.markdown(f'''
        <div class="metric-card">
            <h3>{int(avg_episodes)}</h3>
            <p>Avg Episodes</p>
        </div>
        ''', unsafe_allow_html=True)

    with col4:
        most_common_year = stats.get('most_common_year', 'N/A')
        st.markdown(f'''
        <div class="metric-card">
            <h3>{most_common_year}</h3>
            <p>Popular Year</p>
        </div>
        ''', unsafe_allow_html=True)


def create_genre_distribution_chart(recommendations: List[Dict[str, Any]]):
    """
    Create a genre distribution chart

    Args:
        recommendations: List of recommendation dictionaries

    Returns:
        plotly.graph_objects.Figure: Genre distribution chart
    """
    # Get all genres
    all_genres = []
    for rec in recommendations:
        genres = rec.get('genres', [])
        if isinstance(genres, list):
            all_genres.extend(genres)

    if not all_genres:
        return None

    # Count genres and get top 10
    genre_counts = Counter(all_genres)
    top_genres = dict(genre_counts.most_common(10))

    # Create horizontal bar chart
    fig = px.bar(
        x=list(top_genres.values()),
        y=list(top_genres.keys()),
        orientation='h',
        title="Genre Distribution in Recommendations",
        color=list(top_genres.values()),
        color_continuous_scale="viridis"
    )

    fig.update_layout(
        height=400,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis_title="Count",
        yaxis_title="Genre"
    )

    return fig


def create_score_distribution_chart(recommendations: List[Dict[str, Any]]):
    """
    Create a score distribution chart

    Args:
        recommendations: List of recommendation dictionaries

    Returns:
        plotly.graph_objects.Figure: Score distribution chart
    """
    scores = [r.get('score', 0) for r in recommendations if r.get(
        'score') and r.get('score') > 0]

    if not scores:
        return None

    fig = px.histogram(
        x=scores,
        title="Score Distribution",
        nbins=20,
        color_discrete_sequence=['#667eea']
    )

    fig.update_layout(
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis_title="Score",
        yaxis_title="Count"
    )

    return fig


def create_year_distribution_chart(recommendations: List[Dict[str, Any]]):
    """
    Create a year distribution chart

    Args:
        recommendations: List of recommendation dictionaries

    Returns:
        plotly.graph_objects.Figure: Year distribution chart
    """
    years = [r.get('year') for r in recommendations if r.get('year')]

    if not years:
        return None

    year_counts = Counter(years)
    sorted_years = sorted(year_counts.items())

    fig = px.line(
        x=[str(year) for year, count in sorted_years],
        y=[count for year, count in sorted_years],
        title="Release Year Distribution",
        markers=True
    )

    fig.update_layout(
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis_title="Year",
        yaxis_title="Count"
    )

    return fig


def analyze_user_history(history: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Analyze user's recommendation history

    Args:
        history: List of history entries

    Returns:
        Dict: Analysis results
    """
    if not history:
        return {}

    # Convert to DataFrame for easier analysis
    df = pd.DataFrame(history)

    # Add datetime column
    df['datetime'] = pd.to_datetime(df['timestamp'], unit='s')
    df['date'] = df['datetime'].dt.date

    # Calculate statistics
    total_searches = len(df)
    avg_results = df['results'].mean()
    method_counts = df['method'].value_counts().to_dict()

    # Daily activity
    daily_activity = df.groupby('date').size().to_dict()

    # Most active day
    most_active_date = df['date'].value_counts(
    ).index[0] if not df.empty else None

    return {
        'total_searches': total_searches,
        'avg_results': avg_results,
        'method_distribution': method_counts,
        'daily_activity': daily_activity,
        'most_active_date': most_active_date,
        'date_range': {
            'start': df['date'].min() if not df.empty else None,
            'end': df['date'].max() if not df.empty else None
        }
    }


def create_history_charts(history: List[Dict[str, Any]]):
    """
    Create charts for user history analysis

    Args:
        history: List of history entries

    Returns:
        Tuple of plotly figures
    """
    if not history:
        return None, None

    analysis = analyze_user_history(history)

    # Method distribution pie chart
    method_dist = analysis.get('method_distribution', {})
    method_fig = px.pie(
        values=list(method_dist.values()),
        names=list(method_dist.keys()),
        title="Recommendation Methods Used"
    )
    method_fig.update_layout(height=400)

    # Daily activity line chart
    daily_activity = analysis.get('daily_activity', {})
    if daily_activity:
        dates = list(daily_activity.keys())
        counts = list(daily_activity.values())

        activity_fig = px.line(
            x=dates,
            y=counts,
            title="Search Activity Over Time",
            markers=True
        )
        activity_fig.update_layout(
            height=400,
            xaxis_title="Date",
            yaxis_title="Number of Searches"
        )
    else:
        activity_fig = None

    return method_fig, activity_fig
