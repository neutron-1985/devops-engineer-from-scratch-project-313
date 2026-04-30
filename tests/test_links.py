from datetime import UTC, datetime
from http import HTTPStatus
from types import SimpleNamespace

from fastapi.testclient import TestClient

import links_repository
from main import app

client = TestClient(app)


def make_link(
    link_id=1,
    original_url="https://example.com",
    short_name="example",
):
    return SimpleNamespace(
        id=link_id,
        original_url=original_url,
        short_name=short_name,
        created_at=datetime(2026, 1, 1, tzinfo=UTC),
    )


def make_link_response(link):
    return {
        "id": link.id,
        "original_url": link.original_url,
        "short_name": link.short_name,
        "created_at": "2026-01-01T00:00:00Z",
        "short_url": f"https://short.io/r/{link.short_name}",
    }


def test_get_links(monkeypatch):
    link = make_link()

    monkeypatch.setattr(links_repository, "get_links", lambda: [link])

    response = client.get("/api/links")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == [make_link_response(link)]


def test_create_link(monkeypatch):
    link = make_link()

    def create_link(original_url, short_name):
        assert original_url == link.original_url
        assert short_name == link.short_name
        return link

    monkeypatch.setattr(links_repository, "create_link", create_link)

    response = client.post(
        "/api/links",
        json={
            "original_url": link.original_url,
            "short_name": link.short_name,
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == make_link_response(link)


def test_create_link_with_existing_short_name(monkeypatch):
    def create_link(_original_url, _short_name):
        raise links_repository.ShortNameAlreadyExistsError

    monkeypatch.setattr(links_repository, "create_link", create_link)

    response = client.post(
        "/api/links",
        json={
            "original_url": "https://example.com",
            "short_name": "example",
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"error": "Short name already exists"}


def test_get_link(monkeypatch):
    link = make_link()

    monkeypatch.setattr(links_repository, "get_link", lambda _link_id: link)

    response = client.get(f"/api/links/{link.id}")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == make_link_response(link)


def test_get_missing_link(monkeypatch):
    monkeypatch.setattr(links_repository, "get_link", lambda _link_id: None)

    response = client.get("/api/links/1")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"error": "Not found"}


def test_update_link(monkeypatch):
    link = make_link(
        original_url="https://updated.example.com",
        short_name="updated",
    )

    def update_link(link_id, original_url, short_name):
        assert link_id == link.id
        assert original_url == link.original_url
        assert short_name == link.short_name
        return link

    monkeypatch.setattr(links_repository, "update_link", update_link)

    response = client.put(
        f"/api/links/{link.id}",
        json={
            "original_url": link.original_url,
            "short_name": link.short_name,
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == make_link_response(link)


def test_update_missing_link(monkeypatch):
    monkeypatch.setattr(
        links_repository,
        "update_link",
        lambda _link_id, _original_url, _short_name: None,
    )

    response = client.put(
        "/api/links/1",
        json={
            "original_url": "https://example.com",
            "short_name": "example",
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"error": "Not found"}


def test_update_link_with_existing_short_name(monkeypatch):
    def update_link(_link_id, _original_url, _short_name):
        raise links_repository.ShortNameAlreadyExistsError

    monkeypatch.setattr(links_repository, "update_link", update_link)

    response = client.put(
        "/api/links/1",
        json={
            "original_url": "https://example.com",
            "short_name": "example",
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"error": "Short name already exists"}


def test_delete_link(monkeypatch):
    monkeypatch.setattr(links_repository, "delete_link", lambda _link_id: True)

    response = client.delete("/api/links/1")

    assert response.status_code == HTTPStatus.NO_CONTENT
    assert response.content == b""


def test_delete_missing_link(monkeypatch):
    monkeypatch.setattr(links_repository, "delete_link", lambda _link_id: False)

    response = client.delete("/api/links/1")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"error": "Not found"}
