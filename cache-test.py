import feedparser
import json
from sylvia.render import print_date_time

rss = feedparser.parse("https://www.arts.kuleuven.be/ling/events/events/rss")["entries"]

with open("test.json", "wt") as writer:
    writer.write(json.dumps(rss))

cache = {}

for entry in rss:
    key = entry["link"]
    date_time = print_date_time(entry["updated"])
    description = entry["description"]

    cache[key] = {
        "date_time": date_time,
        "description": description
    }

with open("cache.json", "wt") as writer:
    writer.write(json.dumps(cache))