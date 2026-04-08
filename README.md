# Plant Disease Detection System — Edge AI

An end-to-end plant disease detection system that identifies **38 plant diseases** from leaf images using a MobileNetV2 deep learning model. The system includes a FastAPI backend, a React web frontend, and a **fully offline Flutter mobile app** with on-device TFLite inference.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [System Architecture](#system-architecture)
3. [Technology Stack](#technology-stack)
4. [ML Model Details](#ml-model-details)
5. [Supported Diseases (38 Classes)](#supported-diseases-38-classes)
6. [Project Structure](#project-structure)
7. [Setup & Installation](#setup--installation)
8. [API Reference](#api-reference)
9. [Mobile App — Offline Inference](#mobile-app--offline-inference)
10. [Disease Solutions Engine](#disease-solutions-engine)
11. [Model Conversion Pipeline](#model-conversion-pipeline)
12. [Screenshots & Workflow](#screenshots--workflow)
13. [Troubleshooting](#troubleshooting)
14. [Future Enhancements](#future-enhancements)

---

## Project Overview

Plant diseases cause significant crop losses worldwide. Early and accurate identification is critical for timely intervention. This project provides a practical solution by combining deep learning with a multi-platform application that works both online (web) and **completely offline (mobile)**.

### Key Highlights

- **Offline-first mobile app** — runs ML inference directly on the phone without any server
- **38-class classification** covering major crop diseases across apple, tomato, potato, grape, corn, citrus, and more
- **Disease-specific treatment recommendations** displayed alongside predictions
- **Lightweight model** — only 2.5 MB TFLite model suitable for low-end Android devices
- **Full-stack web platform** with FastAPI backend and React frontend

---

## System Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                    Plant Disease Detection System             │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────┐    REST API    ┌─────────────────────────┐  │
│  │   React      │◄────────────►│   FastAPI Backend        │  │
│  │   Frontend   │   Port 3000   │   Port 8000              │  │
│  │   (Tailwind) │               │   - /predict             │  │
│  │              │               │   - /history             │  │
│  │   Disease    │               │   - /health              │  │
│  │   Solutions  │               │   - /model-info          │  │
│  └─────────────┘               │                           │  │
│                                 │   PyTorch + Transformers  │  │
│                                 │   MobileNetV2 Inference   │  │
│                                 └─────────────────────────┘  │
│                                                              │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │   Flutter Mobile App (Fully Offline)                    │ │
│  │                                                         │ │
│  │   ┌──────────────┐  ┌────────────────────────────────┐  │ │
│  │   │ Image Picker  │  │  TFLite Interpreter            │  │ │
│  │   │ (Camera/      │──│  - plant_disease.tflite (2.5MB)│  │ │
│  │   │  Gallery)     │  │  - 38 class labels             │  │ │
│  │   └──────────────┘  │  - On-device preprocessing      │  │ │
│  │                      │  - Softmax + Top-K ranking      │  │ │
│  │   ┌──────────────┐  └────────────────────────────────┘  │ │
│  │   │ Disease       │                                     │ │
│  │   │ Solutions     │  Treatment recommendations          │ │
│  │   │ Engine        │  for all 38 classes                 │ │
│  │   └──────────────┘                                     │ │
│  └─────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```

---

## Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| ML Model | MobileNetV2 (HuggingFace) | Image classification (38 classes) |
| Backend | Python 3.12, FastAPI, Uvicorn | REST API, model inference |
| ML Framework | PyTorch, Transformers | Model loading and prediction |
| Web Frontend | React 18, Tailwind CSS | User interface |
| Mobile App | Flutter 3.x, Dart | Cross-platform mobile app |
| On-device ML | TensorFlow Lite (tflite_flutter) | Offline inference on Android |
| Model Format | .safetensors (PyTorch), .tflite (mobile) | Model storage |
| Image Processing | Pillow (backend), image package (Flutter) | Preprocessing |

---

## ML Model Details

| Property | Value |
|----------|-------|
| Architecture | MobileNetV2 1.0 224 |
| Source | `linkanjarad/mobilenet_v2_1.0_224-plant-disease-identification` |
| Input Size | 224 × 224 × 3 (RGB) |
| Normalization | (pixel / 255.0 − 0.5) / 0.5 → range [−1, 1] |
| Output | 38-class softmax probabilities |
| Parameters | 2,272,550 |
| PyTorch Model Size | ~9 MB (.safetensors) |
| TFLite Model Size | **2.5 MB** (quantized) |
| Inference | Real-time on modern smartphones |

---

## Supported Diseases (38 Classes)

| # | Class Name |
|---|-----------|
| 0 | Apple Scab |
| 1 | Apple with Black Rot |
| 2 | Cedar Apple Rust |
| 3 | Healthy Apple |
| 4 | Healthy Blueberry Plant |
| 5 | Cherry with Powdery Mildew |
| 6 | Healthy Cherry Plant |
| 7 | Corn (Maize) with Cercospora and Gray Leaf Spot |
| 8 | Corn (Maize) with Common Rust |
| 9 | Corn (Maize) with Northern Leaf Blight |
| 10 | Healthy Corn (Maize) Plant |
| 11 | Grape with Black Rot |
| 12 | Grape with Esca (Black Measles) |
| 13 | Grape with Isariopsis Leaf Spot |
| 14 | Healthy Grape Plant |
| 15 | Orange with Citrus Greening |
| 16 | Peach with Bacterial Spot |
| 17 | Healthy Peach Plant |
| 18 | Bell Pepper with Bacterial Spot |
| 19 | Healthy Bell Pepper Plant |
| 20 | Potato with Early Blight |
| 21 | Potato with Late Blight |
| 22 | Healthy Potato Plant |
| 23 | Healthy Raspberry Plant |
| 24 | Healthy Soybean Plant |
| 25 | Squash with Powdery Mildew |
| 26 | Strawberry with Leaf Scorch |
| 27 | Healthy Strawberry Plant |
| 28 | Tomato with Bacterial Spot |
| 29 | Tomato with Early Blight |
| 30 | Tomato with Late Blight |
| 31 | Tomato with Leaf Mold |
| 32 | Tomato with Septoria Leaf Spot |
| 33 | Tomato with Spider Mites or Two-spotted Spider Mite |
| 34 | Tomato with Target Spot |
| 35 | Tomato Yellow Leaf Curl Virus |
| 36 | Tomato Mosaic Virus |
| 37 | Healthy Tomato Plant |

---

## Project Structure

```
plant-disease-system/
├── backend/
│   ├── main.py                  # FastAPI app with endpoints
│   ├── predict.py               # PyTorch inference pipeline
│   ├── model_loader.py          # Model & processor loading
│   ├── utils.py                 # Helper utilities
│   ├── requirements.txt         # Python dependencies
│   └── logs/
│       └── predictions.jsonl    # Prediction history log
│
├── frontend/
│   ├── package.json
│   ├── tailwind.config.js
│   ├── public/
│   │   └── index.html
│   └── src/
│       ├── App.jsx              # Main React app
│       ├── index.css            # Tailwind styles
│       ├── components/
│       │   ├── Navbar.jsx
│       │   ├── ImageUploader.jsx
│       │   ├── ResultCard.jsx
│       │   └── HistoryList.jsx
│       ├── pages/
│       │   ├── Home.jsx
│       │   ├── Upload.jsx
│       │   └── Result.jsx       # Shows prediction + solutions
│       ├── data/
│       │   └── diseaseSolutions.js  # Treatment recommendations
│       └── services/
│           └── api.js           # Axios API client
│
├── mobile_app/
│   ├── pubspec.yaml
│   ├── assets/
│   │   └── models/
│   │       ├── plant_disease.tflite  # 2.5 MB TFLite model
│   │       └── labels.txt            # 38 class labels
│   └── lib/
│       ├── main.dart
│       ├── data/
│       │   └── disease_solutions.dart  # Treatment recommendations
│       ├── screens/
│       │   ├── home_screen.dart        # Camera/gallery + model status
│       │   └── result_screen.dart      # Prediction + solutions display
│       ├── services/
│       │   ├── api_service.dart        # HTTP client (optional online mode)
│       │   └── model_service.dart      # TFLite on-device inference
│       └── widgets/
│           ├── image_picker_widget.dart
│           └── result_card_widget.dart
│
├── models/
│   └── plant_model/
│       ├── config.json              # Model configuration
│       ├── model.safetensors        # PyTorch weights
│       └── preprocessor_config.json # Image preprocessing config
│
├── tools/
│   ├── convert_model_to_tflite.py   # HF → TFLite (TF-based)
│   ├── convert_weights.py           # PyTorch → TF Keras → TFLite (used)
│   ├── convert_via_onnx.py          # PyTorch → ONNX → TFLite (alt)
│   └── convert_nobuco.py            # PyTorch → Keras via nobuco (alt)
│
└── README.md
```

---

## Setup & Installation

### Prerequisites

- Python 3.10+
- Node.js 18+
- Flutter 3.x with Android SDK
- Git

### 1. Backend (FastAPI)

```bash
cd plant-disease-system/backend
pip install -r requirements.txt
python main.py
```

Backend starts at **http://localhost:8000**

### 2. Frontend (React)

```bash
cd plant-disease-system/frontend
npm install
npm start
```

Frontend starts at **http://localhost:3000**

### 3. Mobile App (Flutter)

For development on emulator:

```bash
cd plant-disease-system/mobile_app
flutter pub get
flutter run
```

To build a release APK:

```bash
flutter build apk --release
```

Output: `mobile_app/build/app/outputs/flutter-apk/app-release.apk`

---

## API Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check — returns `{"status": "ok"}` |
| `/model-info` | GET | Model metadata (name, classes, input size) |
| `/predict` | POST | Upload leaf image, returns disease prediction |
| `/history?limit=20` | GET | Recent prediction history from JSONL log |

### POST /predict — Example Response

```json
{
  "disease": "Tomato with Late Blight",
  "confidence": 0.9234,
  "timestamp": "2026-04-08T12:30:00.000000+00:00",
  "prediction_id": "2f6260b4-7af3-4256-8334-700b182c36a7",
  "top_k": {
    "Tomato with Late Blight": 0.9234,
    "Tomato with Early Blight": 0.0456,
    "Tomato with Septoria Leaf Spot": 0.0189,
    "Tomato with Target Spot": 0.0067,
    "Tomato with Bacterial Spot": 0.0031
  }
}
```

---

## Mobile App — Offline Inference

The Flutter mobile app runs **entirely offline** with no backend required:

1. **Model Loading** — TFLite model (2.5 MB) is bundled inside the APK as a Flutter asset
2. **Image Capture** — Camera or gallery selection with runtime permissions
3. **Preprocessing** — Image resized to 224×224, normalized to [−1, 1] range
4. **Inference** — `tflite_flutter` interpreter runs MobileNetV2 on-device
5. **Post-processing** — Softmax applied to logits, top-5 predictions ranked
6. **Solutions** — Disease-specific treatment recommendations displayed

### On-Device Inference Pipeline

```
Camera/Gallery Image
       ↓
  Decode & Resize (224 × 224)
       ↓
  Normalize: (pixel/255 − 0.5) / 0.5
       ↓
  TFLite Interpreter (MobileNetV2)
       ↓
  38-class Logits
       ↓
  Softmax → Top-5 Ranking
       ↓
  Disease Name + Confidence + Solution
```

### Key Technical Decisions

| Decision | Rationale |
|----------|-----------|
| MobileNetV2 | Lightweight (2.3M params), designed for mobile devices |
| TFLite quantization | Reduced model from ~9 MB to 2.5 MB |
| `rootBundle.load()` | Reliable Flutter asset loading vs `fromAsset()` |
| On-device inference | No internet needed, low latency, privacy-preserving |

---

## Disease Solutions Engine

Both web and mobile apps include a **disease solutions engine** that provides actionable treatment recommendations for every detected disease. Solutions are matched using keyword rules against the predicted disease name.

### Example Solutions

| Disease | Recommendation |
|---------|----------------|
| Late Blight | Remove infected leaves, avoid overhead watering, apply registered fungicide, rotate crops |
| Powdery Mildew | Prune canopy for airflow, remove white-growth leaves, apply sulfur fungicide, reduce nitrogen |
| Mosaic Virus | Remove infected plants (viral, not curable), control aphid vectors, disinfect tools |
| Healthy Plant | Maintain consistent watering, apply balanced fertilizer, weekly leaf inspection |

---

## Model Conversion Pipeline

The PyTorch model was converted to TFLite for mobile deployment:

```
PyTorch (HuggingFace MobileNetV2)
       ↓
  Load weights from .safetensors
       ↓
  Create equivalent TF Keras MobileNetV2
       ↓
  Transfer all 314 weight tensors (NCHW → NHWC)
       ↓
  Validate output match (max diff: 0.000004)
       ↓
  Export as SavedModel → TFLite with DEFAULT optimization
       ↓
  plant_disease.tflite (2.5 MB, float32 quantized)
```

The conversion script is at `tools/convert_weights.py`.

---

## Screenshots & Workflow

### Web Application
1. **Home Page** — Upload a leaf image via drag-and-drop or file picker
2. **Result Page** — Disease name, confidence %, top-5 predictions, and treatment solution

### Mobile Application
1. **Home Screen** — Offline model status indicator, camera/gallery buttons
2. **Result Screen** — Disease prediction, confidence bar, top-5 list, and solution card
3. **Fully Offline** — Works in airplane mode with no internet connection

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Frontend "Prediction failed" | Ensure backend is running on port 8000 |
| Mobile "Offline Model Not Available" | Rebuild APK after `flutter clean` to re-bundle assets |
| Camera not opening on phone | Grant camera permission in phone Settings → Apps |
| Gallery not working | Android uses system picker; no extra permission needed |
| Emulator can't reach backend | Use `10.0.2.2:8000` (Android emulator loopback) |

---

## Future Enhancements

- Add prediction history storage on mobile (SQLite)
- Support iOS deployment
- Implement multi-language support for disease solutions
- Add image cropping and leaf region detection
- Integrate weather-based disease risk alerts
- Export prediction reports as PDF

---

## License

This project is for educational and research purposes.

---

**Repository:** [github.com/siva-balanr05/Plant-disease-analysis](https://github.com/siva-balanr05/Plant-disease-analysis..git)
