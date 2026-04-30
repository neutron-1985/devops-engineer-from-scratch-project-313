import os

from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine

load_dotenv()


engine = create_engine(
    os.environ["DATABASE_URL"],
    echo=True,
)


def init_db():
    import models  # noqa: F401

    SQLModel.metadata.create_all(engine)
