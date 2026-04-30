import os

import psycopg
from dotenv import load_dotenv
from psycopg.rows import namedtuple_row
from sqlmodel import SQLModel, create_engine

load_dotenv()


def get_database_url():
    return os.environ["DATABASE_URL"]


def init_db():
    import models  # noqa: F401

    engine = create_engine(
        get_database_url(),
        echo=True,
    )

    SQLModel.metadata.create_all(engine)

    with engine.begin() as connection:
        connection.exec_driver_sql(
            """
            ALTER TABLE link
            ADD COLUMN IF NOT EXISTS created_at TIMESTAMPTZ NOT NULL
            DEFAULT CURRENT_TIMESTAMP
            """,
        )
        connection.exec_driver_sql(
            """
            CREATE UNIQUE INDEX IF NOT EXISTS ix_link_short_name_unique
            ON link (short_name)
            """,
        )


def get_connection():
    database_url = get_database_url().replace(
        "postgresql+psycopg://",
        "postgresql://",
        1,
    )
    return psycopg.connect(database_url, row_factory=namedtuple_row)
