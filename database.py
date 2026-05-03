import os

from dotenv import load_dotenv

load_dotenv()


def get_sqlalchemy_database_url():
    database_url = os.environ["DATABASE_URL"]
    if database_url.startswith("postgres://"):
        return database_url.replace("postgres://", "postgresql+psycopg://", 1)
    if database_url.startswith("postgresql://"):
        return database_url.replace("postgresql://", "postgresql+psycopg://", 1)
    return database_url
