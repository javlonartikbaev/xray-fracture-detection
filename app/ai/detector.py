import io
from dataclasses import dataclass

import numpy as np
from PIL import Image


@dataclass
class DetectionResult:
    fracture_detected: bool
    confidence: float
    details: str


class FractureDetector:
    def __init__(self):
        self._model_loaded = True  # Mock model always ready

    def predict(self, image_bytes: bytes) -> DetectionResult:
        """
        Analyze X-ray image for fractures.
        Uses image analysis heuristics for demonstration.
        In production, replace with a trained ML model.
        """
        try:
            img = Image.open(io.BytesIO(image_bytes)).convert("L")
            img_array = np.array(img, dtype=np.float32)

            # Heuristic analysis of image properties
            std_intensity = float(np.std(img_array))

            # Normalize to derive a confidence score
            # These thresholds simulate model behavior
            normalized_std = min(std_intensity / 128.0, 1.0)
            confidence = round(0.5 + (normalized_std - 0.5) * 0.6, 3)
            confidence = max(0.1, min(0.99, confidence))

            fracture_detected = confidence > 0.5
            details = "fracture indicators detected" if fracture_detected else "no fracture detected"

            return DetectionResult(
                fracture_detected=fracture_detected,
                confidence=confidence,
                details=details,
            )
        except Exception as e:
            return DetectionResult(
                fracture_detected=False,
                confidence=0.0,
                details=f"analysis error: {str(e)}",
            )


detector = FractureDetector()
