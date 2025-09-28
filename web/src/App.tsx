import { useEffect, useState } from "react";
import { api } from "./lib/api";
import Header from "./components/Header";

export default function App() {
  const [health, setHealth] = useState<any>(null);
  useEffect(() => {
    api.get("/healthz").then(r => setHealth(r.data)).catch(() => setHealth({ ok: false }));
  }, []);
  return (
    <>
      <Header />
      <main style={{ padding: 16 }}>
        <h2>Health</h2>
        <pre>{JSON.stringify(health, null, 2)}</pre>
      </main>
    </>
  );
}
