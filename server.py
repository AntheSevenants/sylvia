import os
import argparse
from app import create_app

parser = argparse.ArgumentParser(description='Run sylvia frontend')
parser.add_argument('-debug', '--debug', nargs='?', type=bool, default=False, help='output file, in JSON format')

args = parser.parse_args()

debug = args.debug

environment_variables = [ "RSS_URL", "CACHE_DIR", "MAX_CACHE_FILES", "CALENDAR_TITLE", "CALENDAR_NOTICE", "EMAIL_TO", "TZ" ]

for environment_variable in environment_variables:
	if not environment_variable in os.environ:
		raise Exception(f"Environment variable '{environment_variable}' missing")


app = create_app(debug=debug)

if debug:
	app.jinja_env.auto_reload = True
	app.config['TEMPLATES_AUTO_RELOAD'] = True
	app.run(host='0.0.0.0', debug=debug)
else:
	from waitress import serve
	print("Sylvia started")
	serve(app, host='0.0.0.0', port=8080)