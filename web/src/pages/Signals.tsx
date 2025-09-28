import { useEffect, useState } from "react";
import { api } from "../lib/api";

export default function Signals() {
  const [items, setItems] = useState<any[] | null>(null);
  useEffect(() => {
    api.get("/signals").then(r => setItems(r.data.items || [])).catch(() => setItems([]));
  }, []);
  return (
    <div>
      <h2>Signals</h2>
      {items === null ? <div>Loadingâ€¦</div> : (
        <ul>
          {items.map(s => (<li key={s.id}>{s.type} â€” {s.origin}</li>))}
        </ul>
      )}
    </div>
  );
}
