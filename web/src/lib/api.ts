import axios from "axios";
import { showToast } from "./toast";

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8080",
  timeout: 8000,
});

api.interceptors.response.use(
  (r) => r,
  (err) => {
    const status = err?.response?.status;
    const msg = typeof err?.response?.data === 'string' ? err.response.data : (err?.response?.data?.detail || 'Request failed');
    showToast(`Error ${status || ''} ${msg}`.trim());
    console.error("API error", status, err?.response?.data);
    return Promise.reject(err);
  }
);
