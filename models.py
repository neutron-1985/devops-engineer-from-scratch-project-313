from datetime import datetime

from sqlalchemy import Column, DateTime, String, text
from sqlmodel import Field, SQLModel


class LinkBase(SQLModel):
    original_url: str
    short_name: str


class Link(LinkBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    short_name: str = Field(sa_column=Column(String, unique=True, nullable=False))
    created_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        ),
    )


class LinkCreate(LinkBase):
    pass


class LinkUpdate(LinkBase):
    pass


class LinkRead(LinkBase):
    id: int
    created_at: datetime
    short_url: str
