import os

import sylvia.diff

from datetime import datetime

from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(
    loader=PackageLoader("website"),
    autoescape=select_autoescape()
)

template = env.get_template("calendar.html")

def date_from_string(input_datetime):
    input_datetime = input_datetime.split("+")[0]
    return datetime.strptime(input_datetime, f"%Y-%m-%dT%H:%M:%S")

def print_date(input_datetime):
    event_timestamp = date_from_string(input_datetime)

    return event_timestamp.strftime("%-d %B %Y")

def print_time(input_datetime):
    event_timestamp = date_from_string(input_datetime)

    return event_timestamp.strftime("%H:%M")

def print_date_time(input_datetime):
    event_timestamp = date_from_string(input_datetime)

    return event_timestamp.strftime("%-d %B %Y %H:%M")

def calendar(rss, cache_new, cache_old=None):
    # Only diff and enrich if cache is set
    if cache_old is not None:
        # Diff the changed events
        changed_events = sylvia.diff.get_updates(cache_old, cache_new)

        # Join the changed events output with the RSS output
        rss = sylvia.diff.join(rss, changed_events)

    calendar_html = sylvia.render.as_html(rss)

    return calendar_html

def as_html(rss):
    return template.render(rss=rss,
                           print_date=print_date,
                           print_time=print_time,
                           print_date_time=print_date_time,
                           calendar_title=os.environ["CALENDAR_TITLE"],
                           calendar_notice=os.environ["CALENDAR_NOTICE"])