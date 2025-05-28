
import streamlit as st
import pandas as pd
import pickle
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="Sakura Anime Recommendation System", layout="wide")
st.title("🌸 Sakura Anime Recommendation System")

# Load anime data and similarity matrices
@st.cache_data
def load_data():
    anime_df = pd.read_csv("anime_data.csv")  # columns: anime_id, title, genres, synopsis, image_url
    with open("content_sim.pkl", "rb") as f:
        content_sim = pickle.load(f)
    with open("collab_sim.pkl", "rb") as f:
        collab_sim = pickle.load(f)
    return anime_df, content_sim, collab_sim

anime_df, content_sim, collab_sim = load_data()

# Simulated user profile
st.sidebar.header("👤 User Preferences")
user_likes = st.sidebar.multiselect("Select anime you like:", anime_df['title'].values)

# Recommendation mode switching
use_collab = False
if len(user_likes) >= 3:
    use_collab = st.sidebar.checkbox("Use Collaborative Filtering", value=True)

st.subheader("🎯 Recommended Anime")

def recommend_content(user_likes):
    indices = anime_df[anime_df['title'].isin(user_likes)].index
    sim_scores = content_sim[indices].mean(axis=0)
    sim_indices = sim_scores.argsort()[::-1][:10]
    return anime_df.iloc[sim_indices]

def recommend_collab(user_likes):
    indices = anime_df[anime_df['title'].isin(user_likes)].index
    sim_scores = collab_sim[indices].mean(axis=0)
    sim_indices = sim_scores.argsort()[::-1][:10]
    return anime_df.iloc[sim_indices]

if user_likes:
    if use_collab:
        recs = recommend_collab(user_likes)
        st.write("Using Collaborative Filtering")
    else:
        recs = recommend_content(user_likes)
        st.write("Using Content-Based Filtering")

    for _, row in recs.iterrows():
        st.markdown(f"### {row['title']}")
        st.image(row['image_url'], width=150)
        st.write(row['synopsis'])
        st.markdown("---")
else:
    st.info("Select some anime from the sidebar to get recommendations.")

