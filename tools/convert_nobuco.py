#!/usr/bin/env python3
"""Convert PyTorch MobileNetV2 plant disease model to TFLite via nobuco (PyTorch→Keras)."""

import os
os.environ["TF_USE_LEGACY_KERAS"] = "1"

import json
import shutil
from pathlib import Path

import numpy as np
import torch
import tensorflow as tf
from transformers import AutoConfig, AutoModelForImageClassification

import nobuco
from nobuco import ChannelOrder, ChannelOrderingStrategy


def main():
    model_dir = Path("models/plant_model")
    output_tflite = Path("mobile_app/assets/models/plant_disease.tflite")
    output_labels = Path("mobile_app/assets/models/labels.txt")

    config = AutoConfig.from_pretrained(str(model_dir), local_files_only=True)

    print("Loading PyTorch model...")
    pt_model = AutoModelForImageClassification.from_pretrained(
        str(model_dir), local_files_only=True
    )
    pt_model.eval()

    # Wrap model to return only logits tensor (nobuco needs plain tensors)
    class LogitsWrapper(torch.nn.Module):
        def __init__(self, model):
            super().__init__()
            self.model = model

        def forward(self, pixel_values):
            return self.model(pixel_values=pixel_values).logits

    wrapper = LogitsWrapper(pt_model)
    wrapper.eval()

    dummy_input = torch.randn(1, 3, 224, 224)

    print("Converting PyTorch → Keras via nobuco...")
    keras_model = nobuco.pytorch_to_keras(
        wrapper,
        args=[dummy_input],
        inputs_channel_order=ChannelOrder.PYTORCH,
        outputs_channel_order=ChannelOrder.PYTORCH,
    )

    # Verify Keras model output matches PyTorch
    with torch.no_grad():
        pt_out = wrapper(dummy_input).numpy()
    tf_input = np.transpose(dummy_input.numpy(), (0, 2, 3, 1))  # NCHW → NHWC
    keras_out = keras_model(tf_input).numpy()
    diff = np.max(np.abs(pt_out - keras_out))
    print(f"Max output difference (PT vs Keras): {diff:.6f}")

    # Convert to TFLite
    print("Converting Keras → TFLite...")
    converter = tf.lite.TFLiteConverter.from_keras_model(keras_model)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    tflite_model = converter.convert()

    output_tflite.parent.mkdir(parents=True, exist_ok=True)
    output_tflite.write_bytes(tflite_model)
    print(f"TFLite model: {output_tflite} ({output_tflite.stat().st_size / 1e6:.1f} MB)")

    # Write labels
    id2label = {int(k): v for k, v in config.id2label.items()}
    ordered = [id2label[i] for i in sorted(id2label)]
    output_labels.parent.mkdir(parents=True, exist_ok=True)
    output_labels.write_text("\n".join(ordered) + "\n", encoding="utf-8")
    print(f"Labels: {output_labels} ({len(ordered)} classes)")
    print("Done!")


if __name__ == "__main__":
    main()
