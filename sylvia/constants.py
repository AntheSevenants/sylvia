import json

with open("resources.json", "rt") as reader:
	resources = json.loads(reader.read())