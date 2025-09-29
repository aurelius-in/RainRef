import { useEffect, useState } from "react";
import Spinner from "../components/Spinner";
import { api } from "../lib/api";

const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8080";

export default function Actions() {
  const [items, setItems] = useState<any[] | null>(null);
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [who, setWho] = useState<any>(null);
  const [compact, setCompact] = useState(false);
  const limit = 10;
  useEffect(() => {
    api.get('/auth/whoami').then(r => setWho(r.data)).catch(()=>setWho(null));
  }, []);
  useEffect(() => {
    if (who?.role !== 'admin') return;
    setItems(null);
    api.get("/action/history", { params: { page, limit } }).then(r => { setItems(r.data.items || []); setTotal(r.data.total || 0); }).catch(() => setItems([]));
  }, [page]);
  return (
    <div>
      <div style={{ display:'flex', alignItems:'center', justifyContent:'space-between' }}>
        <h2 style={{ margin:0 }}>Actions</h2>
        <div style={{ display:'flex', gap:8 }}>
          <button onClick={()=>setCompact(c=>!c)}>{compact ? 'Default View' : 'Compact View'}</button>
        </div>
      </div>
      {who?.role !== 'admin' && (
        <div className="ref-plate" role="status" style={{ marginBottom: 12 }}>Admin role required to view action history.</div>
      )}
      {who?.role === 'admin' ? (items === null ? <Spinner /> : (
        <>
          <ul className={compact ? 'compact-table' : undefined}>
            {items.map(a => (
              <li key={a.id}>{a.type} — ticket: {a.ticket_id || "-"} — <a href={`${API_BASE}/audit/${a.receipt_id}`} target="_blank" rel="noreferrer">receipt</a></li>
            ))}
          </ul>
          <div style={{ display: 'flex', gap: 8 }}>
            <button onClick={() => setPage(p => Math.max(1, p - 1))} disabled={page === 1}>Prev</button>
            <span>Page {page} / {Math.max(1, Math.ceil(total / limit))}</span>
            <button onClick={() => setPage(p => p + 1)} disabled={page >= Math.ceil(total / limit)}>Next</button>
          </div>
        </>
      )) : null}
    </div>
  );
}
