from database import get_database_url
from sqlmodel import Field, Session, SQLModel, create_engine

class LinkBase(SQLModel):
    original_url: str
    short_name: str

class Link(LinkBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

class LinkCreate(LinkBase):
    pass

class LinkShow(LinkBase):
    id: int
    short_url: str

class LinkUpdate(LinkBase):
    pass



