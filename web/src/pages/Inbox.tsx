import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import Spinner from "../components/Spinner";
import { api } from "../lib/api";

const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8080";

export default function Inbox() {
  const [items, setItems] = useState<any[] | null>(null);
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const limit = 10;
  useEffect(() => {
    setItems(null);
    api.get("/ref/events", { params: { page, limit } }).then(r => { setItems(r.data.items || []); setTotal(r.data.total || 0); }).catch(() => setItems([]));
  }, [page]);
  return (
    <div>
      <h2>Ref Events</h2>
      <a href={`${API_BASE}/ref/events/export`} target="_blank" rel="noreferrer">Export CSV</a>
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
