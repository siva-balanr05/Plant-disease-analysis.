#!/usr/bin/env python3
"""Convert PyTorch MobileNetV2 plant disease model to TFLite via ONNX."""

import json
import shutil
from pathlib import Path

# Fix numpy pickle restriction before importing onnx2tf
import numpy as np
_np_load_orig = np.load
def _np_load_allow_pickle(*args, **kwargs):
    kwargs["allow_pickle"] = True
    return _np_load_orig(*args, **kwargs)
np.load = _np_load_allow_pickle

import torch
from transformers import AutoConfig, AutoModelForImageClassification


def main():
    model_dir = Path("models/plant_model")
    output_tflite = Path("mobile_app/assets/models/plant_disease.tflite")
    output_labels = Path("mobile_app/assets/models/labels.txt")
    onnx_path = Path("temp_plant_disease.onnx")
    tf_output_dir = Path("temp_tf_output")

    # Load config
    config = AutoConfig.from_pretrained(str(model_dir), local_files_only=True)

    # Load PyTorch model
    print("Loading PyTorch model...")
    model = AutoModelForImageClassification.from_pretrained(
        str(model_dir), local_files_only=True
    )
    model.eval()

    # Export to ONNX
    print("Exporting to ONNX...")
    dummy_input = torch.randn(1, 3, 224, 224)
    torch.onnx.export(
        model,
        dummy_input,
        str(onnx_path),
        opset_version=13,
        input_names=["pixel_values"],
        output_names=["logits"],
    )
    print(f"ONNX model saved: {onnx_path} ({onnx_path.stat().st_size / 1e6:.1f} MB)")

    # Verify ONNX
    import onnx

    onnx_model = onnx.load(str(onnx_path))
    onnx.checker.check_model(onnx_model)
    print("ONNX model verified OK")

    # Create custom test data to avoid onnx2tf downloading corrupt test images
    test_data_dir = Path("temp_test_data")
    test_data_dir.mkdir(exist_ok=True)
    dummy_npy = test_data_dir / "pixel_values.npy"
    np.save(str(dummy_npy), np.random.randn(1, 3, 224, 224).astype(np.float32))

    # Convert ONNX to TFLite using onnx2tf
    print("Converting ONNX → TFLite via onnx2tf...")
    import onnx2tf
    import onnx2tf.onnx2tf as _onnx2tf_mod
    import onnx2tf.utils.common_functions as _cf

    # Patch broken test data download at both module levels
    _dummy_test = lambda: np.random.randn(20, 224, 224, 3).astype(np.float32)
    _cf.download_test_image_data = _dummy_test
    _onnx2tf_mod.download_test_image_data = _dummy_test

    onnx2tf.convert(
        input_onnx_file_path=str(onnx_path),
        output_folder_path=str(tf_output_dir),
        non_verbose=True,
        custom_input_op_name_np_data_path=[["pixel_values", str(dummy_npy)]],
    )

    # Copy the float32 tflite model to assets
    src = tf_output_dir / "model_float32.tflite"
    if not src.exists():
        # onnx2tf may name it differently
        candidates = list(tf_output_dir.glob("*.tflite"))
        if candidates:
            src = candidates[0]
        else:
            raise FileNotFoundError(f"No .tflite file found in {tf_output_dir}")

    output_tflite.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, output_tflite)
    print(
        f"TFLite model: {output_tflite} ({output_tflite.stat().st_size / 1e6:.1f} MB)"
    )

    # Write labels
    id2label = {int(k): v for k, v in config.id2label.items()}
    ordered = [id2label[i] for i in sorted(id2label)]
    output_labels.parent.mkdir(parents=True, exist_ok=True)
    output_labels.write_text("\n".join(ordered) + "\n", encoding="utf-8")
    print(f"Labels: {output_labels} ({len(ordered)} classes)")

    # Cleanup temp files
    onnx_path.unlink(missing_ok=True)
    if tf_output_dir.exists():
        shutil.rmtree(tf_output_dir, ignore_errors=True)
    print("Done! Temp files cleaned up.")


if __name__ == "__main__":
    main()
