import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../lib/api";

export default function Kb() {
  const [items, setItems] = useState<any[]>([]);
  const [q, setQ] = useState("");
  const refresh = async () => {
    const r = await api.get("/kb/cards", { params: { query: q } });
    setItems(r.data.results || []);
  };
  useEffect(() => {
    refresh();
  }, []);

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
      <input
        placeholder="search"
        value={q}
        onChange={(e) => setQ(e.target.value)}
      />
      <button onClick={refresh}>Search</button>
      <input type="file" onChange={upload} />
      <ul>
        {items.map((c) => (
          <li key={c.id}>
            <Link to={`/kb/${c.id}`}>{c.title}</Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
