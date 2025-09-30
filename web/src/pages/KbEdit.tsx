import { useState } from "react";
import { api } from "../lib/api";

export default function KbEdit() {
  const [title, setTitle] = useState("");
  const [body, setBody] = useState("");
  const [tags, setTags] = useState("");
  const [msg, setMsg] = useState("");
  return (
    <div className="ref-plate">
      <h2 style={{ marginTop: 0 }}>KB Editor</h2>
      <div style={{ display: 'grid', gap: 8 }}>
        <input placeholder="Title" value={title} onChange={e=>setTitle(e.target.value)} />
        <textarea placeholder="Body" value={body} onChange={e=>setBody(e.target.value)} style={{ minHeight: 160 }} />
        <input placeholder="tags (comma-separated)" value={tags} onChange={e=>setTags(e.target.value)} />
        <div style={{ display:'flex', gap:8 }}>
          <button onClick={async()=>{
            try {
              const res = await api.post('/kb/cards', { title, body, tags: tags.split(',').map(s=>s.trim()).filter(Boolean) });
              setMsg(`Saved ${res.data?.id || 'ok'}`);
            } catch (e:any) {
              setMsg(e?.response?.data?.detail || e?.message || 'save failed');
            }
          }}>Save</button>
          <div aria-live="polite" style={{ color:'var(--muted)' }}>{msg}</div>
        </div>
      </div>
    </div>
  );
}


