import { useEffect, useState } from "react";
import { api } from "../lib/api";

export default function Settings() {
  const [rlWindow, setRlWindow] = useState(60);
  const [rlPer, setRlPer] = useState(100);
  const [requireJwt, setRequireJwt] = useState(true);
  const [useRedis, setUseRedis] = useState(true);
  const [stripesOn, setStripesOn] = useState(true);
  const [compactTables, setCompactTables] = useState(false);
  useEffect(() => {
    document.documentElement.setAttribute('data-stripes', stripesOn ? 'on' : 'off');
  }, [stripesOn]);
  return (
    <div style={{ display:'grid', gridTemplateColumns:'280px 1fr', gap:16 }}>
      <aside className="ref-stripes" style={{ padding: 12 }}>
        <div className="ref-plate">
          <h3 style={{ marginTop:0, textAlign:'center', textDecoration:'underline' }}>Settings</h3>
          <ul style={{ margin:0, paddingLeft:16 }}>
            <li>Security</li>
            <li>RateLimit</li>
            <li>Display</li>
          </ul>
        </div>
      </aside>
      <main>
        <section className="ref-plate" style={{ marginBottom:12 }}>
          <h4 style={{ marginTop:0, textAlign:'center', textDecoration:'underline' }}>Security</h4>
          <label style={{ display:'flex', alignItems:'center', gap:8 }}>
            <input type="checkbox" checked={requireJwt} onChange={e=>setRequireJwt(e.currentTarget.checked)} />
            <span>Require JWT for admin</span>
          </label>
          <label style={{ display:'flex', alignItems:'center', gap:8 }}>
            <input type="checkbox" checked={useRedis} onChange={e=>setUseRedis(e.currentTarget.checked)} />
            <span>Redis limiter</span>
          </label>
        </section>
        <section className="ref-plate" style={{ marginBottom:12 }}>
          <h4 style={{ marginTop:0, textAlign:'center', textDecoration:'underline' }}>RateLimit</h4>
          <div style={{ display:'flex', gap:12, alignItems:'center' }}>
            <label>
              <div>Window (s)</div>
              <input type="number" min={1} max={600} value={rlWindow} onChange={e=>setRlWindow(parseInt(e.target.value||'0')||0)} style={{ width:100 }} />
            </label>
            <label>
              <div>Per-Window</div>
              <input type="number" min={1} max={1000} value={rlPer} onChange={e=>setRlPer(parseInt(e.target.value||'0')||0)} style={{ width:100 }} />
            </label>
          </div>
        </section>
        <section className="ref-plate" style={{ marginBottom:12 }}>
          <h4 style={{ marginTop:0, textAlign:'center', textDecoration:'underline' }}>Display</h4>
          <label style={{ display:'flex', alignItems:'center', gap:8 }}>
            <input type="checkbox" checked={stripesOn} onChange={e=>setStripesOn(e.currentTarget.checked)} />
            <span>Stripes</span>
          </label>
          <label style={{ display:'flex', alignItems:'center', gap:8 }}>
            <input type="checkbox" checked={compactTables} onChange={e=>setCompactTables(e.currentTarget.checked)} />
            <span>Compact tables</span>
          </label>
        </section>
      </main>
    </div>
  );
}
