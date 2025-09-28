import { useEffect, useState } from "react";
import { api } from "../lib/api";

export default function Health() {
  const [data, setData] = useState<any>(null);
  useEffect(() => { api.get("/healthz/details").then(r => setData(r.data)).catch(() => setData({ ok: false })); }, []);
  return (
    <div>
      <h2>Health Details</h2>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}
