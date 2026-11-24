import os
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

CHECKPOINT_FILE = "checkpoint.txt"
OUTPUT_FILE = "all_users_animelist.csv"


def scroll_to_bottom(driver, pause_time=1.5, max_attempts=50):
    last_height = driver.execute_script("return document.body.scrollHeight")
    for _ in range(max_attempts):
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def scrape_mal_animelist(username, driver):
    url = f"https://myanimelist.net/animelist/{username}?status=7"
    driver.get(url)
    time.sleep(2)
    scroll_to_bottom(driver)

    rows = driver.find_elements(By.CSS_SELECTOR, "tbody.list-item")
    anime_list = []

    for row in rows:
        try:
            title_tag = row.find_element(
                By.CSS_SELECTOR, 'td.title a.link.sort')
            anime_title = title_tag.text.strip()
            anime_url = title_tag.get_attribute('href')
            anime_id = anime_url.split("/")[4]

            score = row.find_element(
                By.CSS_SELECTOR, 'td.score span').text.strip()
            score = score if score else "N/A"

            progress = row.find_element(
                By.CSS_SELECTOR, 'td.progress').text.strip().replace('\n', ' ')

            status_classes = row.find_element(
                By.CSS_SELECTOR, 'td.status').get_attribute('class').split()
            status = [cls for cls in status_classes if cls not in [
                'data', 'status']][0]

            anime_list.append({
                "username": username,
                "anime_title": anime_title,
                "anime_id": anime_id,
                "progress": progress,
                "score": score,
                "status": status
            })
        except Exception as e:
            print(f"[{username}] Skipping a row due to error: {e}")
            continue

    return anime_list


def read_checkpoint():
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE, "r") as f:
            return f.read().strip()
    return ""


def write_checkpoint(username):
    with open(CHECKPOINT_FILE, "w") as f:
        f.write(username)


def main():
    df_users = pd.read_csv(
        "/home/abhi/work/Recommendation_System/data_zip/user_data.csv")
    usernames = df_users["Username"].dropna().unique()

    last_processed = read_checkpoint()
    checkpoint_found = (last_processed == "")

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--blink-settings=imagesEnabled=false")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")

    prefs = {
        "profile.managed_default_content_settings.images": 2,
        "profile.managed_default_content_settings.stylesheets": 2,
        "profile.managed_default_content_settings.fonts": 2,
        "profile.managed_default_content_settings.plugins": 2
    }
    chrome_options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(service=Service(), options=chrome_options)

    for username in usernames:
        if not checkpoint_found:
            if username == last_processed:
                checkpoint_found = True
            else:
                print(f"⏭️ Skipping {username}")
                continue

        print(f"🔍 Scraping: {username}")
        try:
            user_data = scrape_mal_animelist(username, driver)
            if user_data:
                df = pd.DataFrame(user_data)
                df.to_csv(OUTPUT_FILE, mode='a', index=False,
                          header=not os.path.exists(OUTPUT_FILE))
                write_checkpoint(username)
        except Exception as e:
            print(f"❌ Failed to scrape {username}: {e}")
            continue

    driver.quit()
    print("✅ Done. Output saved to", OUTPUT_FILE)


if __name__ == "__main__":
    main()
