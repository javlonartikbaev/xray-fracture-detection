import os
import uuid

import aiofiles
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.detector import detector
from app.config import settings
from app.models.prediction import XRayPrediction


async def create_prediction(
    db: AsyncSession,
    user_id: int,
    image_bytes: bytes,
    original_filename: str,
    body_part: str | None = None,
    notes: str | None = None,
) -> XRayPrediction:
    os.makedirs(settings.upload_dir, exist_ok=True)

    ext = os.path.splitext(original_filename)[1] or ".jpg"
    image_filename = f"{uuid.uuid4()}{ext}"
    file_path = os.path.join(settings.upload_dir, image_filename)

    async with aiofiles.open(file_path, "wb") as f:
        await f.write(image_bytes)

    result = detector.predict(image_bytes)

    prediction = XRayPrediction(
        user_id=user_id,
        image_filename=image_filename,
        original_filename=original_filename,
        fracture_detected=result.fracture_detected,
        confidence=result.confidence,
        body_part=body_part,
        notes=notes,
    )
    db.add(prediction)
    await db.commit()
    await db.refresh(prediction)
    return prediction


async def get_predictions(
    db: AsyncSession, user_id: int | None = None, skip: int = 0, limit: int = 100
) -> list[XRayPrediction]:
    query = select(XRayPrediction)
    if user_id is not None:
        query = query.where(XRayPrediction.user_id == user_id)
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return list(result.scalars().all())


async def get_prediction_by_id(db: AsyncSession, prediction_id: int) -> XRayPrediction | None:
    result = await db.execute(select(XRayPrediction).where(XRayPrediction.id == prediction_id))
    return result.scalar_one_or_none()


async def delete_prediction(db: AsyncSession, prediction_id: int) -> bool:
    prediction = await get_prediction_by_id(db, prediction_id)
    if prediction is None:
        return False
    file_path = os.path.join(settings.upload_dir, prediction.image_filename)
    await db.delete(prediction)
    await db.commit()
    if os.path.exists(file_path):
        os.remove(file_path)
    return True
