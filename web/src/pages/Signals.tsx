import { useEffect, useState } from "react";
import Spinner from "../components/Spinner";
import { api } from "../lib/api";

export default function Signals() {
  const [items, setItems] = useState<any[] | null>(null);
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const limit = 10;
  useEffect(() => {
    setItems(null);
    api.get("/signals", { params: { page, limit } }).then(r => { setItems(r.data.items || []); setTotal(r.data.total || 0); }).catch(() => setItems([]));
  }, [page]);
  return (
    <div>
      <h2>Signals</h2>
      {items === null ? <Spinner /> : (
        <>
          <ul>
            {items.map(s => (<li key={s.id}>{s.type} â€” {s.origin}</li>))}
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
