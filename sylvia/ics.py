import os
import pytz
import urllib.request
from ics import Calendar

brussels = pytz.timezone(os.environ["TZ"])

def get_event_times(url):
    ical = urllib.request.urlopen(url).read().decode("UTF-8")

    cal = Calendar(ical)
    event = list(cal.events)[0]

    event_begin = event.begin.to(brussels)
    event_end = event.end.to(brussels)

    return event_begin, event_end