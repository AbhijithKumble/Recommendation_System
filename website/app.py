import streamlit as st
import pickle
import requests

st.set_page_config(page_title="Anime Recommender", layout="wide")

# 🌸 Styled Header
st.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <h1 style="color: #ff66b2; font-size: 3em; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
            🌸 Anime Recommender
        </h1>
        <p style="font-size: 1.2em; color: #666;">
            Find anime recommendations based on your favorite shows.
        </p>
    </div>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    with open("./models/animes.pkl", "rb") as f:
        anime_df = pickle.load(f)
    with open("./models/top_5_similar.pkl", "rb") as f:
        top_5_similar = pickle.load(f)
    return anime_df, top_5_similar


@st.cache_data(show_spinner=False)
def fetch_anime_details_by_id(mal_id):
    try:
        response = requests.get(f"https://api.jikan.moe/v4/anime/{mal_id}")
        if response.status_code == 200:
            return response.json().get("data", {})
    except Exception as e:
        st.error(f"Error fetching details: {e}")
    return {}


anime_df, top_5_similar = load_data()
anime_titles = anime_df["title"].values

# 🎯 Styled Anime Selector
st.markdown("""
    <style>
        .stSelectbox>div>div {
            font-size: 1.1em;
        }
        .stButton>button {
            background-color: #ff66b2;
            color: white;
            padding: 0.5em 1.2em;
            border-radius: 8px;
            font-weight: bold;
            margin-top: 0.5em;
        }
        .stButton>button:hover {
            background-color: #ff85c1;
        }
    </style>
""", unsafe_allow_html=True)

selected_anime = st.selectbox("🎥 Select an anime:", anime_titles)

if st.button("🔍 Show Recommendations"):
    recommendations = top_5_similar.get(selected_anime, [])

    if not recommendations:
        st.warning("No recommendations found for the selected anime.")
    else:
        st.subheader(f"🎯 Animes similar to **{selected_anime}**:")
        for rec in recommendations:
            anime_row = anime_df[anime_df["title"] == rec["title"]]
            if anime_row.empty:
                continue
            row = anime_row.iloc[0]
            mal_id = row.get("anime_id")

            if not mal_id:
                st.warning(f"No MAL ID found for {rec['title']}")
                continue

            anime = fetch_anime_details_by_id(mal_id)
            if not anime:
                continue

            with st.container():
                st.markdown(
                    f"  # [{anime.get('title_english') or anime['title']}]({anime['url']})")
                cols = st.columns([1, 2])
                with cols[0]:
                    st.image(anime["images"]["jpg"]
                             ["large_image_url"], width=220)
                with cols[1]:
                    score = anime.get("score")
                    stars = "⭐" * int(round(score / 2)) if score else "N/A"
                    st.markdown(f"**Score:** {score} {stars}")
                    synopsis = anime.get("synopsis", "No synopsis available.")
                    st.markdown(f"**Synopsis:** {synopsis}")

                    trailer = anime.get("trailer", {}).get("embed_url")
                    if trailer:
                        st.video(trailer)

                st.markdown("---")
                st.markdown("---")

                st.markdown("---")
