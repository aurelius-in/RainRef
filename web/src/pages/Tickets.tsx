import { useEffect, useState } from "react";
import Spinner from "../components/Spinner";
import { api } from "../lib/api";

const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8080";

export default function Tickets() {
  const [items, setItems] = useState<any[] | null>(null);
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [status, setStatus] = useState("");
  const [counts, setCounts] = useState<any>({});
  const limit = 10;
  const refresh = async () => {
    setItems(null);
    const r = await api.get("/support/tickets", { params: { page, limit, status } });
    setItems(r.data.items || []);
    setTotal(r.data.total || 0);
    const c = await api.get("/support/tickets/counts");
    setCounts(c.data || {});
  };
  useEffect(() => { refresh(); }, [page, status]);

  const close = async (id: string) => {
    await api.post(`/support/tickets/${id}/close`);
    await refresh();
  };

  return (
    <div>
      <h2>Tickets</h2>
      <a href={`${API_BASE}/support/tickets/export`} target="_blank" rel="noreferrer">Export CSV</a>
      <div style={{ display: 'flex', gap: 12 }}>
        <div>Open: {counts.open || 0}</div>
        <div>Draft: {counts.draft || 0}</div>
        <div>Closed: {counts.closed || 0}</div>
      </div>
      <select value={status} onChange={e => { setPage(1); setStatus(e.target.value); }}>
        <option value="">All</option>
        <option value="open">Open</option>
        <option value="draft">Draft</option>
        <option value="closed">Closed</option>
      </select>
      {items === null ? <Spinner /> : (
        <>
          <ul>
            {items.map(t => (
              <li key={t.id}>
                {t.id} â€” {t.status} {t.status !== 'closed' && (<button onClick={() => close(t.id)}>Close</button>)}
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
