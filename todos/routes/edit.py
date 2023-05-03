from databases.core import Transaction, ClauseElement
from lru import LRU
from starlette.responses import Response, HTMLResponse, RedirectResponse
from starlette.requests import Request
from starlette.routing import Route
from starlette.status import (
    HTTP_303_SEE_OTHER,
    HTTP_307_TEMPORARY_REDIRECT,
    HTTP_404_NOT_FOUND,
)
from starlette.exceptions import HTTPException
from starlette_wtf.csrf import DEFAULT_CSRF_FIELD_NAME as CSRF_KEY

from ..database import notes, db
from ..templates import env
from ..forms import NoteForm


template = env.get_template("note.html")
seen_csrfs = LRU(2**14)


async def edit_note(request: Request) -> Response:
    query: ClauseElement

    form = await NoteForm.from_formdata(request)

    req_id = request.path_params.get("id") or 0
    if not form.is_submitted():
        if req_id:
            query = notes.select().where(notes.c.id == req_id)
            note = await db.fetch_one(query)
            if note is None:
                raise HTTPException(status_code=HTTP_404_NOT_FOUND)
            form.process(obj=note)
        return HTMLResponse(template.render(request=request, form=form))

    form_id = form.id.data or 0
    if req_id != form_id:
        return RedirectResponse(
            request.url_for("edit_note", id=form_id),
            HTTP_307_TEMPORARY_REDIRECT,
        )

    csrf_token = request.session.get(CSRF_KEY)
    if csrf_token in seen_csrfs:
        return RedirectResponse(
            request.url_for("edit_note", id=form_id),
            HTTP_303_SEE_OTHER,
        )

    if not await form.validate_on_submit():
        return HTMLResponse(template.render(request=request, form=form))

    async with db.transaction():
        if not form_id:
            query = notes.insert().values(
                text=form.text.data,
                completed=form.completed.data,
            )
        elif form.delete.data:
            query = notes.delete().where(notes.c.id == form_id)
        else:
            query = (
                notes.update()
                .where(notes.c.id == form_id)
                .values(
                    text=form.text.data,
                    completed=form.completed.data,
                )
            )
        await db.execute(query)

        seen_csrfs[csrf_token] = True
        del request.session[CSRF_KEY]
        return RedirectResponse(request.url_for("list_notes"), HTTP_303_SEE_OTHER)


routes = [
    Route("/{id:int}.html", edit_note, methods=["GET", "POST"], name="edit_note"),
]
