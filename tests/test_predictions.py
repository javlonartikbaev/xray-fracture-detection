import io

import pytest
from httpx import AsyncClient
from PIL import Image


def make_jpeg_bytes() -> bytes:
    """Create a minimal valid JPEG image in memory."""
    img = Image.new("RGB", (64, 64), color=(128, 128, 128))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()


async def _create_user(client: AsyncClient, username: str, email: str) -> int:
    resp = await client.post(
        "/users/",
        json={"username": username, "email": email, "password": "secret"},
    )
    assert resp.status_code == 201
    return resp.json()["id"]


async def test_upload_prediction(client: AsyncClient):
    user_id = await _create_user(client, "imguser", "imguser@example.com")
    jpeg = make_jpeg_bytes()
    response = await client.post(
        "/predictions/upload",
        data={"user_id": str(user_id), "body_part": "wrist"},
        files={"file": ("xray.jpg", jpeg, "image/jpeg")},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == user_id
    assert data["original_filename"] == "xray.jpg"
    assert data["body_part"] == "wrist"
    assert isinstance(data["fracture_detected"], bool)
    assert 0.0 <= data["confidence"] <= 1.0


async def test_list_predictions(client: AsyncClient):
    user_id = await _create_user(client, "listuser", "listuser@example.com")
    jpeg = make_jpeg_bytes()
    await client.post(
        "/predictions/upload",
        data={"user_id": str(user_id)},
        files={"file": ("xray.jpg", jpeg, "image/jpeg")},
    )
    response = await client.get("/predictions/", params={"user_id": user_id})
    assert response.status_code == 200
    assert len(response.json()) >= 1


async def test_list_predictions_all(client: AsyncClient):
    response = await client.get("/predictions/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_get_prediction(client: AsyncClient):
    user_id = await _create_user(client, "getpreduser", "getpreduser@example.com")
    jpeg = make_jpeg_bytes()
    upload_resp = await client.post(
        "/predictions/upload",
        data={"user_id": str(user_id)},
        files={"file": ("xray.jpg", jpeg, "image/jpeg")},
    )
    pred_id = upload_resp.json()["id"]
    response = await client.get(f"/predictions/{pred_id}")
    assert response.status_code == 200
    assert response.json()["id"] == pred_id


async def test_get_prediction_not_found(client: AsyncClient):
    response = await client.get("/predictions/99999")
    assert response.status_code == 404


async def test_delete_prediction(client: AsyncClient):
    user_id = await _create_user(client, "deluser", "deluser@example.com")
    jpeg = make_jpeg_bytes()
    upload_resp = await client.post(
        "/predictions/upload",
        data={"user_id": str(user_id)},
        files={"file": ("xray.jpg", jpeg, "image/jpeg")},
    )
    pred_id = upload_resp.json()["id"]
    response = await client.delete(f"/predictions/{pred_id}")
    assert response.status_code == 204
    response = await client.get(f"/predictions/{pred_id}")
    assert response.status_code == 404


async def test_delete_prediction_not_found(client: AsyncClient):
    response = await client.delete("/predictions/99999")
    assert response.status_code == 404
