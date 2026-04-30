import os

import psycopg
from dotenv import load_dotenv
from psycopg.rows import namedtuple_row
from sqlmodel import SQLModel, create_engine

load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]

engine = create_engine(
    DATABASE_URL,
    echo=True,
)


def init_db():
    import models  # noqa: F401

    SQLModel.metadata.create_all(engine)


def get_connection():
    database_url = DATABASE_URL.replace(
        "postgresql+psycopg://",
        "postgresql://",
        1,
    )
    return psycopg.connect(database_url, row_factory=namedtuple_row)
