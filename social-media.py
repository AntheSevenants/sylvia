import os
import argparse
import json
import tweepy
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

# We compose the different posts from the rich RSS object
posts = sylvia.socials.compose(rss_rich)

# Get authentication for Twitter ready
api = tweepy.Client(bearer_token=os.environ["TW_BEARER_TOKEN"],
                    consumer_key=os.environ["TW_CONSUMER_KEY"],
                    consumer_secret=os.environ["TW_CONSUMER_SECRET"],
                    access_token=os.environ["TW_ACCESS_TOKEN"],
                    access_token_secret=os.environ["TW_ACCESS_TOKEN_SECRET"])

# For each composed post, send a tweet into the world
for post in posts:
    print("Sending tweet:", post)
    api.create_tweet(text=post)