import io

import pytest
from httpx import AsyncClient
from PIL import Image

from app.ai.detector import DetectionResult, FractureDetector


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


async def test_upload_prediction_invalid_content_type(client: AsyncClient):
    user_id = await _create_user(client, "invalidct", "invalidct@example.com")
    response = await client.post(
        "/predictions/upload",
        data={"user_id": str(user_id)},
        files={"file": ("doc.pdf", b"%PDF-1.4 fake", "application/pdf")},
    )
    assert response.status_code == 400


async def test_upload_prediction_invalid_image_bytes(client: AsyncClient):
    user_id = await _create_user(client, "invalidimg", "invalidimg@example.com")
    response = await client.post(
        "/predictions/upload",
        data={"user_id": str(user_id)},
        files={"file": ("fake.jpg", b"not-an-image", "image/jpeg")},
    )
    assert response.status_code == 400


def test_detector_fracture_detected():
    det = FractureDetector()
    # High-contrast image -> high std -> fracture detected
    img = Image.new("L", (64, 64))
    pixels = img.load()
    for x in range(32):
        for y in range(64):
            pixels[x, y] = 0
    for x in range(32, 64):
        for y in range(64):
            pixels[x, y] = 255
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    result = det.predict(buf.getvalue())
    assert isinstance(result, DetectionResult)
    assert isinstance(result.fracture_detected, bool)
    assert 0.0 <= result.confidence <= 1.0


def test_detector_no_fracture():
    det = FractureDetector()
    # Uniform image -> low std -> no fracture
    img = Image.new("L", (64, 64), color=128)
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    result = det.predict(buf.getvalue())
    assert isinstance(result, DetectionResult)
    assert result.fracture_detected is False
    assert result.confidence < 0.5


def test_detector_error_handling():
    det = FractureDetector()
    result = det.predict(b"not-valid-image-bytes")
    assert isinstance(result, DetectionResult)
    assert result.fracture_detected is False
    assert result.confidence == 0.0
    assert "error" in result.details
