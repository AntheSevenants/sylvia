import argparse
import json
import sylvia.render
import sylvia.diff
import sylvia.socials

parser = argparse.ArgumentParser(
    description="social media for sylvia - automatic posts on social media"
)
parser.add_argument("cache_old", type=str, help="Path to the old cache file")

args = parser.parse_args()

# Load the old cache
cache_old = sylvia.diff.get_cache_from_path_full(args.cache_old)

# Retrieve the current RSS feed
rss, cache_new = sylvia.diff.get_rss_new()

# Diff the changed events
changed_events = sylvia.diff.get_updates(cache_old, cache_new)

# Enrich RSS entries with changes
rss_rich = sylvia.diff.join(rss, changed_events)

posts = sylvia.socials.compose(rss_rich)

print(posts)