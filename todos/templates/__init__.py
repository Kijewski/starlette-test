from pathlib import Path

from jinja2 import Environment, FileSystemLoader


loader = FileSystemLoader(Path(__file__).parent)
env = Environment(loader=loader)
