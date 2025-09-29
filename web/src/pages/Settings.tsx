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
  const [adapterName, setAdapterName] = useState('zendesk');
  const [adapterPayload, setAdapterPayload] = useState<string>(`{\n  "subject": "Test from RainRef",\n  "body": "Hello",\n  "priority": "normal"\n}`);
  const [adapterResult, setAdapterResult] = useState<string>('');
  const [adapterCfg, setAdapterCfg] = useState<any>({
    zendesk_base_url: '', zendesk_token: '',
    intercom_base_url: '', intercom_token: '',
    github_repo: '', github_token: ''
  });
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
        <div className="ref-plate" style={{ marginBottom: 12 }}>
          <h4 style={{ marginTop:0 }}>Adapter Test (admin)</h4>
          <div style={{ display:'flex', gap:8, alignItems:'center', marginBottom:8 }}>
            <label>
              <span className="sr-only">Adapter name</span>
              <select aria-label="Adapter name" value={adapterName} onChange={e=>setAdapterName(e.target.value)}>
                <option value="zendesk">zendesk</option>
                <option value="intercom">intercom</option>
                <option value="github">github</option>
              </select>
            </label>
            <button onClick={async()=>{
              try {
                const payload = JSON.parse(adapterPayload || '{}');
                const r = await api.post('/adapters/test', { name: adapterName, payload });
                setAdapterResult(JSON.stringify(r.data, null, 2));
              } catch (e:any) {
                const msg = e?.response?.data?.detail || e?.message || 'failed';
                setAdapterResult(String(msg));
              }
            }}>Test</button>
          </div>
          <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:12 }}>
            <label>
              <div style={{ marginBottom:6 }}>Payload (JSON)</div>
              <textarea value={adapterPayload} onChange={e=>setAdapterPayload(e.target.value)} aria-label="Adapter payload"
                        style={{ width:'100%', minHeight:140, fontFamily:'monospace', background:'var(--panel)', color:'var(--fg)', border:'1px solid var(--hair)', borderRadius:6, padding:8 }}/>
            </label>
            <label>
              <div style={{ marginBottom:6 }}>Result</div>
              <pre className="code-block" style={{ minHeight:140 }}>{adapterResult || '—'}</pre>
            </label>
          </div>
        </div>
        {who?.role === 'admin' && (
          <div className="ref-plate" style={{ marginBottom: 12 }}>
            <h4 style={{ marginTop:0 }}>Adapter Settings</h4>
            <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:12 }}>
              <label>
                <div>Zendesk Base URL</div>
                <input value={adapterCfg.zendesk_base_url || ''} onChange={e=>setAdapterCfg((s:any)=>({...s, zendesk_base_url: e.target.value}))} />
              </label>
              <label>
                <div>Zendesk Token</div>
                <input type="password" value={adapterCfg.zendesk_token || ''} onChange={e=>setAdapterCfg((s:any)=>({...s, zendesk_token: e.target.value}))} />
              </label>
              <label>
                <div>Intercom Base URL</div>
                <input value={adapterCfg.intercom_base_url || ''} onChange={e=>setAdapterCfg((s:any)=>({...s, intercom_base_url: e.target.value}))} />
              </label>
              <label>
                <div>Intercom Token</div>
                <input type="password" value={adapterCfg.intercom_token || ''} onChange={e=>setAdapterCfg((s:any)=>({...s, intercom_token: e.target.value}))} />
              </label>
              <label>
                <div>GitHub Repo (owner/name)</div>
                <input value={adapterCfg.github_repo || ''} onChange={e=>setAdapterCfg((s:any)=>({...s, github_repo: e.target.value}))} />
              </label>
              <label>
                <div>GitHub Token</div>
                <input type="password" value={adapterCfg.github_token || ''} onChange={e=>setAdapterCfg((s:any)=>({...s, github_token: e.target.value}))} />
              </label>
            </div>
            <div style={{ display:'flex', gap:8, marginTop:12 }}>
              <button onClick={async()=>{
                try {
                  const r = await api.get('/admin/adapters/config');
                  setAdapterCfg(r.data || {});
                  setMessage('Loaded adapter settings');
                } catch (e:any) {
                  setMessage(`Load failed: ${e?.response?.data?.detail || e?.message}`);
                }
              }}>Load</button>
              <button onClick={async()=>{
                try {
                  await api.post('/admin/adapters/config', adapterCfg);
                  setMessage('Saved adapter settings');
                } catch (e:any) {
                  setMessage(`Save failed: ${e?.response?.data?.detail || e?.message}`);
                }
              }}>Save</button>
              <div aria-live="polite" style={{ color:'var(--muted)' }}>{message}</div>
            </div>
          </div>
        )}
        <h3>Health</h3>
        <pre>{JSON.stringify(details, null, 2)}</pre>
        <h3>KB Tags</h3>
        <div>{tags.map(t => <span key={t} className="ref-plate" style={{marginRight:6}}>{t}</span>)}</div>
      </main>
    </div>
  );
}
