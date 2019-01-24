from config import Config
from jinja2 import Template

def interpolate_variables(message):
    template = Template(message)
    result = template.render(Config().get()["variables"])
    return result
