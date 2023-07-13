import pytz
import sylvia.render

from datetime import datetime

brussels = pytz.timezone("Europe/Brussels")

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
        date_time = sylvia.render.print_date_time(entry["updated"])

        cache[key] = {
            "title": entry["title"],
            "date_time": date_time,
            "description": entry["description"]
        }

    return cache

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
            if old_cache[key]["date_time"] != new_cache[key]["date_time"]:
                change_object["changes"].append("date_time")
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

            changed_events.append(change_object)

    changed_event_keys = list(map(lambda update: update["key"], changed_events))
    changed_events = dict(zip(changed_event_keys, changed_events))

    return changed_events

def join(rss, changed_events):
    for event in rss:
        key = event["link"]
        if key in changed_events:
            event["change"] = changed_events[key]["change"]
            
            if event["change"] == "changed":
                event["changes"] = changed_events[key]["changes"]

    return rss