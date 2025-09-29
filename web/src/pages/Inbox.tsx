import { useEffect, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import Spinner from "../components/Spinner";
import { api } from "../lib/api";

export default function Inbox() {
  const [params] = useSearchParams();
  const [items, setItems] = useState<any[] | null>(null);
  const [order, setOrder] = useState<'asc' | 'desc'>('desc');
  const [source, setSource] = useState('');
  const [intent, setIntent] = useState('');
  const [severity, setSeverity] = useState('');
  const [product, setProduct] = useState('');
  const [assignee, setAssignee] = useState('');
  const [byChannel, setByChannel] = useState<any>({});
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const limit = 10;
  useEffect(() => {
    const q = (params.get('q')||'').toLowerCase();
    setItems(null);
    api.get("/ref/events", { params: { page, limit, order, channel: source } }).then(r => { setItems(r.data.items || []); setTotal(r.data.total || 0); }).catch(() => setItems([]));
    api.get("/ref/events/stats").then(r => setByChannel(r.data.by_channel || {})).catch(() => setByChannel({}));
  }, [page, order, source, params]);
  return (
    <div style={{ display: 'grid', gridTemplateRows: 'auto 1fr auto', gap: 12 }}>
      <div style={{ display:'flex', alignItems:'center', gap: 12 }}>
        <h2 style={{ margin: 0 }}>Inbox</h2>
        <div style={{display:'flex',gap:8}}>{Object.entries(byChannel||{}).map(([k,v]) => <span key={k} className="ref-plate">{k}: {v as any}</span>)}</div>
        <div style={{ marginLeft: 'auto', display:'flex', gap:8 }}>
          <label>
            <span className="sr-only">Order</span>
            <select value={order} onChange={e => setOrder(e.target.value as any)} aria-label="Order" style={{ background:'var(--panel)', border:'1px solid var(--hair)', color:'var(--fg)' }}>
              <option value="desc">Newest</option>
              <option value="asc">Oldest</option>
            </select>
          </label>
          <label>
            <span className="sr-only">Source</span>
            <select value={source} onChange={e => setSource(e.target.value)} aria-label="Source" style={{ background:'var(--panel)', border:'1px solid var(--hair)', color:'var(--fg)' }}>
              <option value="">All sources</option>
              {Object.keys(byChannel||{}).map(k => <option key={k} value={k}>{k}</option>)}
            </select>
          </label>
          <label>
            <span className="sr-only">Intent</span>
            <select value={intent} onChange={e => setIntent(e.target.value)} aria-label="Intent" style={{ background:'var(--panel)', border:'1px solid var(--hair)', color:'var(--fg)' }}>
              <option value="">Intent</option>
              <option>bug</option>
              <option>friction</option>
              <option>feature</option>
              <option>pricing</option>
              <option>churn</option>
            </select>
          </label>
          <label>
            <span className="sr-only">Severity</span>
            <select value={severity} onChange={e => setSeverity(e.target.value)} aria-label="Severity" style={{ background:'var(--panel)', border:'1px solid var(--hair)', color:'var(--fg)' }}>
              <option value="">Severity</option>
              <option>S1</option>
              <option>S2</option>
              <option>S3</option>
              <option>S4</option>
            </select>
          </label>
          <label>
            <span className="sr-only">Product</span>
            <input value={product} onChange={e=>setProduct(e.target.value)} placeholder="Product area" aria-label="Product area" style={{ background:'var(--panel)', border:'1px solid var(--hair)', color:'var(--fg)', padding:'6px 8px' }} />
          </label>
          <label>
            <span className="sr-only">Assignee</span>
            <input value={assignee} onChange={e=>setAssignee(e.target.value)} placeholder="Assignee" aria-label="Assignee" style={{ background:'var(--panel)', border:'1px solid var(--hair)', color:'var(--fg)', padding:'6px 8px' }} />
          </label>
        </div>
      </div>
      <div style={{ borderTop:'1px solid var(--hair)' }}>
        {items === null ? (
          <Spinner />
        ) : items.length === 0 ? (
          <div className="ref-stripes" style={{ padding: 24 }}>
            <div className="ref-plate" style={{ maxWidth: 480 }}>
              <h3 style={{ marginTop:0 }}>No items</h3>
              <p style={{ color:'var(--muted)' }}>You’re all caught up. New Ref Events will land here. Use filters to focus on a product area.</p>
            </div>
          </div>
        ) : (
          <table style={{ width:'100%', borderCollapse:'collapse' }}>
            <thead>
              <tr style={{ textAlign:'left', color:'var(--muted)' }}>
                <th>Source</th>
                <th>Intent</th>
                <th>Severity</th>
                <th>Title</th>
                <th>Product</th>
                <th>Age/SLA</th>
                <th>Assignee</th>
              </tr>
            </thead>
            <tbody>
              {items
                .filter(e => !intent || (e.intent||'').toLowerCase()===intent)
                .filter(e => !severity || (e.severity||'')===severity)
                .filter(e => !product || (e.product||'').toLowerCase().includes(product.toLowerCase()))
                .filter(e => !assignee || (e.assignee||'').toLowerCase().includes(assignee.toLowerCase()))
                .filter(e => {
                  const q = (params.get('q')||'').toLowerCase();
                  if (!q) return true;
                  return (e.text||'').toLowerCase().includes(q);
                })
                .map((e) => {
                  const intentChip = e.intent || '—';
                  const severityChip = e.severity || '—';
                  const productVal = e.product || '—';
                  const age = e.age || '—';
                  const sla = e.sla || '—';
                  const who = e.assignee || 'Unassigned';
                  return (
                    <tr key={e.id} style={{ borderBottom:'1px solid var(--hair)' }}>
                      <td style={{ whiteSpace:'nowrap', padding:'8px 6px' }}>{e.channel}</td>
                      <td style={{ padding:'8px 6px' }}>
                        <span style={{ border:'1px solid var(--hair)', padding:'2px 6px' }}>{intentChip}</span>
                      </td>
                      <td style={{ padding:'8px 6px' }}>
                        <span style={{ border:'1px solid var(--hair)', padding:'2px 6px' }}>{severityChip}</span>
                      </td>
                      <td style={{ padding:'8px 6px' }}>
                        <Link to={`/events/${e.id}`}>{e.text}</Link>
                      </td>
                      <td style={{ padding:'8px 6px' }}>{productVal}</td>
                      <td style={{ padding:'8px 6px' }}>{age} / {sla}</td>
                      <td style={{ padding:'8px 6px' }}>{who}</td>
                    </tr>
                  );
                })}
            </tbody>
          </table>
        )}
      </div>
      <div style={{ display: 'flex', gap: 8, alignItems:'center', justifyContent:'space-between', paddingTop: 8 }}>
        <label style={{ display:'flex', alignItems:'center', gap:6 }}>
          <input type="checkbox" aria-label="Compact mode" onChange={(e)=>{
            const root = document.querySelector('table tbody');
            if (!root) return;
            (root as HTMLElement).style.fontSize = e.currentTarget.checked ? '13px' : '';
          }} />
          <span style={{ color:'var(--muted)' }}>Compact</span>
        </label>
        <button onClick={() => setPage(p => Math.max(1, p - 1))} disabled={page === 1}>Prev</button>
        <span>Page {page} / {Math.max(1, Math.ceil(total / limit))}</span>
        <button onClick={() => setPage(p => p + 1)} disabled={page >= Math.ceil(total / limit)}>Next</button>
      </div>
    </div>
  );
}
