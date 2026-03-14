import feedparser
import requests
import json
import os
import re
from datetime import datetime

WEBHOOK = "https://discord.com/api/webhooks/1481698681219453181/VxrFmjQS1k3MeF74b9Xm4eN4UJ8zScQFN7vhq-ye7lz1b0iPYDjm4PDWlL4-_0UjSfRG"

feeds = {
    "Cricbuzz": "https://www.cricbuzz.com/rss/news.xml",
    "ICC": "https://www.icc-cricket.com/rss"
}

CACHE_FILE = "posted.json"

# Load cache
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "r") as f:
        posted = json.load(f)
else:
    posted = []

new_links = []

def get_image(entry):
    if "media_content" in entry:
        return entry.media_content[0]["url"]

    if "media_thumbnail" in entry:
        return entry.media_thumbnail[0]["url"]

    if "image" in entry:
        return entry.image["href"]

    return None

def get_og_image(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        html = requests.get(url, headers=headers, timeout=10).text

        match = re.search(r'<meta property="og:image" content="([^"]+)"', html)

        if match:
            return match.group(1)

    except:
        pass

    return None


for source, url in feeds.items():

    print(f"Checking feed: {source}")

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)

        feed = feedparser.parse(response.content)

    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        continue

    print(f"{source} entries found:", len(feed.entries))

    for entry in feed.entries[:5]:

        print("Checking article:", entry.title)

        if entry.link in posted:
            print("Skipping duplicate")
            continue

        image = get_image(entry)

        if not image:
            image = get_og_image(entry.link)

        description = entry.get("summary", "No description available.")
        description = description.replace("<p>", "").replace("</p>", "")
        description = description[:200]

        embed = {
            "title": entry.title,
            "url": entry.link,
            "description": description,
            "color": 15548997,
            "footer": {
                "text": f"Source: {source}"
            },
            "timestamp": datetime.utcnow().isoformat()
        }

        if image:
            embed["image"] = {"url": image}

        payload = {
            "embeds": [embed]
        }

        try:
            response = requests.post(WEBHOOK, json=payload)
            print("Posting:", entry.title)
            print("Webhook status:", response.status_code)

            if response.status_code == 204:
                new_links.append(entry.link)

        except Exception as e:
            print("Webhook error:", e)


posted.extend(new_links)

with open(CACHE_FILE, "w") as f:
    json.dump(posted, f)

print("Script finished.")
