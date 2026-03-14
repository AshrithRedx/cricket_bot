import feedparser
import requests

WEBHOOK_URL = "https://discord.com/api/webhooks/1481698681219453181/VxrFmjQS1k3MeF74b9Xm4eN4UJ8zScQFN7vhq-ye7lz1b0iPYDjm4PDWlL4-_0UjSfRG"

feeds = [
    "https://www.cricbuzz.com/rss/news.xml",
    "https://www.espncricinfo.com/rss/content/story/feeds/0.xml"
]

for feed_url in feeds:
    feed = feedparser.parse(feed_url)

    for entry in feed.entries[:3]:
        message = {
            "content": f"📰 {entry.title}\n{entry.link}"
        }

        requests.post(WEBHOOK_URL, json=message)
