from contextlib import asynccontextmanager
from functools import wraps
from typing import AsyncIterator, AsyncIterator, Callable, Awaitable

from databases.core import Database, Transaction
import sqlalchemy
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import Response

from .config import config


@asynccontextmanager
async def lifespan(app: Starlette) -> AsyncIterator[None]:
    async with db:
        yield


def in_transaction(
    func: Callable[[Request, Transaction], Awaitable[Response]],
) -> Callable[[Request], Awaitable[Response]]:
    @wraps(func)
    async def wrapped(request: Request) -> Response:
        async with db.transaction() as transaction:
            return await func(request, transaction)

    return wrapped


def create_db():
    metadata.create_all(sqlalchemy.create_engine(config("DATABASE_URL")))


metadata = sqlalchemy.MetaData()

notes = sqlalchemy.Table(
    "notes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("text", sqlalchemy.String),
    sqlalchemy.Column("completed", sqlalchemy.Boolean),
)

db = Database(config("DATABASE_URL"))
