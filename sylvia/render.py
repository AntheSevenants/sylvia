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
    """Get a datetime object from an RSS date

    Args:
        input_datetime (str): the RSS date field

    Returns:
        datetime: datetime parsed from RSS date
    """

    input_datetime = input_datetime.split("+")[0]
    return datetime.strptime(input_datetime, f"%Y-%m-%dT%H:%M:%S")

def print_date(input_datetime, no_convert=False):
    """Print the current date from a datetime object as DD Month YYYY

    Args:
        input_datetime (datetime): input datetime object
        no_convert (bool, optional): whether the input is already a datetime object. Defaults to False.
        
    Returns:
        str: datetime object rendered as DD Month YYYY
    """

    if not no_convert:
        event_timestamp = date_from_string(input_datetime)
    else:
        event_timestamp = input_datetime

    return event_timestamp.strftime("%-d %B %Y")

def print_time(input_datetime, no_convert=False):
    """Print the current time from a datetime object as HH:MM

    Args:
        input_datetime (datetime): input datetime object
        no_convert (bool, optional): whether the input is already a datetime object. Defaults to False.

    Returns:
        str: datetime object rendered as HH:MM
    """

    if not no_convert:
        event_timestamp = date_from_string(input_datetime)
    else:
        event_timestamp = input_datetime

    return event_timestamp.strftime("%H:%M")

def print_date_time(input_datetime, no_convert=False):
    """Print the current date and time from a datetime object as DD Month YYYY HH:MM

    Args:
        input_datetime (datetime): input datetime object
        no_convert (bool, optional): whether the input is already a datetime object. Defaults to False.

    Returns:
        str: datetime object rendered as DD Month YYYY HH:MM
    """

    if not no_convert:
        event_timestamp = date_from_string(input_datetime)
    else:
        event_timestamp = input_datetime

    # If there is just a general time, do not display 12 AM
    if event_timestamp.hour == 0 and event_timestamp.minute == 0:
        return event_timestamp.strftime("%-d %B %Y")
    else:
        return event_timestamp.strftime("%-d %B %Y %H:%M")

def calendar(rss, cache_new, cache_old=None):
    """Render the calendar as HTML

    Args:
        rss (dict): the full RSS feed representation
        cache_new (dict): the cache representation of the current RSS state
        cache_old (dict, optional): the cache representation of a previous RSS state. Defaults to None.

    Returns:
        str: the calendar as HTML
    """

    # Only diff and enrich if cache is set
    if cache_old is not None:
        # Diff the changed events
        changed_events = sylvia.diff.get_updates(cache_old, cache_new)

        # Join the changed events output with the RSS output
        rss = sylvia.diff.join(rss, changed_events)

        # Add date and time information to all events from ICS
        rss = sylvia.diff.attach_date_time(rss)

    calendar_html = as_html(rss)

    return calendar_html

def as_html(rss):
    """Renders a calendar based on a single RSS representation of the current state of the RSS feed *and* possible changes

    Args:
        rss (dict): an enriched RSS representation of the current state of the RSS feed and possible changes

    Returns:
        str: the calendar as HTML
    """

    return template.render(rss=rss,
                           print_date=print_date,
                           print_time=print_time,
                           print_date_time=print_date_time,
                           calendar_title=os.environ["CALENDAR_TITLE"],
                           calendar_notice=os.environ["CALENDAR_NOTICE"])