import pytz
from datetime import datetime

brussels = pytz.timezone("Europe/Brussels")

def get_current_date_time():
    now = datetime.now(brussels)
    time_string = now.strftime(f"%Y-%m-%d %H:%M")

    return time_string