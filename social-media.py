import argparse
import json
import sylvia.render
import sylvia.diff

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

# Time for character management :-) You're probably not paying for Twitter (X?) Blue
medium = "twitter"
TWEET_LENGTH = 280
LINK_LENGTH = 23 + 1 # as per https://developer.twitter.com/en/docs/counting-characters

for event in rss_rich:
    if not "change" in event:
        continue

    body_text = ""
    if event["change"] == "added":
        body_text = f"🆕 New event! "
    elif event["change"] == "changed":
        if "date" in event["changes"]:
            body_text = f"📅⚠️ Date change! "
        elif "time" in event["changes"]:
            body_text = f"⏰⚠️ Time change! "
        else:
            # Other changes do not matter
            continue

    chars_left = TWEET_LENGTH - len(body_text)
    event_title = event["title"]

    # We only truncate if the social medium is Twitter
    if chars_left < len(event["title"]) and medium == "twitter":
        print("Big problems!", event["title"])
        # We truncate the title to the number of chars left, minus one for the …
        event_title = event["title"][:chars_left - 1] + "…"

    body_text = f"{body_text}{event_title} {event['link']}"

    print(body_text)