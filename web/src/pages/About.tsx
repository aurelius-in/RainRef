import { useEffect, useState } from "react";
import { api } from "../lib/api";

export default function About() {
  const [info, setInfo] = useState<any>(null);
  useEffect(() => { api.get("/info").then(r => setInfo(r.data)); }, []);
  return (
    <div>
      <h2>About RainRef</h2>
      <div>Version: {info?.version} ({info?.git_sha}) — env: {info?.env}</div>
      <div><a href="/docs" target="_blank">API Docs</a> · <a href="/openapi.json" target="_blank">OpenAPI</a> · <a href="/status" target="_blank">Status</a></div>
      <div><a href="https://github.com/aurelius-in/RainRef" target="_blank" rel="noreferrer">GitHub</a></div>
    </div>
  );
}
