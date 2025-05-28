import pickle


def load_content_based_models():
    with open("./models/content_based_animes.pkl", "rb") as f1, \
            open("./models/top_5_similar_content_based.pkl", "rb") as f2:
        anime_df = pickle.load(f1)
        top_sim = pickle.load(f2)
    return anime_df, top_sim


def get_recommendations(title, top_sim_dict, top_n=5):
    """
    Return top N similar anime titles using content-based filtering.
    """
    return top_sim_dict.get(title, [])[:top_n]
