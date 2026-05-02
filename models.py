from datetime import datetime

from sqlalchemy import Column, DateTime, func
from sqlmodel import Field, SQLModel


class LinkBase(SQLModel):
    original_url: str
    short_name: str

class Link(LinkBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            server_default=func.now(),
        ),
    )

class LinkCreate(LinkBase):
    pass

class LinkShow(LinkBase):
    id: int
    short_url: str
    created_at: datetime | None

class LinkUpdate(LinkBase):
    pass
