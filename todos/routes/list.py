from starlette.responses import Response, HTMLResponse
from starlette.requests import Request
from starlette.routing import Route

from ..database import notes, db
from ..templates import env
from ..forms import NoteForm


template = env.get_template("notes.html")


async def list_notes(request: Request) -> Response:
    form = await NoteForm.from_formdata(request, formdata=None)
    results = await db.fetch_all(notes.select())
    body = template.render(request=request, results=results, form=form)
    return HTMLResponse(body)


routes = [
    Route("/", list_notes, methods=["GET"], name="list_notes"),
]
