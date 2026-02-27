import io

from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile, status
from PIL import Image
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_db
from app.schemas.prediction import PredictionResponse
from app.services import prediction_service

router = APIRouter(prefix="/predictions", tags=["predictions"])

ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp", "image/tiff"}


@router.post("/upload", response_model=PredictionResponse, status_code=status.HTTP_201_CREATED)
async def upload_prediction(
    file: UploadFile,
    user_id: int = Form(...),
    body_part: str | None = Form(None),
    notes: str | None = Form(None),
    db: AsyncSession = Depends(get_db),
):
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=400, detail="File must be a valid image (JPEG, PNG, GIF, WebP, TIFF)")

    image_bytes = await file.read()
    if not image_bytes:
        raise HTTPException(status_code=400, detail="Empty file uploaded")
    if len(image_bytes) > settings.max_file_size:
        raise HTTPException(status_code=413, detail=f"File exceeds maximum size of {settings.max_file_size} bytes")

    try:
        Image.open(io.BytesIO(image_bytes)).verify()
    except Exception:
        raise HTTPException(status_code=400, detail="Uploaded file is not a valid image")
    return await prediction_service.create_prediction(
        db=db,
        user_id=user_id,
        image_bytes=image_bytes,
        original_filename=file.filename or "upload.jpg",
        body_part=body_part,
        notes=notes,
    )


@router.get("/", response_model=list[PredictionResponse])
async def list_predictions(
    user_id: int | None = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    return await prediction_service.get_predictions(db, user_id=user_id, skip=skip, limit=limit)


@router.get("/{prediction_id}", response_model=PredictionResponse)
async def get_prediction(prediction_id: int, db: AsyncSession = Depends(get_db)):
    prediction = await prediction_service.get_prediction_by_id(db, prediction_id)
    if prediction is None:
        raise HTTPException(status_code=404, detail="Prediction not found")
    return prediction


@router.delete("/{prediction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_prediction(prediction_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await prediction_service.delete_prediction(db, prediction_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Prediction not found")
