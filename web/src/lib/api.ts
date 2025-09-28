import axios from "axios";
export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8080",
});

api.interceptors.response.use(
  (r) => r,
  (err) => {
    console.error("API error", err?.response?.status, err?.response?.data);
    return Promise.reject(err);
  }
);
