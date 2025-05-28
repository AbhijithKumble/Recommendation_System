import streamlit as st
from recommender.content_based import load_content_based_models
from recommender.collaborative import load_collaborative_models


@st.cache_data
def load_models():
    """
    Load both recommendation models with caching
    Returns:
        tuple: (content_models, collab_models)
    """
    try:
        content_models = load_content_based_models()
        collab_models = load_collaborative_models()
        return content_models, collab_models
    except Exception as e:
        st.error(f"Error loading models: {str(e)}")
        return None, None


def get_content_models():
    """Get content-based models from session state"""
    return st.session_state.get('content_models', None)


def get_collab_models():
    """Get collaborative filtering models from session state"""
    return st.session_state.get('collab_models', None)


def models_loaded():
    """Check if both models are loaded"""
    return (st.session_state.get('content_models') is not None and
            st.session_state.get('collab_models') is not None)
