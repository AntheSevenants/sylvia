import os
import json
import pytz
import feedparser
import sylvia.render
import sylvia.helpers

from datetime import datetime
from glob import glob
from pathlib import Path

brussels = pytz.timezone("Europe/Brussels")

def get_cache_files(cache_path: str):
    """Get a list of all available cache files in a given directory

    Args:
        cache_path (str): the path where all cache files are stored

    Returns:
        list[str]: a list of all available JSON cache files (stems)
    """

    stems = [ Path(cache_file).stem for cache_file in glob(f"{cache_path}/*.json") ]
    stems.sort(reverse=True)

    return stems

def get_cache_from_path(cache_file: str):
    if cache_file == "none":
        cache_old = None
    else:
        cache_file = f"{cache_file}.json"
        cache_dir = os.environ['CACHE_DIR']
        cache_path = f"{cache_dir}/{cache_file}"

        if not os.path.exists(cache_path):
            return sylvia.error.generate("Invalid cache file.")
    
        # Open the old cache
        with open(cache_path, "rt") as reader:
            cache_old = json.loads(reader.read())

    return cache_old

def get_cache(rss: dict):
    """Generate cache dict from RSS entries

    Args:
        rss (dict): RSS output

    Returns:
        cache (dict): the cache for RSS
    """

    cache = {}

    for entry in rss:
        key = entry["link"]

        cache[key] = {
            "title": entry["title"],
            "date_time": sylvia.render.print_date_time(entry["updated"]),
            "date": sylvia.render.print_date(entry["updated"]),
            "time": sylvia.render.print_time(entry["updated"]),
            "description": entry["description"]
        }

    return cache

def get_rss_new():
    """Get the current RSS feed XML as a cache dict

    Returns:
        dict: the current RSS state
        dict: the cache for current RSS state
    """

    # Retrieve the RSS feed
    rss = feedparser.parse(os.environ["RSS_URL"])
    rss = rss["entries"]
    # Turn it into "new" cache
    cache_new = sylvia.diff.get_cache(rss)

    return rss, cache_new

def save_cache(rss: dict):
    """Save a cache dict to disk with the current date as the filename

    Args:
        rss (dict): the cache for RSS
    """

    # Get the current date and time to generate the filename
    time_string = sylvia.helpers.get_current_date_time()

    # Compose the filename
    cache_dir = os.environ['CACHE_DIR']
    filename = f"{cache_dir}/{time_string}.json"

    # Write to disk
    with open(filename, "wt") as writer:
        writer.write(json.dumps(rss))

def get_updates(old_cache: dict, new_cache: dict):
    """Get a dictionary of changes to the calendar since a previous point in time

    Args:
        old_cache (dict): dict containing the cache of the previous point of the calendar
        new_cache (dict): dict containing the cache of the current point in the calendar
    """

    # We get the keys of all old and current events
    old_events = list(old_cache.keys())
    new_events = list(new_cache.keys())

    # Will keep track of everything
    changed_events = []

    # We go over each key in the old cache
    for key in old_cache:
        # for printing
        key_friendly = key.split("/")[-1]

        # If a key in the old cache is not in the new cache, it was removed
        # This means the event is no longer on the calendar
        if key not in new_events:
            # However, it is possible that the event is no longer on the calendar because it has passed
            # So, we check whether the event is now in the past
            input_datetime = old_cache[key]["date_time"]
            event_time = datetime.strptime(input_datetime, f"%d %B %Y %H:%M")
            event_time = event_time.replace(tzinfo=brussels)
            now = datetime.now(brussels)

            # If it is, no big deal
            if event_time <= now:
                print(key_friendly, "has passed")
                continue

            # Else, this is due to a manual removal
            print(key_friendly, "not in current events")
            changed_events.append({ "key": key,
                                    "change": "deleted" })

    # We go over each key in the new cache
    for key in new_cache:
        # for printing
        key_friendly = key.split("/")[-1]

        # If a key is not in the old cache, it means it is new
        if key not in old_events:
            print(key_friendly, "not in old events")

            changed_events.append({ "key": key,
                                    "change": "added" })
        # Else, it was already in the previous cache, but it can have changed
        else:
            print(key_friendly, "found in cache")

            change_object = { "key": key,
                                "change": "changed",
                                "changes": [] }

            # Difference in date/time?
            if old_cache[key]["date"] != new_cache[key]["date"]:
                change_object["changes"].append("date")
                print(key_friendly, "date changed")

            if old_cache[key]["time"] != new_cache[key]["time"]:
                change_object["changes"].append("time")
                print(key_friendly, "time changed")

            # Difference in title?
            if old_cache[key]["title"] != new_cache[key]["title"]:
                change_object["changes"].append("title")
                print(key_friendly, "title changed")

            # Difference in description?
            if old_cache[key]["description"] != new_cache[key]["description"]:
                change_object["changes"].append("description")
                print(key_friendly, "description changed")

            if len(change_object["changes"]) == 0:
                continue

            change_object["old_event"] = old_cache[key]

            changed_events.append(change_object)

    changed_event_keys = list(map(lambda update: update["key"], changed_events))
    changed_events = dict(zip(changed_event_keys, changed_events))

    return changed_events

def join(rss: dict, changed_events: dict):
    """Join the RSS entries with calendar update information

    Args:
        rss (dict): the RSS feed to enrich
        changed_events (dict): a dictionary which dictates which elements have changed

    Returns:
        dict: RSS enriched with change information
    """

    for event in rss:
        key = event["link"]
        if key in changed_events:
            event["change"] = changed_events[key]["change"]
            
            if event["change"] == "changed":
                event["changes"] = changed_events[key]["changes"]
                event["old_event"] = changed_events[key]["old_event"]

    return rss