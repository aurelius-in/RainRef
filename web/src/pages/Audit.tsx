import { useEffect, useState } from "react";
import { api } from "../lib/api";

export default function Audit() {
  const [items, setItems] = useState<any[] | null>(null);
  useEffect(() => {
    api.get("/audit").then(r => setItems(r.data.items || [])).catch(() => setItems([]));
  }, []);
  return (
    <div>
      <h2>Audit</h2>
      {items === null ? <div>Loadingâ€¦</div> : (
        <ul>
          {items.map(a => (<li key={a.id}>{a.receipt_id} â€” verified: {String(a.verified)}</li>))}
        </ul>
      )}
    </div>
  );
}
