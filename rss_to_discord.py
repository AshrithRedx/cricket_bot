import feedparser
import requests
import json
import os
from datetime import datetime

WEBHOOK = "https://discord.com/api/webhooks/1481698681219453181/VxrFmjQS1k3MeF74b9Xm4eN4UJ8zScQFN7vhq-ye7lz1b0iPYDjm4PDWlL4-_0UjSfRG"

feeds = {
    "Cricbuzz": "https://www.cricbuzz.com/rss/news.xml",
    "BCCI": "https://www.bcci.tv/feeds/news",
    "IPL": "https://www.iplt20.com/rss/news"
}

CACHE_FILE = "posted.json"

if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "r") as f:
        posted = json.load(f)
else:
    posted = []

new_links = []

for source, url in feeds.items():
    feed = feedparser.parse(url)

    for entry in feed.entries[:5]:

        if entry.link in posted:
            continue

        image = None

        if "media_content" in entry:
            image = entry.media_content[0]["url"]

        embed = {
            "title": entry.title,
            "url": entry.link,
            "description": entry.get("summary", "")[:200] + "...",
            "color": 16753920,
            "footer": {
                "text": source
            },
            "timestamp": datetime.utcnow().isoformat()
        }

        if image:
            embed["image"] = {"url": image}

        payload = {
            "embeds": [embed]
        }

        requests.post(WEBHOOK, json=payload)

        new_links.append(entry.link)

posted.extend(new_links)

with open(CACHE_FILE, "w") as f:
    json.dump(posted, f)
