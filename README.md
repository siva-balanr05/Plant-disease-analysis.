# Offline Plant Disease Analysis

Full-stack plant disease detection system with:

- FastAPI backend
- React web frontend
- Flutter mobile app
- Hugging Face image classification model

## Features

- Disease prediction from leaf images
- Confidence score and top-k predictions
- Prediction history logging
- Web and mobile clients
- Disease-specific recommendation tips on the web result page

## Project Structure

```text
plant-disease-system/
  backend/
  frontend/
  mobile_app/
  models/
```

## Requirements

- Python 3.10+
- Node.js 18+
- Flutter 3+
- Android SDK (for Android emulator/device testing)

## 1. Run Backend

```bash
cd backend
pip install -r requirements.txt
python main.py
```

Backend runs on:

- http://localhost:8000

### Backend API Endpoints

- GET /health
- GET /model-info
- GET /history?limit=20
- POST /predict

Example predict request:

- Method: POST
- URL: http://localhost:8000/predict
- Content-Type: multipart/form-data
- Field name: file

## 2. Run Frontend (React)

```bash
cd frontend
npm install
npm start
```

Frontend runs on:

- http://localhost:3000

Frontend API base URL is configured to:

- http://localhost:8000

## 3. Run Mobile App (Flutter)

```bash
cd mobile_app
flutter pub get
flutter run
```

For a specific device:

```bash
flutter devices
flutter run -d <device_id>
```

### Mobile API Base URL Logic

Configured in mobile app service layer:

- Android emulator: http://10.0.2.2:8000
- iOS simulator: http://127.0.0.1:8000
- Web/Desktop: http://localhost:8000

## Prediction Output Format

Response payload from /predict:

```json
{
  "disease": "Tomato With Late Blight",
  "confidence": 0.58,
  "timestamp": "2026-04-08T07:52:00.758941+00:00",
  "prediction_id": "2f6260b4-7af3-4256-8334-700b182c36a7",
  "top_k": {
    "Tomato With Late Blight": 0.58,
    "Tomato With Early Blight": 0.2561
  }
}
```

## Logs and History

- Predictions are stored in backend logs as JSONL.
- Log path: backend/logs/predictions.jsonl

## Offline Model Notes

- Model files are stored in models/plant_model
- After initial availability, app can run without internet for inference

## Common Troubleshooting

### Prediction failed from frontend

- Ensure backend is running on port 8000
- Verify frontend API base URL points to http://localhost:8000

### Flutter camera or gallery permission denied

- Reinstall app on emulator/device after manifest or permission logic changes
- Open app settings and grant Camera/Photos if previously denied

### Android emulator cannot connect to backend

- Use http://10.0.2.2:8000 from Android emulator
- Confirm backend is running and health endpoint is reachable

## Development Notes

- Keep heavy/generated folders out of git (node_modules, build outputs)
- Keep model binary artifacts out of git when possible
