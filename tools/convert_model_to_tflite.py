#!/usr/bin/env python3
"""Convert a local Hugging Face image classification model to TensorFlow Lite.

Usage:
  python tools/convert_model_to_tflite.py

Optional:
  python tools/convert_model_to_tflite.py \
    --model-dir models/plant_model \
    --output-tflite mobile_app/assets/models/plant_disease.tflite \
    --output-labels mobile_app/assets/models/labels.txt

Requirements (install in your Python env):
  pip install tensorflow transformers safetensors
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import tensorflow as tf
from transformers import AutoConfig, TFAutoModelForImageClassification


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert HF model to TFLite")
    parser.add_argument(
        "--model-dir",
        type=Path,
        default=Path("models/plant_model"),
        help="Path to local Hugging Face model directory",
    )
    parser.add_argument(
        "--output-tflite",
        type=Path,
        default=Path("mobile_app/assets/models/plant_disease.tflite"),
        help="Path to write .tflite model",
    )
    parser.add_argument(
        "--output-labels",
        type=Path,
        default=Path("mobile_app/assets/models/labels.txt"),
        help="Path to write class labels txt",
    )
    parser.add_argument(
        "--output-meta",
        type=Path,
        default=Path("mobile_app/assets/models/model_meta.json"),
        help="Path to write preprocessing metadata json",
    )
    return parser.parse_args()


def write_labels(config: AutoConfig, output_labels: Path) -> None:
    output_labels.parent.mkdir(parents=True, exist_ok=True)
    id2label = {int(k): v for k, v in config.id2label.items()}
    ordered = [id2label[i] for i in sorted(id2label)]
    output_labels.write_text("\n".join(ordered) + "\n", encoding="utf-8")


def write_meta(model_dir: Path, config: AutoConfig, output_meta: Path) -> None:
    preproc_path = model_dir / "preprocessor_config.json"
    preproc = {}
    if preproc_path.exists():
        preproc = json.loads(preproc_path.read_text(encoding="utf-8"))

    image_size = int(getattr(config, "image_size", 224) or 224)
    meta = {
        "input_size": image_size,
        "image_mean": preproc.get("image_mean", [0.5, 0.5, 0.5]),
        "image_std": preproc.get("image_std", [0.5, 0.5, 0.5]),
        "rescale_factor": preproc.get("rescale_factor", 1 / 255.0),
        "num_classes": int(getattr(config, "num_labels", 0) or 0),
    }

    output_meta.parent.mkdir(parents=True, exist_ok=True)
    output_meta.write_text(json.dumps(meta, indent=2), encoding="utf-8")


def main() -> None:
    args = parse_args()

    model_dir = args.model_dir
    if not model_dir.exists():
        raise FileNotFoundError(f"Model directory not found: {model_dir}")

    config = AutoConfig.from_pretrained(str(model_dir), local_files_only=True)

    print("Loading TF model from local PyTorch weights...")
    model = TFAutoModelForImageClassification.from_pretrained(
        str(model_dir),
        from_pt=True,
        local_files_only=True,
    )

    input_size = int(getattr(config, "image_size", 224) or 224)

    @tf.function(
        input_signature=[
            tf.TensorSpec(
                shape=[1, input_size, input_size, 3],
                dtype=tf.float32,
                name="pixel_values",
            )
        ]
    )
    def serving(pixel_values: tf.Tensor) -> dict[str, tf.Tensor]:
        outputs = model(pixel_values=pixel_values, training=False)
        return {"logits": outputs.logits}

    concrete = serving.get_concrete_function()

    print("Converting to TFLite...")
    converter = tf.lite.TFLiteConverter.from_concrete_functions([concrete], model)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    tflite_model = converter.convert()

    args.output_tflite.parent.mkdir(parents=True, exist_ok=True)
    args.output_tflite.write_bytes(tflite_model)

    write_labels(config, args.output_labels)
    write_meta(model_dir, config, args.output_meta)

    print(f"Wrote TFLite model: {args.output_tflite}")
    print(f"Wrote labels: {args.output_labels}")
    print(f"Wrote meta: {args.output_meta}")


if __name__ == "__main__":
    main()
