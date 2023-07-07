import argparse
import sylvia.render
import feedparser

parser = argparse.ArgumentParser(description='sylvia - generate RSS-based event calendars')
parser.add_argument('rss_path', type=str,
					help='Path to the RSS feed the calendar should be based on')
args = parser.parse_args()

rss = feedparser.parse(args.rss_path)

print(sylvia.render.calendar(rss))