import { useEffect, useMemo, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import Spinner from "../components/Spinner";
import { api } from "../lib/api";

export default function Events() {
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
  // Local mock data for offline/empty-state preview and pagination testing
  const cap = (s?: string) => s ? s.charAt(0).toUpperCase() + s.slice(1) : '';
  const MOCK_ITEMS = useMemo(() => {
    const base = [
      { channel: 'Support', intent: 'Bug', severity: 'High', product: 'Login', text: 'Bug: app crashes on login', assignee: 'Alex' },
      { channel: 'Support', intent: 'Friction', severity: 'Med', product: 'Activation', text: 'Activation link not received', assignee: 'Jamie' },
      { channel: 'Issues', intent: 'Feature', severity: 'Low', product: 'Settings', text: 'Feature: add export to CSV', assignee: 'Priya' },
      { channel: 'Tickets', intent: 'Pricing', severity: 'Low', product: 'Billing', text: 'Coupon not applied at checkout', assignee: 'Sam' },
      { channel: 'Support', intent: 'Churn', severity: 'High', product: 'Account', text: 'Cancel request due to repeated downtime', assignee: 'Taylor' },
    ];
    const arr: any[] = [];
    const rand = (min:number,max:number)=>Math.floor(Math.random()*(max-min+1))+min;
    for (let i = 0; i < 40; i++) {
      const t = base[i % base.length];
      arr.push({ id: `m-${i+1}`, ...t, created_at: new Date(Date.now()-i*60*60*1000).toISOString(), age: `${rand(1,7)}d`, sla: `${rand(1,24)}h` });
    }
    return arr;
  }, []);
  useEffect(() => {
    const q = (params.get('q')||'').toLowerCase();
    setItems(null);
    api.get("/ref/events", { params: { page, limit, order, channel: source } }).then(r => { setItems(r.data.items || []); setTotal(r.data.total || 0); }).catch(() => setItems([]));
    api.get("/ref/events/stats").then(r => setByChannel(r.data.by_channel || {})).catch(() => setByChannel({}));
  }, [page, order, source, params]);
  // Choose data source: server items when present; otherwise mock
  const dataSource = (items && items.length > 0) ? items : MOCK_ITEMS;
  const computedTotal = (items && items.length > 0) ? total : dataSource.length;

  return (
    <div style={{ display: 'grid', gridTemplateRows: 'auto 1fr auto', gap: 12 }}>
      <div style={{ display:'flex', alignItems:'center', gap: 12 }}>
        <div className="chip-sections">
          <div className="chip-section" role="group" aria-label="Order">
            <span className="icon" role="img" aria-label="Order" title="Order">
              <svg viewBox="0 0 24 24" aria-hidden="true">
                <path d="M12 4L8 8h8l-4-4zM12 20l4-4H8l4 4z" />
              </svg>
            </span>
            <span className="chip" role="button" aria-pressed={order==='desc'} onClick={()=>setOrder('desc')}>Newest</span>
            <span className="chip" role="button" aria-pressed={order==='asc'} onClick={()=>setOrder('asc')}>Oldest</span>
          </div>
          <div className="chip-section" role="group" aria-label="Severity">
            <span className="icon" role="img" aria-label="Severity" title="Severity">
              <svg viewBox="0 0 24 24" aria-hidden="true">
                <path d="M12 3l9 16H3l9-16z" />
                <path d="M12 9v5M12 18h.01" />
              </svg>
            </span>
            <span className="chip" role="button" aria-pressed={!severity} onClick={()=>setSeverity('')}>All</span>
            {[
              {k:'high', label:'High'},
              {k:'medium', label:'Med'},
              {k:'low', label:'Low'},
            ].map(s => (
              <span key={s.k} className="chip" role="button" aria-pressed={severity===s.k} onClick={()=>setSeverity(s.k)}>{s.label}</span>
            ))}
          </div>
          <div className="chip-section full-row" role="group" aria-label="Intent">
            <span className="icon" role="img" aria-label="Intent" title="Intent">
              <svg viewBox="0 0 24 24" aria-hidden="true">
                <circle cx="12" cy="12" r="8" />
                <circle cx="12" cy="12" r="3" />
              </svg>
            </span>
            <span className="chip" role="button" aria-pressed={!intent} onClick={()=>setIntent('')}>All</span>
            {['Bug','Friction','Feature','Pricing','Churn'].map((i)=> (
              <span key={i} className="chip" role="button" aria-pressed={intent.toLowerCase()===i.toLowerCase()} onClick={()=>setIntent(i.toLowerCase())}>{i}</span>
            ))}
          </div>
        </div>
      </div>
      <div style={{ borderTop:'1px solid var(--hair)' }}>
        {items === null && (MOCK_ITEMS.length === 0) ? (
          <Spinner />
        ) : (
          <table style={{ width:'100%', borderCollapse:'collapse' }}>
            <thead className="table-head-center">
              <tr style={{ color:'var(--muted)' }}>
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
              {dataSource
                .filter(e => !intent || (String(e.intent||'').toLowerCase()===String(intent).toLowerCase()))
                .filter(e => !severity || (String(e.severity||'').toLowerCase().startsWith(String(severity).toLowerCase()[0])))
                .filter(e => !product || (e.product||'').toLowerCase().includes(product.toLowerCase()))
                .filter(e => !assignee || (e.assignee||'').toLowerCase().includes(assignee.toLowerCase()))
                .filter(e => {
                  const q = (params.get('q')||'').toLowerCase();
                  if (!q) return true;
                  return (e.text||'').toLowerCase().includes(q);
                })
                .slice((page-1)*limit, (page-1)*limit + limit)
                .map((e:any) => {
                  const intentChip = e.intent || '—';
                  const severityChip = e.severity || '—';
                  const productVal = e.product || '—';
                  const age = e.age || '—';
                  const sla = e.sla || '—';
                  const who = e.assignee || 'Unassigned';
                  return (
                    <tr key={e.id || `${e.channel}-${e.text}`} style={{ borderBottom:'1px solid var(--hair)' }}>
                      <td style={{ whiteSpace:'nowrap', padding:'8px 6px' }}>{cap(String(e.channel||''))}</td>
                      <td style={{ padding:'8px 6px' }}>
                        <span style={{ border:'1px solid var(--hair)', padding:'2px 6px' }}>{intentChip}</span>
                      </td>
                      <td style={{ padding:'8px 6px' }}>
                        <span style={{ border:'1px solid var(--hair)', padding:'2px 6px' }}>{severityChip}</span>
                      </td>
                      <td style={{ padding:'8px 6px' }}>
                        {e.id ? <Link to={`/events/${e.id}`}>{e.text}</Link> : <span>{e.text}</span>}
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
        <span>Page {page} / {Math.max(1, Math.ceil(computedTotal / limit))}</span>
        <button onClick={() => setPage(p => p + 1)} disabled={page >= Math.ceil(computedTotal / limit)}>Next</button>
      </div>
    </div>
  );
}
