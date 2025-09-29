export async function health(base = "http://localhost:8080") {
  const r = await fetch(`${base}/healthz`);
  return r.json();
}

export async function listEvents(base = "http://localhost:8080") {
  const r = await fetch(`${base}/ref/events`);
  return r.json();
}

export async function listActionsByType(base = "http://localhost:8080", type: string, page = 1, limit = 20) {
  const r = await fetch(`${base}/action/history/by-type?type=${encodeURIComponent(type)}&page=${page}&limit=${limit}`);
  return r.json();
}

export async function deleteSignal(base = "http://localhost:8080", id: string) {
  const r = await fetch(`${base}/signals/${id}`, { method: 'DELETE' });
  return r.json();
}

export async function bulkDeleteCards(base = "http://localhost:8080", ids: string[]) {
  const r = await fetch(`${base}/kb/cards/delete`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ ids }) });
  return r.json();
}
