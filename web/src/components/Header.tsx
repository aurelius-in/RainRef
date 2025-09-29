import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../lib/api";

export default function Header() {
  const [ok, setOk] = useState<boolean | null>(null);
  const [who, setWho] = useState<any>(null);
  const env = (import.meta.env.MODE || 'dev').toUpperCase();
  const [scope, setScope] = useState<'Inbox'|'KB'|'Signals'>('Inbox');
  const [query, setQuery] = useState('');
  const navigate = useNavigate();
  const [theme, setTheme] = useState<string>(document.documentElement.getAttribute('data-theme') || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'));
  useEffect(() => {
    api.get("/healthz").then(() => setOk(true)).catch(() => setOk(false));
    api.get('/auth/whoami').then(r => setWho(r.data)).catch(()=>{});
  }, []);
  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    try { localStorage.setItem('rr_theme', theme); } catch {}
  }, [theme]);
  const dot = ok === null ? '#9ca3af' : ok ? '#22c55e' : '#ef4444';
  return (
    <>
      <header style={{ padding: 16, borderBottom: '1px solid var(--hair)', display: 'flex', gap: 12, alignItems: 'center', background: 'var(--bg)', color: 'var(--fg)', justifyContent: 'space-between' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <img src="/rr-white-trans.png" alt="RainRef" height={28} />
          <div style={{ display: 'flex', flexDirection: 'column' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
              <h1 style={{ margin: 0, fontSize: 20, fontWeight: 700 }}>RainRef</h1>
              <span style={{ width: 10, height: 10, borderRadius: 999, background: dot, display: 'inline-block' }} />
              <span aria-label="environment" style={{ border:'1px solid var(--hair)', padding:'2px 6px' }}>{env}</span>
            </div>
            <p style={{ margin: 0, fontSize: 12, opacity: 0.9 }}>The Ref for answers, safe actions, and clear signals.</p>
          </div>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <div style={{ display:'flex', gap:6 }}>
            <select aria-label="Scope" value={scope} onChange={e=>setScope(e.target.value as any)} style={{ background:'var(--panel)', border:'1px solid var(--hair)', color:'var(--fg)' }}>
              <option>Inbox</option>
              <option>KB</option>
              <option>Signals</option>
            </select>
            <input
              placeholder="Search"
              aria-label="Search"
              value={query}
              onChange={e=>setQuery(e.target.value)}
              onKeyDown={(e)=>{
                if (e.key === 'Enter') {
                  const q = encodeURIComponent(query.trim());
                  if (scope === 'Inbox') navigate(`/?q=${q}`);
                  else if (scope === 'KB') navigate(`/kb?q=${q}`);
                  else navigate(`/signals?q=${q}`);
                }
              }}
              style={{ background: 'var(--panel)', border: '1px solid var(--hair)', color: 'var(--fg)', padding: '6px 8px' }}
            />
          </div>
          <button onClick={()=>setTheme(theme==='dark'?'light':'dark')} aria-label="Toggle theme" style={{ background:'var(--panel)', border:'1px solid var(--hair)', color:'var(--fg)', padding:'6px 8px' }}>{theme==='dark'?'Light':'Dark'}</button>
          <div style={{ fontSize: 12, opacity: 0.9 }}>User: {who?.user || 'anonymous'}</div>
        </div>
      </header>
      <div className="ref-stripes" aria-hidden="true" style={{ height: 8 }} />
    </>
  );
}
