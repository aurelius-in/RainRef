import { useEffect, useState } from "react";
import { api } from "../lib/api";

export default function Metrics() {
  const [basic, setBasic] = useState<any>(null);
  const [stats, setStats] = useState<any>(null);
  useEffect(() => {
    api.get("/metrics/basic").then(r => setBasic(r.data));
    api.get("/ref/events/stats").then(r => setStats(r.data));
  }, []);
  return (
    <div>
      <h2>Metrics</h2>
      <h3>Basic</h3>
      <pre>{JSON.stringify(basic, null, 2)}</pre>
      <h3>Event Stats</h3>
      <pre>{JSON.stringify(stats, null, 2)}</pre>
    </div>
  );
}
