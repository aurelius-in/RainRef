export type Json = Record<string, any>;

export class RainRefClient {
  baseUrl: string;
  token?: string;

  constructor(baseUrl = 'http://localhost:8080', token?: string) {
    this.baseUrl = baseUrl.replace(/\/$/, '');
    this.token = token;
  }

  setToken(token: string) {
    this.token = token;
  }

  private headers(): HeadersInit {
    const h: HeadersInit = { 'Content-Type': 'application/json' };
    if (this.token) h['Authorization'] = `Bearer ${this.token}`;
    return h;
  }

  async health(): Promise<Json> {
    const r = await fetch(`${this.baseUrl}/healthz`);
    if (!r.ok) throw new Error(`health ${r.status}`);
    return r.json();
  }

  async login(username: string, password: string): Promise<Json> {
    const r = await fetch(`${this.baseUrl}/auth/login`, {
      method: 'POST',
      headers: this.headers(),
      body: JSON.stringify({ username, password })
    });
    if (!r.ok) throw new Error(`login ${r.status}`);
    const data = await r.json();
    if (data?.access_token) this.setToken(data.access_token);
    return data;
  }

  async whoami(): Promise<Json> {
    const r = await fetch(`${this.baseUrl}/auth/whoami`, { headers: this.headers() });
    if (!r.ok) throw new Error(`whoami ${r.status}`);
    return r.json();
  }

  async ingestEvent(source: string, channel: string, text: string, user_ref?: string): Promise<Json> {
    const payload: Json = { source, channel, text };
    if (user_ref) payload.user_ref = user_ref;
    const r = await fetch(`${this.baseUrl}/ref/events`, {
      method: 'POST', headers: this.headers(), body: JSON.stringify(payload)
    });
    if (!r.ok) throw new Error(`ingest ${r.status}`);
    return r.json();
  }

  async proposeAnswer(text: string, source = 'inbox', channel = 'support', user_ref?: string): Promise<Json> {
    const payload: Json = { source, channel, text };
    if (user_ref) payload.user_ref = user_ref;
    const r = await fetch(`${this.baseUrl}/support/answer`, {
      method: 'POST', headers: this.headers(), body: JSON.stringify(payload)
    });
    if (!r.ok) throw new Error(`answer ${r.status}`);
    return r.json();
  }

  async executeAction(action: Json): Promise<Json> {
    const r = await fetch(`${this.baseUrl}/action/execute`, {
      method: 'POST', headers: this.headers(), body: JSON.stringify(action)
    });
    if (!r.ok) throw new Error(`execute ${r.status}`);
    return r.json();
  }

  async getReceipt(id: string): Promise<Json> {
    const r = await fetch(`${this.baseUrl}/audit/${id}`, { headers: this.headers() });
    if (!r.ok) throw new Error(`receipt ${r.status}`);
    return r.json();
  }
}

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
