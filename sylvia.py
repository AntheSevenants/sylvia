import argparse
import json
import sylvia.render
import sylvia.diff
import feedparser

parser = argparse.ArgumentParser(
    description="sylvia - generate RSS-based event calendars"
)
parser.add_argument(
    "rss_path", type=str, help="Path to the RSS feed the calendar should be based on"
)
parser.add_argument("cache_old", type=str, help="Path to the old cache file")

args = parser.parse_args()

# Open the old cache
with open(args.cache_old, "rt") as reader:
    cache_old = json.loads(reader.read())

# Retrieve the RSS feed
rss = feedparser.parse(args.rss_path)
rss = rss["entries"]
# Turn it into "new" cache
cache_new = sylvia.diff.get_cache(rss)

# Diff the changed events
changed_events = sylvia.diff.get_updates(cache_old, cache_new)

# Join the changed events output with the RSS output
rss = sylvia.diff.join(rss, changed_events)

print(sylvia.render.calendar(rss))
