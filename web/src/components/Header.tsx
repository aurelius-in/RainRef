import { useEffect, useState } from "react";
import { api } from "../lib/api";

export default function Header() {
  const [ok, setOk] = useState<boolean | null>(null);
  useEffect(() => {
    api.get("/healthz").then(() => setOk(true)).catch(() => setOk(false));
  }, []);
  const dot = ok === null ? '#9ca3af' : ok ? '#22c55e' : '#ef4444';
  return (
    <header style={{ padding: 16, borderBottom: '1px solid #e5e7eb', display: 'flex', gap: 12, alignItems: 'center', background: '#0a2540', color: 'white' }}>
      <img src="/rr-white-trans.png" alt="RainRef" height={28} />
      <div style={{ display: 'flex', flexDirection: 'column' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <h1 style={{ margin: 0, fontSize: 20, fontWeight: 700 }}>RainRef</h1>
          <span style={{ width: 10, height: 10, borderRadius: 999, background: dot, display: 'inline-block' }} />
        </div>
        <p style={{ margin: 0, fontSize: 12, opacity: 0.9 }}>The Ref for answers, safe actions, and clear signals.</p>
      </div>
    </header>
  );
}
