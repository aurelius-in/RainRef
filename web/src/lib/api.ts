import axios from "axios";
import { showToast } from "./toast";

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8080",
  timeout: 8000,
});

// Attach a request id for tracing
api.interceptors.request.use((config) => {
  const rid = `req-${Math.random().toString(36).slice(2, 10)}`;
  config.headers = config.headers || {};
  (config.headers as any)['X-Request-ID'] = rid;
  const token = localStorage.getItem('rr_token');
  if (token) {
    (config.headers as any)['Authorization'] = `Bearer ${token}`;
  }
  return config;
});

// Error toasts with optional disable and 429 friendly message
api.interceptors.response.use(
  (r) => r,
  (err) => {
    const status = err?.response?.status;
    const msg = typeof err?.response?.data === 'string' ? err.response.data : (err?.response?.data?.detail || 'Request failed');
    const rid = err?.response?.headers?.['x-request-id'];
    const disableToasts = String(import.meta.env.VITE_DISABLE_TOASTS||'').toLowerCase() === 'true';
    if (!disableToasts) {
      // Suppress noisy 404s (empty states) from toasts; still reject for callers
      if (status === 404) {
        // no toast for 404 to avoid repeated noise on empty pages
      } else if (status === 429) {
        showToast('Take a beat — we throttled duplicate clicks.');
      } else if (rid) {
        showToast(`Request ${rid}: ${msg}`);
      } else {
        showToast(`Error ${status || ''} ${msg}`.trim());
      }
    }
    console.error("API error", status, err?.response?.data, rid);
    return Promise.reject(err);
  }
);

// Simple one-shot retry for GETs
api.interceptors.response.use(undefined, async (error) => {
  const config = error.config || {};
  const method = (config.method || 'get').toLowerCase();
  if (method === 'get' && !config._retried) {
    config._retried = true;
    return api.request(config);
  }
  throw error;
});
