import argparse
from app import create_app

parser = argparse.ArgumentParser(description='Run sylvia frontend')

args = parser.parse_args()

app = create_app(debug=True)
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

app.run(host='0.0.0.0', debug=True)