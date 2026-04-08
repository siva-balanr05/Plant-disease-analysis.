#!/usr/bin/env python3
"""Convert PyTorch MobileNetV2 plant disease model to TFLite via manual weight transfer."""

import os
os.environ["TF_USE_LEGACY_KERAS"] = "1"

from pathlib import Path

import numpy as np
import torch
import tensorflow as tf
from transformers import AutoConfig, AutoModelForImageClassification


def get_pt_weights(state_dict, prefix):
    """Extract conv weight + BN params for a given HF MobileNetV2 layer prefix."""
    conv_w = state_dict[f"{prefix}.convolution.weight"].numpy()
    bn_gamma = state_dict[f"{prefix}.normalization.weight"].numpy()
    bn_beta = state_dict[f"{prefix}.normalization.bias"].numpy()
    bn_mean = state_dict[f"{prefix}.normalization.running_mean"].numpy()
    bn_var = state_dict[f"{prefix}.normalization.running_var"].numpy()
    return conv_w, bn_gamma, bn_beta, bn_mean, bn_var


def set_conv_bn_weights(tf_conv_layer, tf_bn_layer, conv_w, bn_gamma, bn_beta, bn_mean, bn_var, is_depthwise=False):
    """Set weights on a TF Conv2D/DepthwiseConv2D + BatchNormalization pair."""
    if is_depthwise:
        # PyTorch depthwise: [ch, 1, kH, kW] → TF: [kH, kW, ch, 1]
        tf_w = np.transpose(conv_w, (2, 3, 0, 1))
    else:
        # PyTorch Conv2D: [out, in, kH, kW] → TF: [kH, kW, in, out]
        tf_w = np.transpose(conv_w, (2, 3, 1, 0))

    tf_conv_layer.set_weights([tf_w])
    tf_bn_layer.set_weights([bn_gamma, bn_beta, bn_mean, bn_var])


def main():
    model_dir = Path("models/plant_model")
    output_tflite = Path("mobile_app/assets/models/plant_disease.tflite")
    output_labels = Path("mobile_app/assets/models/labels.txt")

    config = AutoConfig.from_pretrained(str(model_dir), local_files_only=True)

    # Load PyTorch model
    print("Loading PyTorch model...")
    pt_model = AutoModelForImageClassification.from_pretrained(
        str(model_dir), local_files_only=True
    )
    pt_model.eval()
    sd = pt_model.state_dict()

    # Create TF Keras MobileNetV2
    print("Creating TF Keras MobileNetV2...")
    base_model = tf.keras.applications.MobileNetV2(
        input_shape=(224, 224, 3),
        include_top=False,
        weights=None,
        alpha=1.0,
    )

    # Build full model with classifier
    inputs = tf.keras.Input(shape=(224, 224, 3))
    x = base_model(inputs, training=False)
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    outputs = tf.keras.layers.Dense(38, name="classifier")(x)
    tf_model = tf.keras.Model(inputs, outputs)

    # Build layer name lookup
    layer_dict = {layer.name: layer for layer in base_model.layers}

    print("Transferring weights...")

    # ── Stem: first conv ──
    # HF: conv_stem.first_conv → Keras: Conv1 + bn_Conv1
    conv_w, bn_g, bn_b, bn_m, bn_v = get_pt_weights(sd, "mobilenet_v2.conv_stem.first_conv")
    set_conv_bn_weights(layer_dict["Conv1"], layer_dict["bn_Conv1"],
                        conv_w, bn_g, bn_b, bn_m, bn_v, is_depthwise=False)

    # ── Stem: depthwise 3x3 ──
    # HF: conv_stem.conv_3x3 → Keras: expanded_conv_depthwise + expanded_conv_depthwise_BN
    conv_w, bn_g, bn_b, bn_m, bn_v = get_pt_weights(sd, "mobilenet_v2.conv_stem.conv_3x3")
    set_conv_bn_weights(layer_dict["expanded_conv_depthwise"], layer_dict["expanded_conv_depthwise_BN"],
                        conv_w, bn_g, bn_b, bn_m, bn_v, is_depthwise=True)

    # ── Stem: reduce 1x1 ──
    # HF: conv_stem.reduce_1x1 → Keras: expanded_conv_project + expanded_conv_project_BN
    conv_w, bn_g, bn_b, bn_m, bn_v = get_pt_weights(sd, "mobilenet_v2.conv_stem.reduce_1x1")
    set_conv_bn_weights(layer_dict["expanded_conv_project"], layer_dict["expanded_conv_project_BN"],
                        conv_w, bn_g, bn_b, bn_m, bn_v, is_depthwise=False)

    # ── Inverted residual blocks: layer.0 → block_1, ..., layer.15 → block_16 ──
    for i in range(16):
        block_idx = i + 1
        pt_prefix = f"mobilenet_v2.layer.{i}"
        keras_prefix = f"block_{block_idx}"

        # Expand 1x1
        conv_w, bn_g, bn_b, bn_m, bn_v = get_pt_weights(sd, f"{pt_prefix}.expand_1x1")
        set_conv_bn_weights(
            layer_dict[f"{keras_prefix}_expand"],
            layer_dict[f"{keras_prefix}_expand_BN"],
            conv_w, bn_g, bn_b, bn_m, bn_v, is_depthwise=False,
        )

        # Depthwise 3x3
        conv_w, bn_g, bn_b, bn_m, bn_v = get_pt_weights(sd, f"{pt_prefix}.conv_3x3")
        set_conv_bn_weights(
            layer_dict[f"{keras_prefix}_depthwise"],
            layer_dict[f"{keras_prefix}_depthwise_BN"],
            conv_w, bn_g, bn_b, bn_m, bn_v, is_depthwise=True,
        )

        # Project/reduce 1x1
        conv_w, bn_g, bn_b, bn_m, bn_v = get_pt_weights(sd, f"{pt_prefix}.reduce_1x1")
        set_conv_bn_weights(
            layer_dict[f"{keras_prefix}_project"],
            layer_dict[f"{keras_prefix}_project_BN"],
            conv_w, bn_g, bn_b, bn_m, bn_v, is_depthwise=False,
        )

    # ── Final 1x1 conv ──
    # HF: conv_1x1 → Keras: Conv_1 + Conv_1_bn
    conv_w, bn_g, bn_b, bn_m, bn_v = get_pt_weights(sd, "mobilenet_v2.conv_1x1")
    set_conv_bn_weights(layer_dict["Conv_1"], layer_dict["Conv_1_bn"],
                        conv_w, bn_g, bn_b, bn_m, bn_v, is_depthwise=False)

    # ── Classifier ──
    clf_w = sd["classifier.weight"].numpy()  # [38, 1280]
    clf_b = sd["classifier.bias"].numpy()    # [38]
    # PyTorch Dense [out, in] → TF Dense [in, out]
    for layer in tf_model.layers:
        if layer.name == "classifier":
            layer.set_weights([clf_w.T, clf_b])
            break

    print("All weights transferred!")

    # ── Validate: compare outputs ──
    print("Validating output match...")
    dummy_np = np.random.randn(1, 3, 224, 224).astype(np.float32)
    # Normalize like the preprocessing pipeline: (x / 255 - 0.5) / 0.5 → already in [-1, 1] range
    # For validation, just use raw random data

    # PyTorch forward
    with torch.no_grad():
        pt_input = torch.from_numpy(dummy_np)
        pt_out = pt_model(pixel_values=pt_input).logits.numpy()

    # TF forward (convert NCHW → NHWC)
    tf_input = np.transpose(dummy_np, (0, 2, 3, 1))
    tf_out = tf_model(tf_input, training=False).numpy()

    max_diff = np.max(np.abs(pt_out - tf_out))
    mean_diff = np.mean(np.abs(pt_out - tf_out))
    print(f"Max output difference: {max_diff:.6f}")
    print(f"Mean output difference: {mean_diff:.6f}")

    if max_diff > 1.0:
        print("WARNING: Large output difference detected! Model may not be accurate.")
    else:
        print("Output validation passed!")

    # ── Convert to TFLite via SavedModel ──
    print("Saving as SavedModel...")
    saved_model_dir = "temp_saved_model"
    tf.saved_model.save(tf_model, saved_model_dir)

    print("Converting SavedModel to TFLite...")
    converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_dir)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    tflite_model = converter.convert()

    output_tflite.parent.mkdir(parents=True, exist_ok=True)
    output_tflite.write_bytes(tflite_model)
    size_mb = output_tflite.stat().st_size / 1e6
    print(f"TFLite model: {output_tflite} ({size_mb:.1f} MB)")

    # Cleanup SavedModel
    import shutil
    shutil.rmtree(saved_model_dir, ignore_errors=True)

    # ── Write labels ──
    id2label = {int(k): v for k, v in config.id2label.items()}
    ordered = [id2label[i] for i in sorted(id2label)]
    output_labels.parent.mkdir(parents=True, exist_ok=True)
    output_labels.write_text("\n".join(ordered) + "\n", encoding="utf-8")
    print(f"Labels: {output_labels} ({len(ordered)} classes)")

    print("Done!")


if __name__ == "__main__":
    main()
