# Offline Plant Disease Detection System

A production-ready full-stack system for plant disease detection using a Hugging Face image classification model, FastAPI backend, React web dashboard, and Flutter mobile client.

## Prerequisites

- Python 3.10+
- Node.js 18+
- Flutter 3+

## Backend Setup

```bash
cd backend
pip install -r requirements.txt
python main.py
```

Model auto-downloads on first run and is cached in `../models/plant_model/`.

## Frontend Setup

```bash
cd frontend
npm install
npm start
```

## Flutter Setup

```bash
cd mobile_app
flutter pub get
flutter run
```

Change `baseUrl` in `lib/services/api_service.dart` for physical device testing.

## API Reference

- `POST http://localhost:8000/predict`
  - Body: form-data, key=`file`, value=`<image>`
  - Response: `{ disease, confidence, timestamp, prediction_id, top_k }`
- `GET http://localhost:8000/history?limit=20`
- `GET http://localhost:8000/health`
- `GET http://localhost:8000/model-info`

## Offline Mode

After first run, model is saved to `models/plant_model/`.
The app works fully offline on subsequent runs.
