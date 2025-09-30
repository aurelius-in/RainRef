import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../lib/api";

export default function Header() {
  const [ok, setOk] = useState<boolean | null>(null);
  const [who, setWho] = useState<any>(null);
  // environment badge removed to avoid confusion in UI
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
  const dot = ok === null ? 'transparent' : ok ? 'transparent' : 'transparent';
  return (
    <>
      <header style={{ padding: 16, borderBottom: '1px solid var(--hair)', display: 'flex', gap: 12, alignItems: 'center', background: 'var(--bg)', color: 'var(--fg)', justifyContent: 'space-between' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <img src={theme === 'dark' ? "/rr-white-trans.png" : "/rr-black-trans.png"} alt="RainRef" height={28} />
          <div style={{ display: 'flex', flexDirection: 'column' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8 }} />
            <p style={{ margin: 0, fontSize: 12, opacity: 0.9 }}>The Ref for answers, safe actions, and clear signals.</p>
          </div>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
            <div style={{ display:'flex', gap:6 }}>
              <input
                placeholder="Search"
                aria-label="Search"
                value={query}
                onChange={e=>setQuery(e.target.value)}
                onKeyDown={(e)=>{
                  if (e.key === 'Enter') {
                    const q = encodeURIComponent(query.trim());
                    navigate(`/?q=${q}`);
                  }
                }}
                style={{ background: 'var(--panel)', border: '1px solid var(--hair)', color: 'var(--fg)', padding: '6px 8px', minWidth: 260 }}
              />
            </div>
          <button onClick={()=>setTheme(theme==='dark'?'light':'dark')} aria-label="Toggle theme" style={{ background:'var(--panel)', border:'1px solid var(--hair)', color:'var(--fg)', padding:'6px 8px' }}>{theme==='dark' ? '🌙' : '☀️'}</button>
          <div style={{ fontSize: 12, opacity: 0.9 }}>User: {who?.sub || 'Admin'}</div>
        </div>
      </header>
      <div className="ref-stripes" aria-hidden="true" style={{ height: 8 }} />
    </>
  );
}
