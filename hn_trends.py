import json
import os
from datetime import datetime

import requests


TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"
HEADERS = {"User-Agent": "TrendPulse/1.0"}
MAX_STORIES_TO_SCAN = 200
MAX_PER_CATEGORY = 20
REQUEST_TIMEOUT_SECONDS = 10

categories = {
    "technology": [
        "ai",
        "software",
        "tech",
        "code",
        "computer",
        "data",
        "cloud",
        "api",
        "gpu",
        "llm",
    ],
    "worldnews": [
        "war",
        "government",
        "country",
        "president",
        "election",
        "climate",
        "attack",
        "global",
    ],
    "sports": [
        "nfl",
        "nba",
        "fifa",
        "sport",
        "game",
        "team",
        "player",
        "league",
        "championship",
    ],
    "science": [
        "research",
        "study",
        "space",
        "physics",
        "biology",
        "discovery",
        "nasa",
        "genome",
    ],
    "entertainment": [
        "movie",
        "film",
        "music",
        "netflix",
        "game",
        "book",
        "show",
        "award",
        "streaming",
    ],
}


def get_category(title):
    lowered_title = title.lower()
    for category, keywords in categories.items():
        if any(keyword in lowered_title for keyword in keywords):
            return category
    return None


def fetch_json(session, url):
    response = session.get(url, timeout=REQUEST_TIMEOUT_SECONDS)
    response.raise_for_status()
    return response.json()


def collect_trends():
    print("Script started...")

    results = []
    category_count = {key: 0 for key in categories}
    collected_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with requests.Session() as session:
        session.headers.update(HEADERS)

        try:
            story_ids = fetch_json(session, TOP_STORIES_URL)
            print(f"Fetched story IDs: {len(story_ids)}")
        except requests.RequestException as exc:
            print(f"Error fetching top stories: {exc}")
            story_ids = []

        for story_id in story_ids[:MAX_STORIES_TO_SCAN]:
            try:
                data = fetch_json(session, ITEM_URL.format(story_id))
            except requests.RequestException as exc:
                print(f"Error fetching story {story_id}: {exc}")
                continue

            title = data.get("title")
            if not title:
                continue

            category = get_category(title)
            if not category or category_count[category] >= MAX_PER_CATEGORY:
                continue

            story = {
                "post_id": data.get("id"),
                "title": title,
                "category": category,
                "score": data.get("score", 0),
                "num_comments": data.get("descendants", 0),
                "author": data.get("by"),
                "collected_at": collected_at,
            }

            results.append(story)
            category_count[category] += 1

    os.makedirs("data", exist_ok=True)
    filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

    with open(filename, "w", encoding="utf-8") as file_obj:
        json.dump(results, file_obj, indent=4, ensure_ascii=False)

    print(f"Collected stories: {len(results)}")
    print(f"Saved to: {filename}")
    print("Script finished.")


if __name__ == "__main__":
    collect_trends()
