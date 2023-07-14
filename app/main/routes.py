import sylvia.diff

from flask import session, redirect, url_for, render_template, request, send_file, current_app
from . import main

print("routes are loaded")

@main.route('/')
def index():
    # TODO remove hardcoding
    cache_files = sylvia.diff.get_cache_files("cache/")

    return render_template('index.html', cache_files=cache_files)