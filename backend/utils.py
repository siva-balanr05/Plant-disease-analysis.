from __future__ import annotations

import json
import uuid
from datetime import UTC, datetime
from io import BytesIO
from pathlib import Path
from typing import Any

from PIL import Image, UnidentifiedImageError

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}
ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/jpg"}
MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024
PREDICTION_LOG_PATH = Path("logs/predictions.jsonl")


def validate_image_file(filename: str, content_type: str | None, size: int) -> None:
    extension = Path(filename).suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError("Unsupported file extension. Allowed: .jpg, .jpeg, .png")

    if content_type is None or content_type.lower() not in ALLOWED_CONTENT_TYPES:
        raise ValueError("Unsupported content type. Allowed: image/jpeg, image/png")

    if size > MAX_FILE_SIZE_BYTES:
        raise ValueError("File too large. Maximum allowed size is 5MB")


def open_and_validate_image(raw_bytes: bytes) -> Image.Image:
    try:
        image = Image.open(BytesIO(raw_bytes))
        image.load()
        return image.convert("RGB")
    except (UnidentifiedImageError, OSError, ValueError) as exc:
        raise ValueError("Invalid or corrupt image file") from exc


def log_prediction(
    filename: str,
    disease: str,
    confidence: float,
    top_k_scores: dict[str, float],
) -> str:
    prediction_id = str(uuid.uuid4())
    record: dict[str, Any] = {
        "id": prediction_id,
        "timestamp": datetime.now(UTC).isoformat(),
        "filename": filename,
        "disease": disease,
        "confidence": confidence,
        "top_scores": top_k_scores,
    }

    PREDICTION_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with PREDICTION_LOG_PATH.open("a", encoding="utf-8") as file_handle:
        file_handle.write(json.dumps(record) + "\n")

    return prediction_id


def read_prediction_history(limit: int = 50) -> list[dict[str, Any]]:
    if not PREDICTION_LOG_PATH.exists():
        return []

    records: list[dict[str, Any]] = []
    with PREDICTION_LOG_PATH.open("r", encoding="utf-8") as file_handle:
        for line in file_handle:
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                continue

    return list(reversed(records[-limit:]))
