import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../lib/api";

export default function Settings() {
  const [details, setDetails] = useState<any>(null);
  const [info, setInfo] = useState<any>(null);
  const [cfg, setCfg] = useState<any>(null);
  const [tags, setTags] = useState<string[]>([]);
  useEffect(() => {
    api.get("/healthz/details").then(r => setDetails(r.data)).catch(() => setDetails({ ok: false }));
    api.get("/info").then(r => setInfo(r.data)).catch(() => setInfo({ version: "?", git_sha: "?", env: "dev" }));
    api.get("/config").then(r => setCfg(r.data)).catch(() => setCfg({ allowed_origins: [], env: "dev" }));
    api.get("/kb/tags").then(r => setTags(r.data.tags || [])).catch(() => setTags([]));
  }, []);
  const clearLocal = () => { try { localStorage.clear(); alert("Local data cleared."); } catch {} };
  return (
    <div>
      <h2>Settings</h2>
      <div>API base URL: {import.meta.env.VITE_API_URL || "http://localhost:8080"}</div>
      <div>Version: {info?.version} ({info?.git_sha}) â€” env: {info?.env}</div>
      <div>Allowed Origins: {(cfg?.allowed_origins||[]).join(", ")}</div>
      <div><a href="/docs" target="_blank">API Docs</a> Â· <a href="/openapi.json" target="_blank">OpenAPI</a> Â· <Link to="/metrics">Metrics</Link></div>
      <button onClick={clearLocal}>Clear Local Storage</button>
      <h3>Health</h3>
      <pre>{JSON.stringify(details, null, 2)}</pre>
      <h3>KB Tags</h3>
      <div>{tags.map(t => <span key={t} style={{border:'1px solid #e5e7eb',padding:'2px 6px',borderRadius:6,marginRight:6}}>{t}</span>)}</div>
    </div>
  );
}
