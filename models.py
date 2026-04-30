from sqlmodel import Field, SQLModel


class LinkBase(SQLModel):
    original_url: str
    short_name: str


class Link(LinkBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class LinkCreate(LinkBase):
    pass


class LinkUpdate(LinkBase):
    pass


class LinkRead(LinkBase):
    id: int
    short_url: str
