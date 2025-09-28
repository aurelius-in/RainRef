import axios from "axios";
import { showToast } from "./toast";

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8080",
  timeout: 8000,
});

api.interceptors.request.use((config) => {
  const rid = `req-${Math.random().toString(36).slice(2, 10)}`;
  config.headers = config.headers || {};
  (config.headers as any)['X-Request-ID'] = rid;
  return config;
});

api.interceptors.response.use(
  (r) => r,
  (err) => {
    const status = err?.response?.status;
    const msg = typeof err?.response?.data === 'string' ? err.response.data : (err?.response?.data?.detail || 'Request failed');
    const rid = err?.response?.headers?.['x-request-id'];
    if (rid) {
      showToast(`Request ${rid}: ${msg}`);
    } else {
      showToast(`Error ${status || ''} ${msg}`.trim());
    }
    console.error("API error", status, err?.response?.data, rid);
    return Promise.reject(err);
  }
);
