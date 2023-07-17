import os
import pytz
from datetime import datetime

import sylvia.diff

brussels = pytz.timezone("Europe/Brussels")

def get_current_date_time():
    """Get the current date and time as YYYY-MM-DD HH:MM

    Returns:
        str: the current date and time as YYYY-MM-DD HH:MM
    """

    now = datetime.now(brussels)
    time_string = now.strftime(f"%Y-%m-%d %H:%M")

    return time_string

def get_current_date():
    """Get the current date as YYYY-MM-DD

    Returns:
        str: the current date and time as YYYY-MM-DD
    """

    now = datetime.now(brussels)
    time_string = now.strftime(f"%Y-%m-%d")

    return time_string

def clean_cache_files():
    """Clean cache files in the set cache dir using the set max cache files
    """

    # Remove old checkpoints
    cache_files = sylvia.diff.get_cache_files(os.environ["CACHE_DIR"])
    max_cache_files = int(os.environ["MAX_CACHE_FILES"])
    if len(cache_files) > max_cache_files and max_cache_files != 0:
        print("Found old cache files.")
        to_remove_files = cache_files[max_cache_files:]
        for file in to_remove_files:
            filename = f"{os.environ['CACHE_DIR']}/{file}.json"
            print("Removing", filename)
            os.remove(filename)