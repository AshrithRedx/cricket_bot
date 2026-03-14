import feedparser
import requests
import json
import os
from datetime import datetime

WEBHOOK = "https://discord.com/api/webhooks/1481698681219453181/VxrFmjQS1k3MeF74b9Xm4eN4UJ8zScQFN7vhq-ye7lz1b0iPYDjm4PDWlL4-_0UjSfRG"
feeds = {
    "Cricbuzz": "https://www.cricbuzz.com/rss/news.xml",
    "ICC": "https://www.icc-cricket.com/rss"
}


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

for source, url in feeds.items():

    try:
        feed = feedparser.parse(url)
    except:
        continue

    for entry in feed.entries[:5]:

        if entry.link in posted:
            continue

        image = get_image(entry)

        description = entry.get("summary", "")
        description = description.replace("<p>", "").replace("</p>", "")
        description = description[:200] + "..."

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

        requests.post(WEBHOOK, json=payload)

        new_links.append(entry.link)

posted.extend(new_links)

with open(CACHE_FILE, "w") as f:
    json.dump(posted, f)
