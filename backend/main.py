from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from datetime import UTC, datetime
from typing import Any, AsyncIterator

import uvicorn
from fastapi import FastAPI, File, HTTPException, Query, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from model_loader import LOCAL_MODEL_DIR, MODEL_NAME, get_model, load_model
from predict import run_inference
from utils import (
    log_prediction,
    open_and_validate_image,
    read_prediction_history,
    validate_image_file,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    try:
        load_model()
        logger.info("Model loaded successfully")
    except Exception:
        logger.exception("Failed to load model during startup")
    yield
    logger.info("Offline Plant Disease Detection API shutting down")


app = FastAPI(title="Offline Plant Disease Detection System", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class PredictionResponse(BaseModel):
    disease: str
    confidence: float
    timestamp: str
    prediction_id: str
    top_k: dict[str, float]


class HistoryResponse(BaseModel):
    predictions: list[dict[str, Any]]
    total: int


@app.post("/predict", response_model=PredictionResponse)
async def predict(file: UploadFile = File(...)) -> PredictionResponse:
    try:
        raw_bytes = await file.read()
        validate_image_file(file.filename or "uploaded_image.jpg", file.content_type, len(raw_bytes))

        image = open_and_validate_image(raw_bytes)
        processor, model, device = get_model()

        inference_result = run_inference(image, processor, model, device)
        prediction_id = log_prediction(
            filename=file.filename or "uploaded_image.jpg",
            disease=str(inference_result["disease"]),
            confidence=float(inference_result["confidence"]),
            top_k_scores=dict(inference_result["top_k"]),
        )

        return PredictionResponse(
            disease=str(inference_result["disease"]),
            confidence=float(inference_result["confidence"]),
            timestamp=datetime.now(UTC).isoformat(),
            prediction_id=prediction_id,
            top_k=dict(inference_result["top_k"]),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Unexpected error during prediction")
        raise HTTPException(status_code=500, detail="Internal server error") from exc


@app.get("/history", response_model=HistoryResponse)
async def history(limit: int = Query(default=50, ge=1, le=200)) -> HistoryResponse:
    predictions = read_prediction_history(limit)
    return HistoryResponse(predictions=predictions, total=len(predictions))


@app.get("/health")
async def health() -> dict[str, Any]:
    model_loaded = True
    device_name = "unknown"

    try:
        _, _, device = get_model()
        device_name = str(device)
    except RuntimeError:
        model_loaded = False

    return {"status": "ok", "model_loaded": model_loaded, "device": device_name}


@app.get("/model-info")
async def model_info() -> dict[str, Any]:
    try:
        _, model, device = get_model()
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    return {
        "model_name": MODEL_NAME,
        "num_classes": int(model.config.num_labels),
        "device": str(device),
        "offline_mode": (LOCAL_MODEL_DIR / "config.json").exists(),
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
