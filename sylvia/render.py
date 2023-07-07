from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(
    loader=PackageLoader("website"),
    autoescape=select_autoescape()
)

template = env.get_template("calendar.html")

def calendar(rss):
    return template.render(rss=rss)