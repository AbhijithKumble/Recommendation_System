from ui.styles import load_custom_css
import streamlit as st
import time
from ui.components import display_header, display_sidebar, display_footer
from ui.tabs import recommendations_tab, search_tab, analytics_tab, history_tab
from utils.model_loader import load_models
from config.settings import PAGE_CONFIG

# Page configuration
st.set_page_config(**PAGE_CONFIG)

# Load custom CSS
load_custom_css()

# Initialize session state


def initialize_session_state():
    """Initialize session state variables"""
    if 'content_models' not in st.session_state:
        st.session_state.content_models = None
    if 'collab_models' not in st.session_state:
        st.session_state.collab_models = None
    if 'recommendation_history' not in st.session_state:
        st.session_state.recommendation_history = []


def main():
    # Initialize session state
    initialize_session_state()

    # Display header
    display_header()

    # Load models
    with st.spinner("🔮 Loading AI models..."):
        content_models, collab_models = load_models()

    if content_models is None or collab_models is None:
        st.error(
            "❌ Failed to load recommendation models. Please check your model files.")
        return

    # Store models in session state
    st.session_state.content_models = content_models
    st.session_state.collab_models = collab_models

    # Sidebar for user input
    preferences = display_sidebar()

    # Main content area with tabs
    tab1, tab2, tab3, tab4 = st.tabs(
        ["🎯 Get Recommendations", "🔍 Search Anime", "📊 Analytics", "📝 History"])

    with tab1:
        recommendations_tab(preferences)

    with tab2:
        search_tab()

    with tab3:
        analytics_tab()

    with tab4:
        history_tab()

    # Display footer
    display_footer()


if __name__ == "__main__":
    main()
