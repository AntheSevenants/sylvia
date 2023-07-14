from flask import session, redirect, url_for, render_template, request, send_file, current_app
from . import main

print("routes are loaded")

@main.route('/')
def index():
    print("hallo met Gert")
    return render_template('index.html')