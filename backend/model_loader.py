from __future__ import annotations

from pathlib import Path
from typing import Any, Tuple

import torch
from transformers import AutoImageProcessor, AutoModelForImageClassification

MODEL_NAME = "Daksh159/plant-disease-mobilenetv2"
FALLBACK_MODEL_NAME = "linkanjarad/mobilenet_v2_1.0_224-plant-disease-identification"
LOCAL_MODEL_DIR = Path("../models/plant_model")

_processor: Any = None
_model: AutoModelForImageClassification | None = None
_device: torch.device | None = None


def _resolve_model_source() -> str:
    if (LOCAL_MODEL_DIR / "config.json").exists():
        return str(LOCAL_MODEL_DIR)
    return MODEL_NAME


def load_model() -> Tuple[Any, AutoModelForImageClassification, torch.device]:
    global _processor, _model, _device

    if _processor is not None and _model is not None and _device is not None:
        return _processor, _model, _device

    model_source = _resolve_model_source()

    try:
        _processor = AutoImageProcessor.from_pretrained(model_source)
    except OSError:
        if model_source == str(LOCAL_MODEL_DIR):
            raise

        model_source = FALLBACK_MODEL_NAME
        _processor = AutoImageProcessor.from_pretrained(model_source)
    _model = AutoModelForImageClassification.from_pretrained(model_source)

    _device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    _model.to(_device)
    _model.eval()

    if model_source != str(LOCAL_MODEL_DIR):
        LOCAL_MODEL_DIR.mkdir(parents=True, exist_ok=True)
        _processor.save_pretrained(str(LOCAL_MODEL_DIR))
        _model.save_pretrained(str(LOCAL_MODEL_DIR))

    return _processor, _model, _device


def get_model() -> Tuple[Any, AutoModelForImageClassification, torch.device]:
    if _processor is None or _model is None or _device is None:
        raise RuntimeError("Model not loaded. Call load_model() first.")

    return _processor, _model, _device
