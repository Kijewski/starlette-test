from pathlib import Path

from starlette.routing import Mount
from starlette.staticfiles import StaticFiles

from . import edit, list


routes = [
    *edit.routes,
    *list.routes,
    Mount(
        "/static",
        app=StaticFiles(directory=Path(__file__).parent.parent / "static"),
        name="static",
    ),
]
