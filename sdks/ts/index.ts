export async function health(base = "http://localhost:8080") {
  const r = await fetch(`${base}/healthz`);
  return r.json();
}

export async function listEvents(base = "http://localhost:8080") {
  const r = await fetch(`${base}/ref/events`);
  return r.json();
}
