import streamlit as st
import pickle

st.set_page_config(page_title="Anime Recommender", layout="wide")
st.title("🌸 Anime Recommender")


@st.cache_data
def load_data():
    with open("./models/animes.pkl", "rb") as f:
        anime_df = pickle.load(f)
    with open("./models/top_5_similar.pkl", "rb") as f:
        top_5_similar = pickle.load(f)
    return anime_df, top_5_similar


anime_df, top_5_similar = load_data()

anime_titles = anime_df["title"].values

# Select anime
selected_anime = st.selectbox("Select an anime:", anime_titles)

if st.button("Show Recommendations"):
    recommendations = top_5_similar.get(selected_anime, [])

    if not recommendations:
        st.warning("No recommendations found for the selected anime.")
    else:
        st.subheader(f"Animes similar to **{selected_anime}**:")
        cols = st.columns(len(recommendations))

        for col, rec in zip(cols, recommendations):
            anime_row = anime_df[anime_df["title"] == rec["title"]]
            if not anime_row.empty:
                row = anime_row.iloc[0]
                if "image_url" in row and isinstance(row["image_url"], str):
                    col.image(row["image_url"], use_column_width=True)
                col.markdown(f"### {row['title']}")
