import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../lib/api";

export default function Settings() {
  const [details, setDetails] = useState<any>(null);
  const [info, setInfo] = useState<any>(null);
  const [cfg, setCfg] = useState<any>(null);
  const [limits, setLimits] = useState<any>(null);
  const [tags, setTags] = useState<string[]>([]);
  const [loginState, setLoginState] = useState({ username: 'admin', password: 'admin' });
  const [who, setWho] = useState<any>(null);
  useEffect(() => {
    api.get("/healthz/details").then(r => setDetails(r.data)).catch(() => setDetails({ ok: false }));
    api.get("/info").then(r => setInfo(r.data)).catch(() => setInfo({ version: "?", git_sha: "?", env: "dev" }));
    api.get("/config").then(r => setCfg(r.data)).catch(() => setCfg({ allowed_origins: [], env: "dev" }));
    api.get("/config/limits").then(r => setLimits(r.data)).catch(() => setLimits({}));
    api.get("/kb/tags").then(r => setTags(r.data.tags || [])).catch(() => setTags([]));
    api.get('/auth/whoami').then(r => setWho(r.data)).catch(()=>{});
  }, []);
  const clearLocal = () => { try { localStorage.clear(); alert("Local data cleared."); } catch {} };
  return (
    <div style={{ display:'grid', gridTemplateColumns:'280px 1fr', gap:16 }}>
      <aside className="ref-stripes" style={{ padding: 12 }}>
        <div className="ref-plate">
          <h3 style={{ marginTop:0 }}>Sections</h3>
          <ul>
            <li>Integrations</li>
            <li>Roles &amp; Permissions</li>
            <li>Org Profile</li>
            <li>Data Retention</li>
            <li>BYO-LLM</li>
            <li>Region</li>
          </ul>
        </div>
      </aside>
      <main>
        <h2>Settings</h2>
        <div>API base URL: {import.meta.env.VITE_API_URL || "http://localhost:8080"}</div>
        <div>Version: {info?.version} ({info?.git_sha}) — env: {info?.env}</div>
        <div>Allowed Origins: {(cfg?.allowed_origins||[]).join(", ")}</div>
        <div>Rate Limits: window {limits?.rate_limit_window_sec}s, per-window {limits?.rate_limit_per_window}</div>
        <div><a href="/docs" target="_blank">API Docs</a> · <a href="/openapi.json" target="_blank">OpenAPI</a> · <Link to="/metrics">Metrics</Link></div>
        <button onClick={clearLocal}>Clear Local Storage</button>
        <h3>Auth</h3>
        <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
          <input placeholder="username" value={loginState.username} onChange={e=>setLoginState(s=>({...s, username: e.target.value}))} />
          <input placeholder="password" type="password" value={loginState.password} onChange={e=>setLoginState(s=>({...s, password: e.target.value}))} />
          <button onClick={async ()=>{
            const r = await api.post('/auth/login', loginState);
            localStorage.setItem('rr_token', r.data.access_token);
            const w = await api.get('/auth/whoami');
            setWho(w.data);
          }}>Login</button>
          <button onClick={()=>{ localStorage.removeItem('rr_token'); setWho(null); }}>Logout</button>
        </div>
        <div><strong>Who am I</strong>: <code>{JSON.stringify(who)}</code></div>
        <h3>Integrations</h3>
        <div className="ref-plate" style={{ marginBottom: 12 }}>
          <div>Zendesk configured: {String(cfg?.adapters?.zendesk)}</div>
          <div>Intercom configured: {String(cfg?.adapters?.intercom)}</div>
          <div>GitHub configured: {String(cfg?.adapters?.github)}</div>
          <div style={{ color:'var(--muted)' }}>Set ZENDESK_BASE_URL/TOKEN, INTERCOM_BASE_URL/TOKEN, GITHUB_REPO/TOKEN.</div>
        </div>
        <h3>Health</h3>
        <pre>{JSON.stringify(details, null, 2)}</pre>
        <h3>KB Tags</h3>
        <div>{tags.map(t => <span key={t} className="ref-plate" style={{marginRight:6}}>{t}</span>)}</div>
      </main>
    </div>
  );
}
