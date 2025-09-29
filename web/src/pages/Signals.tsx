import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import Spinner from "../components/Spinner";
import { api } from "../lib/api";

export default function Signals() {
  const [params] = useSearchParams();
  const [items, setItems] = useState<any[] | null>(null);
  const [tab, setTab] = useState<'stream'|'themes'>('stream');
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const limit = 10;
  useEffect(() => {
    setItems(null);
    api.get("/signals", { params: { page, limit } }).then(r => { setItems(r.data.items || []); setTotal(r.data.total || 0); }).catch(() => setItems([]));
  }, [page, params]);
  return (
    <div>
      <header style={{ display:'flex', alignItems:'center', justifyContent:'space-between' }}>
        <h2>Signals</h2>
        <div style={{ display:'flex', gap:8 }}>
          <button onClick={()=>setTab('stream')} aria-pressed={tab==='stream'}>Stream</button>
          <button onClick={()=>setTab('themes')} aria-pressed={tab==='themes'}>Themes</button>
        </div>
      </header>
      <section className="ref-plate" style={{ margin: '12px 0' }}>
        <div style={{ display:'flex', gap:12, color:'var(--muted)' }}>
          <div><strong>Bugs</strong>: —</div>
          <div><strong>Frictions</strong>: —</div>
          <div><strong>Features</strong>: —</div>
          <div><strong>Pricing</strong>: —</div>
          <div><strong>Churn</strong>: —</div>
        </div>
      </section>
      {tab==='stream' ? (
        items === null ? <Spinner /> : (
          <>
            <ul>
              {items
                ?.filter(s => {
                  const q = (params.get('q')||'').toLowerCase();
                  if (!q) return true;
                  return (s.type||'').toLowerCase().includes(q) || (s.origin||'').toLowerCase().includes(q);
                })
                .map(s => (<li key={s.id} style={{ borderBottom:'1px solid var(--hair)', padding:'6px 0' }}>{s.type} — {s.origin}</li>))}
            </ul>
            <div style={{ display: 'flex', gap: 8 }}>
              <button onClick={() => setPage(p => Math.max(1, p - 1))} disabled={page === 1}>Prev</button>
              <span>Page {page} / {Math.max(1, Math.ceil(total / limit))}</span>
              <button onClick={() => setPage(p => p + 1)} disabled={page >= Math.ceil(total / limit)}>Next</button>
            </div>
          </>
        )
      ) : (
        <div className="ref-stripes" style={{ padding: 24 }}>
          <div className="ref-plate" style={{ maxWidth: 520 }}>
            <h3 style={{ marginTop:0 }}>Themes</h3>
            <p style={{ color:'var(--muted)' }}>Grouped clusters will appear here as signals accumulate.</p>
          </div>
        </div>
      )}
    </div>
  );
}
