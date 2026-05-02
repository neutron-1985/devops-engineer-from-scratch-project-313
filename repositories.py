from sqlmodel import Session, func, select

from models import Link, LinkCreate, LinkUpdate


class LinksRepository:
    def __init__(self, engine):
        self.engine = engine

    def get_all(self):
        with Session(self.engine) as session:
            return session.exec(select(Link)).all()

    def get_range(self, start: int, end: int):
        with Session(self.engine) as session:
            statement = (
                select(Link)
                .offset(start)
                .limit(end - start)
            )
            return session.exec(statement).all()

    def count(self):
        with Session(self.engine) as session:
            statement = select(func.count()).select_from(Link)
            return session.exec(statement).one()

    def get_by_id(self, link_id: int):
        with Session(self.engine) as session:
            return session.get(Link, link_id)

    def get_by_short_name(self, short_name: str):
        with Session(self.engine) as session:
            return session.exec(
                select(Link).where(Link.short_name == short_name)
            ).first()

    def create(self, link_create: LinkCreate):
        with Session(self.engine) as session:
            link = Link(
                original_url=link_create.original_url,
                short_name=link_create.short_name,
            )
            session.add(link)
            session.commit()
            session.refresh(link)
            return link

    def update(self, link_id: int, link_update: LinkUpdate):
        with Session(self.engine) as session:
            link = session.get(Link, link_id)
            if link is None:
                return None

            link.original_url = link_update.original_url
            link.short_name = link_update.short_name
            session.add(link)
            session.commit()
            session.refresh(link)
            return link

    def delete(self, link_id: int):
        with Session(self.engine) as session:
            link = session.get(Link, link_id)
            if link is None:
                return False

            session.delete(link)
            session.commit()
            return True
