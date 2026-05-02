from datetime import UTC, datetime
from http import HTTPStatus
from types import SimpleNamespace

from fastapi.testclient import TestClient

from main import app
from repositories import LinksRepository

client = TestClient(app)


def make_link(
        link_id=1,
        original_url="https://example.com",
        short_name="example",
        created_at=datetime(2026, 1, 1, 12, 0, tzinfo=UTC),
    ):
    return SimpleNamespace(
        id=link_id,
        original_url=original_url,
        short_name=short_name,
        created_at=created_at,
    )


def make_link_response(link):
    return {
        "id": link.id,
        "original_url": link.original_url,
        "short_name": link.short_name,
        "short_url": f"https://short.io/r/{link.short_name}",
        "created_at": link.created_at.isoformat().replace("+00:00", "Z"),
    }


def make_not_found_response(path):
    return {
        "error": "Not Found",
        "message": "Страница не найдена",
        "path": f"http://testserver{path}",
    }


def make_duplicate_response():
    return {"detail": "short_name already exists"}


def test_get_links(monkeypatch):
    link = make_link()

    def fake_get_all(self):
        return [link]

    monkeypatch.setattr(
        LinksRepository,
        "get_all",
        fake_get_all
    )

    response = client.get("/api/links")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == [make_link_response(link)]

def test_get_link(monkeypatch):
    link = make_link()

    def fake_get_link(self, id):
        return link

    monkeypatch.setattr(
        LinksRepository,
        "get_by_id",
        fake_get_link
    )

    response = client.get(f"/api/links/{link.id}")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == make_link_response(link)


def test_get_link_not_found(monkeypatch):
    link_id = 404

    def fake_get_link(self, id):
        assert id == link_id
        return None

    monkeypatch.setattr(
        LinksRepository,
        "get_by_id",
        fake_get_link,
    )

    response = client.get(f"/api/links/{link_id}")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == make_not_found_response(f"/api/links/{link_id}")


def test_edit_link(monkeypatch):
    link = make_link()

    new_url = "https://example.com/new"
    new_name = "new-name"

    def fake_update_link(self, link_id, link_update):
        assert link_id == link.id
        assert link_update.original_url == new_url
        assert link_update.short_name == new_name
        link.original_url = link_update.original_url
        link.short_name = link_update.short_name
        return link

    def fake_get_by_short_name(self, short_name):
        assert short_name == new_name
        return None

    monkeypatch.setattr(
        LinksRepository,
        "get_by_short_name",
        fake_get_by_short_name,
    )

    monkeypatch.setattr(
        LinksRepository,
        "update",
        fake_update_link,
    )

    response = client.put(
        f"/api/links/{link.id}",
        json={
            "original_url": new_url,
            "short_name": new_name,
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == make_link_response(link)


def test_edit_link_duplicate_short_name(monkeypatch):
    link = make_link()
    existing_link = make_link(link_id=2, short_name="existing-name")

    def fake_get_by_short_name(self, short_name):
        assert short_name == existing_link.short_name
        return existing_link

    monkeypatch.setattr(
        LinksRepository,
        "get_by_short_name",
        fake_get_by_short_name,
    )

    response = client.put(
        f"/api/links/{link.id}",
        json={
            "original_url": "https://example.com/new",
            "short_name": "existing-name",
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == make_duplicate_response()


def test_delete_link(monkeypatch):
    link = make_link()

    def fake_delete_link(self, link_id):
        assert link_id == link.id
        return True

    monkeypatch.setattr(
        LinksRepository,
        "delete",
        fake_delete_link,
    )

    response = client.delete(f"/api/links/{link.id}")

    assert response.status_code == HTTPStatus.NO_CONTENT
    assert response.content == b""


def test_delete_link_not_found(monkeypatch):
    link_id = 404

    def fake_delete_link(self, id):
        assert id == link_id
        return False

    monkeypatch.setattr(
        LinksRepository,
        "delete",
        fake_delete_link,
    )

    response = client.delete(f"/api/links/{link_id}")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == make_not_found_response(f"/api/links/{link_id}")


def test_create_link(monkeypatch):
    link = make_link()

    def fake_get_by_short_name(self, short_name):
        assert short_name == link.short_name
        return None

    def fake_create_link(self, link_create):
        assert link_create.original_url == link.original_url
        assert link_create.short_name == link.short_name
        return link

    monkeypatch.setattr(
        LinksRepository,
        "get_by_short_name",
        fake_get_by_short_name,
    )

    monkeypatch.setattr(
        LinksRepository,
        "create",
        fake_create_link,
    )

    response = client.post(
        "/api/links",
        json={
            "original_url": link.original_url,
            "short_name": link.short_name,
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == make_link_response(link)


def test_create_link_duplicate_short_name(monkeypatch):
    link = make_link()

    def fake_get_by_short_name(self, short_name):
        assert short_name == link.short_name
        return link

    monkeypatch.setattr(
        LinksRepository,
        "get_by_short_name",
        fake_get_by_short_name,
    )

    response = client.post(
        "/api/links",
        json={
            "original_url": link.original_url,
            "short_name": link.short_name,
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == make_duplicate_response()
