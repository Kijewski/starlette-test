from starlette.requests import Request
from starlette.responses import HTMLResponse, Response
from starlette.status import (
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from .config import DEBUG
from .templates import env


template_404 = env.get_template("http/404.html")
template_500 = env.get_template("http/500.html")


async def not_found(request: Request, exc: Exception) -> Response:
    body = template_404.render(request=request, exc=exc)
    return HTMLResponse(content=body, status_code=HTTP_404_NOT_FOUND)


async def server_error(request: Request, exc: Exception) -> Response:
    body = template_500.render(request=request, exc=exc)
    return HTMLResponse(content=body, status_code=HTTP_500_INTERNAL_SERVER_ERROR)


exception_handlers = {
    HTTP_404_NOT_FOUND: not_found,
    **({HTTP_500_INTERNAL_SERVER_ERROR: server_error} if not DEBUG else {}),
}
