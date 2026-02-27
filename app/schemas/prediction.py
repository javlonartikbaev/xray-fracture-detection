from datetime import datetime
from pydantic import BaseModel


class PredictionResponse(BaseModel):
    id: int
    user_id: int
    image_filename: str
    original_filename: str
    fracture_detected: bool
    confidence: float
    body_part: str | None = None
    notes: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class PredictionCreate(BaseModel):
    user_id: int
    body_part: str | None = None
    notes: str | None = None
