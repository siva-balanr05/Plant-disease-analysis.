import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000",
  timeout: 30000,
});

export async function predictDisease(imageFile) {
  const formData = new FormData();
  formData.append("file", imageFile);

  const response = await api.post("/predict", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  return response.data;
}

export async function getHistory(limit = 20) {
  const response = await api.get(`/history?limit=${limit}`);
  return response.data.predictions;
}

export async function checkHealth() {
  const response = await api.get("/health");
  return response.data;
}
