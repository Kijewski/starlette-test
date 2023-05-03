#!/usr/bin/env python3
# pipenv run ./create-db.py

from logging import basicConfig, INFO

from todos.database import create_db


if __name__ == "__main__":
    basicConfig(level=INFO)
    create_db()
