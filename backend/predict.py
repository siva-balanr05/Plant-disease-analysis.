from __future__ import annotations

import torch
import torch.nn.functional as F
from PIL import Image
from transformers import AutoImageProcessor, AutoModelForImageClassification

TOP_K = 5


def run_inference(
    image: Image.Image,
    processor: AutoImageProcessor,
    model: AutoModelForImageClassification,
    device: torch.device,
) -> dict[str, object]:
    inputs = processor(images=image, return_tensors="pt")
    inputs = {key: value.to(device) for key, value in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)

    logits = outputs.logits
    probabilities = F.softmax(logits, dim=-1)[0]

    top_k_values, top_k_indices = torch.topk(probabilities, k=TOP_K)

    id2label = model.config.id2label
    top_label = id2label[int(top_k_indices[0].item())]

    top_k: dict[str, float] = {}
    for score, index in zip(top_k_values, top_k_indices):
        label = _format_label(id2label[int(index.item())])
        top_k[label] = round(float(score.item()), 4)

    return {
        "disease": _format_label(top_label),
        "confidence": round(float(top_k_values[0].item()), 4),
        "top_k": top_k,
    }


def _format_label(raw: str) -> str:
    cleaned = raw.replace("___", " - ").replace("_", " ")
    return " ".join(word.capitalize() for word in cleaned.split())
