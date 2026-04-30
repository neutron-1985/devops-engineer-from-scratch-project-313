import psycopg

from database import get_connection


class ShortNameAlreadyExistsError(Exception):
    pass


def get_links():
    with get_connection() as conn:
        with conn.cursor() as curs:
            curs.execute("SELECT id, original_url, short_name, created_at FROM link")
            return curs.fetchall()


def create_link(original_url: str, short_name: str):
    try:
        with get_connection() as conn:
            with conn.cursor() as curs:
                curs.execute(
                    """
                    INSERT INTO link (original_url, short_name)
                    VALUES (%s, %s)
                    RETURNING id, original_url, short_name, created_at
                    """,
                    (original_url, short_name),
                )
                return curs.fetchone()
    except psycopg.errors.UniqueViolation as exc:
        raise ShortNameAlreadyExistsError from exc


def get_link(link_id: int):
    with get_connection() as conn:
        with conn.cursor() as curs:
            curs.execute(
                """
                SELECT id, original_url, short_name, created_at
                FROM link
                WHERE id = %s
                """,
                (link_id,),
            )
            return curs.fetchone()


def update_link(link_id: int, original_url: str, short_name: str):
    try:
        with get_connection() as conn:
            with conn.cursor() as curs:
                curs.execute(
                    """
                    UPDATE link
                    SET original_url = %s,
                        short_name = %s
                    WHERE id = %s
                    RETURNING id, original_url, short_name, created_at
                    """,
                    (original_url, short_name, link_id),
                )
                return curs.fetchone()
    except psycopg.errors.UniqueViolation as exc:
        raise ShortNameAlreadyExistsError from exc


def delete_link(link_id: int) -> bool:
    with get_connection() as conn:
        with conn.cursor() as curs:
            curs.execute("DELETE FROM link WHERE id = %s", (link_id,))
            return curs.rowcount > 0
