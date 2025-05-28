import requests


def fetch_anime_details_by_id(mal_id):
    try:
        response = requests.get(
            f"https://api.jikan.moe/v4/anime/{mal_id}/full")
        if response.status_code == 200:
            return response.json().get("data", None)
        return None
    except Exception as e:
        print(f"Error fetching details: {e}")
        return None
