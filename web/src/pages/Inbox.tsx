import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import Spinner from "../components/Spinner";
import { api } from "../lib/api";

export default function Inbox() {
  const [items, setItems] = useState<any[] | null>(null);
  const [order, setOrder] = useState<'asc' | 'desc'>('desc');
  const [byChannel, setByChannel] = useState<any>({});
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const limit = 10;
  useEffect(() => {
    setItems(null);
    api.get("/ref/events", { params: { page, limit, order } }).then(r => { setItems(r.data.items || []); setTotal(r.data.total || 0); }).catch(() => setItems([]));
    api.get("/ref/events/stats").then(r => setByChannel(r.data.by_channel || {})).catch(() => setByChannel({}));
  }, [page, order]);
  return (
    <div>
      <h2>Ref Events</h2>
      <div style={{display:'flex',gap:8}}>{Object.entries(byChannel||{}).map(([k,v]) => <span key={k} style={{border:'1px solid #e5e7eb',padding:'2px 6px',borderRadius:6}}>{k}: {v as any}</span>)}</div>
      <select value={order} onChange={e => setOrder(e.target.value as any)}>
        <option value="desc">Newest</option>
        <option value="asc">Oldest</option>
      </select>
      {items === null ? (
        <Spinner />
      ) : (
        <>
          <ul>
            {items.map((e) => (
              <li key={e.id}>
                <Link to={`/events/${e.id}`}>{e.channel}: {e.text}</Link>
              </li>
            ))}
          </ul>
          <div style={{ display: 'flex', gap: 8 }}>
            <button onClick={() => setPage(p => Math.max(1, p - 1))} disabled={page === 1}>Prev</button>
            <span>Page {page} / {Math.max(1, Math.ceil(total / limit))}</span>
            <button onClick={() => setPage(p => p + 1)} disabled={page >= Math.ceil(total / limit)}>Next</button>
          </div>
        </>
      )}
    </div>
  );
}
