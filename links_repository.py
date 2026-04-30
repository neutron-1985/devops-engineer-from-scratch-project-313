from database import get_connection


def get_links():
    with get_connection() as conn:
        with conn.cursor() as curs:
            curs.execute("SELECT id, original_url, short_name FROM link")
            return curs.fetchall()


def create_link(original_url: str, short_name: str):
    with get_connection() as conn:
        with conn.cursor() as curs:
            curs.execute(
                """
                INSERT INTO link (original_url, short_name)
                VALUES (%s, %s)
                """,
                (original_url, short_name),
            )


def get_link(link_id: int):
    with get_connection() as conn:
        with conn.cursor() as curs:
            curs.execute(
                "SELECT id, original_url, short_name FROM link WHERE id = %s",
                (link_id,),
            )
            return curs.fetchone()


def update_link(link_id: int, original_url: str, short_name: str):
    with get_connection() as conn:
        with conn.cursor() as curs:
            curs.execute(
                """
                UPDATE link
                SET original_url = %s,
                    short_name = %s
                WHERE id = %s
                """,
                (original_url, short_name, link_id),
            )

            if curs.rowcount == 0:
                return None

            curs.execute(
                "SELECT id, original_url, short_name FROM link WHERE id = %s",
                (link_id,),
            )
            return curs.fetchone()


def delete_link(link_id: int) -> bool:
    with get_connection() as conn:
        with conn.cursor() as curs:
            curs.execute("DELETE FROM link WHERE id = %s", (link_id,))
            return curs.rowcount > 0
