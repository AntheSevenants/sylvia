import os
import json

import sylvia.error
import sylvia.diff
import sylvia.render
import sylvia.email
import sylvia.helpers

from flask import session, redirect, url_for, render_template, request, send_file, current_app, Response
from . import main

@main.route('/')
def index():
    cache_files = sylvia.diff.get_cache_files(os.environ["CACHE_DIR"])

    return render_template('index.html', cache_files=cache_files)

@main.route('/calendar', methods = ["GET", "POST"])
def calendar():
    if request.method != "POST":
        return sylvia.error.generate("This endpoint only accepts POST requests.")
    
    if not "changes_source" in request.form:
        return sylvia.error.generate("Malformed POST request.")
    
    cache_file = request.form["changes_source"]
    cache_old = sylvia.diff.get_cache_from_path(cache_file)
    rss, cache_new = sylvia.diff.get_rss_new()

    calendar_html = sylvia.render.calendar(rss, cache_new, cache_old)

    return render_template('calendar.html', calendar_html=calendar_html, cache_file=cache_file)


@main.route('/download', methods = ["GET", "POST"])
def download():
    if request.method != "POST":
        return sylvia.error.generate("This endpoint only accepts POST requests.")
    
    if not "changes_source" in request.form:
        return sylvia.error.generate("Malformed POST request.")
    
    cache_file = request.form["changes_source"]
    cache_old = sylvia.diff.get_cache_from_path(cache_file)
    rss, cache_new = sylvia.diff.get_rss_new()

    calendar_html = sylvia.render.calendar(rss, cache_new, cache_old)

    eml_content = sylvia.email.create("TODO@TODO.com", "Agenda OE Taalkunde TODO", calendar_html)

    email_filename = f"{os.environ['CALENDAR_TITLE']} - {sylvia.helpers.get_current_date_time()}.eml"

    # Create a checkpoint
    sylvia.diff.save_cache(cache_new)

    # Remove old cache files
    sylvia.helpers.clean_cache_files()

    return Response(eml_content,
                    mimetype="text/plain",
                    headers={"Content-disposition": f"attachment; filename={email_filename}"})