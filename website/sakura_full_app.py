
import streamlit as st
import pandas as pd
import pickle
import os
import json
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="Sakura Anime Recommendation System", layout="wide")

st.title("🌸 Sakura Anime Recommendation System")

# ----------- User Authentication -----------
USER_DB = "user_db.json"

def load_user_db():
    if os.path.exists(USER_DB):
        with open(USER_DB, "r") as f:
            return json.load(f)
    return {}

def save_user_db(user_db):
    with open(USER_DB, "w") as f:
        json.dump(user_db, f)

user_db = load_user_db()

# ----------- Login or Register -----------
auth_mode = st.sidebar.selectbox("Choose Mode", ["Login", "Register"])

if auth_mode == "Register":
    new_user = st.sidebar.text_input("Username")
    new_pass = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Register"):
        if new_user in user_db:
            st.sidebar.error("User already exists!")
        else:
            user_db[new_user] = {"password": new_pass, "likes": []}
            save_user_db(user_db)
            st.sidebar.success("User registered. Please login.")

if auth_mode == "Login":
    user = st.sidebar.text_input("Username")
    passwd = st.sidebar.text_input("Password", type="password")
    login_button = st.sidebar.button("Login")

    if login_button:
        if user in user_db and user_db[user]["password"] == passwd:
            st.session_state["logged_in"] = True
            st.session_state["user"] = user
        else:
            st.sidebar.error("Invalid username or password.")

if not st.session_state.get("logged_in", False):
    st.warning("Please login to use the recommendation system.")
    st.stop()

username = st.session_state["user"]
st.sidebar.success(f"Logged in as: {username}")

# ----------- Load Anime Data and Similarities -----------
@st.cache_data
def load_data():
    anime_df = pd.read_csv("anime_data.csv")  # must have title, synopsis, image_url
    with open("content_sim.pkl", "rb") as f:
        content_sim = pickle.load(f)
    with open("collab_sim.pkl", "rb") as f:
        collab_sim = pickle.load(f)
    return anime_df, content_sim, collab_sim

anime_df, content_sim, collab_sim = load_data()

# ----------- Anime Liking System -----------
st.sidebar.header("❤️ Like Anime")
like_title = st.sidebar.selectbox("Choose anime to like:", anime_df["title"].values)
if st.sidebar.button("Like"):
    if like_title not in user_db[username]["likes"]:
        user_db[username]["likes"].append(like_title)
        save_user_db(user_db)
        st.sidebar.success(f"Added {like_title} to your favorites.")
    else:
        st.sidebar.info("Already liked.")

user_likes = user_db[username]["likes"]
st.sidebar.write("Your Favorites:")
st.sidebar.write(user_likes)

# ----------- Recommendation Logic -----------
def recommend_content(user_likes):
    indices = anime_df[anime_df["title"].isin(user_likes)].index
    sim_scores = content_sim[indices].mean(axis=0)
    sim_indices = sim_scores.argsort()[::-1][:10]
    return anime_df.iloc[sim_indices]

def recommend_collab(user_likes):
    indices = anime_df[anime_df["title"].isin(user_likes)].index
    sim_scores = collab_sim[indices].mean(axis=0)
    sim_indices = sim_scores.argsort()[::-1][:10]
    return anime_df.iloc[sim_indices]

st.subheader("🎯 Recommended Anime")

if len(user_likes) == 0:
    st.info("Like a few anime from the sidebar to get recommendations.")
else:
    use_collab = False
    if len(user_likes) >= 3:
        use_collab = st.radio("Select recommendation method", ["Content-Based", "Collaborative Filtering"]) == "Collaborative Filtering"
    if use_collab:
        st.write("Using Collaborative Filtering")
        recs = recommend_collab(user_likes)
    else:
        st.write("Using Content-Based Filtering")
        recs = recommend_content(user_likes)

    for _, row in recs.iterrows():
        st.markdown(f"### {row['title']}")
        st.image(row['image_url'], width=150)
        st.write(row['synopsis'])
        st.markdown("---")
