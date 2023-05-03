from base64 import b85encode
from os import getrandom

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette_wtf import CSRFProtectMiddleware

from .config import DEBUG
from .database import lifespan
from .exception_handlers import exception_handlers
from .routes import routes


app = Starlette(
    debug=DEBUG,
    routes=routes,
    lifespan=lifespan,
    middleware=[
        Middleware(GZipMiddleware, compresslevel=7),
        Middleware(SessionMiddleware, secret_key=b85encode(getrandom(16))),
        Middleware(CSRFProtectMiddleware, csrf_secret=b85encode(getrandom(16))),
    ],
    exception_handlers=exception_handlers,
)
