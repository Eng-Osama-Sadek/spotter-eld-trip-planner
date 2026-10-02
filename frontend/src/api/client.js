import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export const api = axios.create({
  baseURL: API_URL,
  timeout: 60000
});

export const planTrip = (payload) => api.post("/api/trips/plan/", payload);
