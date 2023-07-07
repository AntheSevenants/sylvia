from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(
    loader=PackageLoader("html"),
    autoescape=select_autoescape()
)

template = env.get_template("calendar.html")

def calendar(events):
    return template.render()