import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import Spinner from "../components/Spinner";
import { api } from "../lib/api";

export default function Kb() {
  const [items, setItems] = useState<any[] | null>(null);
  const [q, setQ] = useState("");
  const [tags, setTags] = useState("");
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const limit = 10;
  const refresh = async () => {
    setItems(null);
    const r = await api.get("/kb/cards", { params: { query: q, tags, page, limit } });
    setItems(r.data.results || []);
    setTotal(r.data.total || 0);
  };
  useEffect(() => { refresh(); }, [page]);

  const upload = async (e: any) => {
    const file = e.target.files?.[0];
    if (!file) return;
    const fd = new FormData();
    fd.append("file", file);
    await api.post("/kb/upload", fd);
    await refresh();
  };

  return (
    <div>
      <h2>Knowledge</h2>
      <input placeholder="search" value={q} onChange={e => setQ(e.target.value)} />
      <input placeholder="tags (comma-separated)" value={tags} onChange={e => setTags(e.target.value)} />
      <button onClick={() => { setPage(1); refresh(); }}>Search</button>
      <input type="file" onChange={upload} />
      {items === null ? (
        <Spinner />
      ) : (
        <>
          <ul>
            {items.map((c) => (
              <li key={c.id}><Link to={`/kb/${c.id}`}>{c.title}</Link></li>
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
