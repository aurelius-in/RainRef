import { useEffect, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import Spinner from "../components/Spinner";
import { api } from "../lib/api";

const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8080";

export default function Kb() {
  const [params] = useSearchParams();
  const [items, setItems] = useState<any[] | null>(null);
  const [q, setQ] = useState("");
  const [tags, setTags] = useState("");
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [stats, setStats] = useState<any>(null);
  const [order, setOrder] = useState<'asc' | 'desc'>('desc');
  const limit = 10;
  const refresh = async () => {
    setItems(null);
    const r = await api.get("/kb/cards", { params: { query: q, tags, page, limit, order } });
    setItems(r.data.results || []);
    setTotal(r.data.total || 0);
  };
  useEffect(() => {
    const qp = params.get('q'); if (qp) setQ(qp);
    refresh();
    api.get("/kb/stats").then(r => setStats(r.data)).catch(() => setStats({}));
  }, [page, order, params]);

  return (
    <div>
      <h2>Knowledge</h2>
      <div style={{display:'flex',gap:12,flexWrap:'wrap',marginBottom:8}}>
        {stats?.top_tags?.map((x:any) => (
          <span key={x.tag} style={{border:'1px solid #e5e7eb',padding:'2px 6px',borderRadius:6}}>{x.tag}: {x.count}</span>
        ))}
        <span style={{opacity:0.7}}>Total: {stats?.total ?? total}</span>
      </div>
      <div style={{ display: 'flex', gap: 12, alignItems: 'center' }}>
        <input placeholder="search" value={q} onChange={e => setQ(e.target.value)} />
        <input placeholder="tags (comma-separated)" value={tags} onChange={e => setTags(e.target.value)} />
        <button onClick={() => { setPage(1); refresh(); }}>Search</button>
        <select value={order} onChange={e => setOrder(e.target.value as any)}>
          <option value="desc">Newest</option>
          <option value="asc">Oldest</option>
        </select>
        <Link to="/kb/new">New Card</Link>
        <a href={`${API_BASE}/kb/cards/export`} target="_blank" rel="noreferrer">Export JSON</a>
      </div>
      {items === null ? (
        <Spinner />
      ) : (
        <>
          <ul>
            {items.map((c) => (
              <li key={c.id}><Link to={`/kb/${c.id}`}>{c.title}</Link> Â· <Link to={`/kb/${c.id}/edit`}>Edit</Link></li>
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
