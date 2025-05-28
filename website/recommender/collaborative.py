import pickle


def load_collaborative_models():
    with open("./models/collab_filt_df_v2.0.pkl", "rb") as f1, \
            open("./models/collab_filt_top_10_sim_v2.0.pkl", "rb") as f2:
        anime_df = pickle.load(f1)
        top_sim_dict = pickle.load(f2)
    return anime_df, top_sim_dict


def get_recommendations(title, anime_df, top_sim_dict, top_n=5):
    """
    Return top N similar anime titles using collaborative filtering.
    """
    row = anime_df[anime_df["title"] == title]
    if row.empty:
        return []

    anime_id = row.iloc[0]["anime_id"]
    if anime_id not in top_sim_dict:
        return []

    similar_ids = top_sim_dict[anime_id][:top_n]
    similar_id_list = [sid for sid, _ in similar_ids]
    recommended = anime_df[anime_df["anime_id"].isin(similar_id_list)]
    return recommended["title"].tolist()
