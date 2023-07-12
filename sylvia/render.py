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

    return event_timestamp.strftime("%-H:%M")


def calendar(rss):
    return template.render(rss=rss,
                           print_date=print_date,
                           print_time=print_time)