import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_database_url():
    return os.environ["DATABASE_URL"]


def get_connection():
    return psycopg2.connect(get_database_url())

