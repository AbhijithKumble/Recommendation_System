import pandas as pd
from typing import List, Dict, Any, Union
from recommender.content_based import get_recommendations as content_recommend
from recommender.collaborative import get_recommendations as collab_recommend


def normalize_recommendations(recommendations: Union[List, pd.DataFrame]) -> List[Dict[str, Any]]:
    """
    Normalize recommendations from different sources to a consistent format

    Args:
        recommendations: Either a list of dicts (content-based) or DataFrame (collaborative)

    Returns:
        List[Dict]: Normalized list of recommendation dictionaries
    """
    if isinstance(recommendations, pd.DataFrame):
        # Convert DataFrame to list of dictionaries
        return recommendations.to_dict('records')
    elif isinstance(recommendations, list):
        # Already in the correct format
        return recommendations
    else:
        # Handle other formats or return empty list
        return []


def get_content_based_recommendations(anime_input: Any, content_models: Any, n_recommendations: int = 10) -> List[Dict[str, Any]]:
    """
    Get content-based recommendations and normalize the output

    Args:
        anime_input: Input for recommendations (ID, title, etc.)
        content_models: Content-based models
        n_recommendations: Number of recommendations to return

    Returns:
        List[Dict]: Normalized recommendations
    """
    try:
        raw_recommendations = content_recommend(
            anime_input, content_models, n_recommendations)
        return normalize_recommendations(raw_recommendations)
    except Exception as e:
        print(f"Error getting content-based recommendations: {e}")
        return []


def get_collaborative_recommendations(anime_input: any, collab_models: Any, n_recommendations: int = 10) -> List[Dict[str, Any]]:
    """
    Get collaborative filtering recommendations and normalize the output

    Args:
        anime_input: Input for recommendations (ID, title, etc.)
        collab_models: Collaborative filtering models
        n_recommendations: Number of recommendations to return

    Returns:
        List[Dict]: Normalized recommendations
    """
    try:
        raw_recommendations = collab_recommend(
            anime_input, collab_models, n_recommendations)
        return normalize_recommendations(raw_recommendations)
    except Exception as e:
        print(f"Error getting collaborative recommendations: {e}")
        return []


def get_hybrid_recommendations(anime_input: Any, content_models: Any, collab_models: Any, n_recommendations: int = 10) -> List[Dict[str, Any]]:
    """
    Get hybrid recommendations by combining content-based and collaborative filtering

    Args:
        anime_input: Input for recommendations
        content_models: Content-based models
        collab_models: Collaborative filtering models
        n_recommendations: Total number of recommendations to return

    Returns:
        List[Dict]: Combined and normalized recommendations
    """
    try:
        # Split recommendations between methods
        content_count = n_recommendations // 2
        collab_count = n_recommendations - content_count

        # Get recommendations from both methods
        content_recs = get_content_based_recommendations(
            anime_input, content_models, content_count)
        collab_recs = get_collaborative_recommendations(
            anime_input, collab_models, collab_count)

        # Combine recommendations
        combined_recs = content_recs + collab_recs

        # Remove duplicates based on title or ID
        seen_titles = set()
        unique_recs = []

        for rec in combined_recs:
            title = rec.get('title', '')
            anime_id = rec.get('id', '')
            identifier = title or str(anime_id)

            if identifier and identifier not in seen_titles:
                seen_titles.add(identifier)
                unique_recs.append(rec)

        return unique_recs[:n_recommendations]

    except Exception as e:
        print(f"Error getting hybrid recommendations: {e}")
        return []


def apply_filters(recommendations: List[Dict[str, Any]], preferences: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Apply user filters to recommendations

    Args:
        recommendations: List of recommendation dictionaries
        preferences: User preferences including filters

    Returns:
        List[Dict]: Filtered recommendations
    """
    filtered_recs = []

    for rec in recommendations:
        # Score filter
        score = rec.get('score', 0)
        if score and score < preferences.get('min_score', 0):
            continue

        # Episodes filter
        episodes = rec.get('episodes', 0)
        if episodes:
            if (episodes < preferences.get('min_episodes', 0) or
                    episodes > preferences.get('max_episodes', float('inf'))):
                continue

        # Genre filter
        preferred_genres = preferences.get('preferred_genres', [])
        if preferred_genres:
            rec_genres = rec.get('genres', [])
            if not any(genre in rec_genres for genre in preferred_genres):
                continue

        filtered_recs.append(rec)

    return filtered_recs


def get_recommendations_by_method(method: str, anime_input: Any, content_models: Any, collab_models: Any, n_recommendations: int = 10) -> List[Dict[str, Any]]:
    """
    Get recommendations based on the specified method

    Args:
        method: Recommendation method ('Content-Based', 'Collaborative Filtering', 'Hybrid (Best)')
        anime_input: Input for recommendations
        content_models: Content-based models
        collab_models: Collaborative filtering models
        n_recommendations: Number of recommendations

    Returns:
        List[Dict]: Recommendations based on the specified method
    """
    if method == "Content-Based":
        return get_content_based_recommendations(anime_input, content_models, n_recommendations)
    elif method == "Collaborative Filtering":
        return get_collaborative_recommendations(anime_input, collab_models, n_recommendations)
    else:  # Hybrid (Best)
        return get_hybrid_recommendations(anime_input, content_models, collab_models, n_recommendations)
