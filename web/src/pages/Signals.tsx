import { useEffect, useMemo, useState } from "react";
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

  const metrics = useMemo(() => {
    const counts: Record<string, number> = { bug: 0, friction: 0, feature: 0, pricing: 0, churn: 0 };
    (items||[]).forEach((s:any) => {
      const t = String(s.type||'').toLowerCase();
      if (t.includes('bug')) counts.bug++;
      else if (t.includes('friction')) counts.friction++;
      else if (t.includes('feature')) counts.feature++;
      else if (t.includes('pricing')) counts.pricing++;
      else if (t.includes('churn')) counts.churn++;
    });
    return counts;
  }, [items]);

  const themes = useMemo(() => {
    // Simple grouping by type keyword with sample origins
    const groups: Record<string, { count:number, examples:string[] }> = {};
    (items||[]).forEach((s:any) => {
      const t = String(s.type||'').toLowerCase();
      let key = 'other';
      if (t.includes('bug')) key = 'bugs';
      else if (t.includes('friction')) key = 'frictions';
      else if (t.includes('feature')) key = 'features';
      else if (t.includes('pricing')) key = 'pricing';
      else if (t.includes('churn')) key = 'churn';
      if (!groups[key]) groups[key] = { count: 0, examples: [] };
      groups[key].count += 1;
      const ex = String(s.origin||'').slice(0, 48);
      if (ex && !groups[key].examples.includes(ex)) {
        groups[key].examples.push(ex);
        if (groups[key].examples.length > 3) groups[key].examples.pop();
      }
    });
    return groups;
  }, [items]);
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
          <div><strong>Bugs</strong>: {metrics.bug}</div>
          <div><strong>Frictions</strong>: {metrics.friction}</div>
          <div><strong>Features</strong>: {metrics.feature}</div>
          <div><strong>Pricing</strong>: {metrics.pricing}</div>
          <div><strong>Churn</strong>: {metrics.churn}</div>
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
          <div className="ref-plate" style={{ maxWidth: 640 }}>
            <h3 style={{ marginTop:0 }}>Themes</h3>
            {!items?.length ? (
              <p style={{ color:'var(--muted)' }}>No signals yet.</p>
            ) : (
              <ul>
                {Object.entries(themes).map(([k,v]) => (
                  <li key={k} style={{ marginBottom:8 }}>
                    <strong style={{ textTransform:'capitalize' }}>{k}</strong> — {v.count}
                    {v.examples.length ? (
                      <div style={{ color:'var(--muted)' }}>e.g., {v.examples.join('; ')}</div>
                    ) : null}
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
