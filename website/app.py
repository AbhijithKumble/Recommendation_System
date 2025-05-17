import streamlit as st
import pickle

st.set_page_config(page_title="Anime Recommender", layout="wide")
st.title("🌸 Anime Recommender with Similarity Matrix")


@st.cache_data
def load_data():
    with open("./models/animes.pkl", "rb") as f:
        anime_df = pickle.load(f)
    with open("./models/similarity_matrix.pkl", "rb") as f:
        similarity = pickle.load(f)
    return anime_df, similarity


anime_df, similarity = load_data()

# For convenience: list of anime titles
anime_titles = anime_df["title"].values


def recommend_anime(title, anime_df, similarity, top_n=5):
    # Find index of selected anime
    idx = anime_df[anime_df["title"] == title].index[0]

    # Get similarity scores for this anime to all others
    sim_scores = list(enumerate(similarity[idx]))

    # Sort by similarity score descending, exclude itself (idx)
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Take top_n + 1 because first one is itself
    sim_scores = sim_scores[1: top_n + 1]

    # Get anime indices of recommendations
    anime_indices = [i[0] for i in sim_scores]

    # Return recommended anime info
    return anime_df.iloc[anime_indices]


# Select anime
selected_anime = st.selectbox("Select an anime:", anime_titles)

if st.button("Show Recommendations"):
    recommendations = recommend_anime(selected_anime, anime_df, similarity)

    st.subheader(f"Animes similar to **{selected_anime}**:")
    cols = st.columns(len(recommendations))

    for col, (_, row) in zip(cols, recommendations.iterrows()):
        if "image_url" in row:
            col.image(row["image_url"], use_column_width=True)
        col.markdown(f"### {row['title']}")
