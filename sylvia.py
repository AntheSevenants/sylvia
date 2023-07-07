import argparse

parser = argparse.ArgumentParser(description='sylvia - generate RSS-based event calendars')
parser.add_argument('rss_path', type=str,
					help='Path to the RSS feed the calendar should be based on')
args = parser.parse_args()

print(args.rss_path)