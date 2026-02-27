import pytest
from httpx import AsyncClient


async def test_create_user(client: AsyncClient):
    response = await client.post(
        "/users/",
        json={"username": "alice", "email": "alice@example.com", "password": "secret"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "alice"
    assert data["email"] == "alice@example.com"
    assert data["is_active"] is True
    assert "id" in data


async def test_create_user_duplicate_email(client: AsyncClient):
    payload = {"username": "bob", "email": "bob@example.com", "password": "secret"}
    await client.post("/users/", json=payload)
    payload["username"] = "bob2"
    response = await client.post("/users/", json=payload)
    assert response.status_code == 400


async def test_create_user_duplicate_username(client: AsyncClient):
    payload = {"username": "charlie", "email": "charlie@example.com", "password": "secret"}
    await client.post("/users/", json=payload)
    payload["email"] = "charlie2@example.com"
    response = await client.post("/users/", json=payload)
    assert response.status_code == 400


async def test_list_users(client: AsyncClient):
    await client.post(
        "/users/",
        json={"username": "dave", "email": "dave@example.com", "password": "secret"},
    )
    response = await client.get("/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1


async def test_get_user(client: AsyncClient):
    create_resp = await client.post(
        "/users/",
        json={"username": "eve", "email": "eve@example.com", "password": "secret"},
    )
    user_id = create_resp.json()["id"]
    response = await client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["username"] == "eve"


async def test_get_user_not_found(client: AsyncClient):
    response = await client.get("/users/99999")
    assert response.status_code == 404


async def test_update_user(client: AsyncClient):
    create_resp = await client.post(
        "/users/",
        json={"username": "frank", "email": "frank@example.com", "password": "secret"},
    )
    user_id = create_resp.json()["id"]
    response = await client.put(f"/users/{user_id}", json={"username": "frank2"})
    assert response.status_code == 200
    assert response.json()["username"] == "frank2"


async def test_delete_user(client: AsyncClient):
    create_resp = await client.post(
        "/users/",
        json={"username": "grace", "email": "grace@example.com", "password": "secret"},
    )
    user_id = create_resp.json()["id"]
    response = await client.delete(f"/users/{user_id}")
    assert response.status_code == 204
    response = await client.get(f"/users/{user_id}")
    assert response.status_code == 404


async def test_delete_user_not_found(client: AsyncClient):
    response = await client.delete("/users/99999")
    assert response.status_code == 404
