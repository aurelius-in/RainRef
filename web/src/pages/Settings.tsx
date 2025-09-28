import { useEffect, useState } from "react";
import { api } from "../lib/api";

export default function Settings() {
  const [details, setDetails] = useState<any>(null);
  const [info, setInfo] = useState<any>(null);
  useEffect(() => {
    api.get("/healthz/details").then(r => setDetails(r.data)).catch(() => setDetails({ ok: false }));
    api.get("/info").then(r => setInfo(r.data)).catch(() => setInfo({ version: "?", git_sha: "?" }));
  }, []);
  return (
    <div>
      <h2>Settings</h2>
      <div>API base URL: {import.meta.env.VITE_API_URL || "http://localhost:8080"}</div>
      <div>Version: {info?.version} ({info?.git_sha})</div>
      <h3>Health</h3>
      <pre>{JSON.stringify(details, null, 2)}</pre>
    </div>
  );
}
