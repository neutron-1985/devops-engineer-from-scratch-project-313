import os

import psycopg
from dotenv import load_dotenv

load_dotenv()


def get_database_url():
    database_url = os.environ["DATABASE_URL"]
    if database_url.startswith("postgres://"):
        return database_url.replace("postgres://", "postgresql+psycopg://", 1)
    if database_url.startswith("postgresql://"):
        return database_url.replace("postgresql://", "postgresql+psycopg://", 1)
    return database_url


def get_connection():
    return psycopg.connect(get_database_url())
