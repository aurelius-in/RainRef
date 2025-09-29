import { useEffect, useRef, useState } from "react";
import { api } from "../lib/api";
import { showToast } from "../lib/toast";

export default function Playbooks() {
  const [items, setItems] = useState<any[] | null>(null);
  const [selected, setSelected] = useState<any | null>(null);
  const [message, setMessage] = useState<string>("");
  const liveRef = useRef<HTMLDivElement>(null);
  useEffect(() => {
    // Placeholder: list playbooks when API available
    setItems([
      { id: 'activation_1', yaml: `id: activation_1\nmatch:\n  intent: friction\n  patterns:\n    - did not get activation\nactions:\n  - type: resend_activation\n    params:\n      template: welcome_v2\n` }
    ]);
    setSelected({ id: 'activation_1', yaml: `id: activation_1\nmatch:\n  intent: friction\n  patterns:\n    - did not get activation\nactions:\n  - type: resend_activation\n    params:\n      template: welcome_v2\n` });
  }, []);
  return (
    <div style={{ display:'grid', gridTemplateColumns:'320px 1fr', gap:16 }}>
      <aside className="ref-stripes" style={{ padding: 12 }}>
        <div className="ref-plate">
          <h3 style={{ marginTop:0 }}>Playbooks</h3>
          {items?.length ? items.map(p => (
            <div key={p.id} style={{ borderTop:'1px solid var(--hair)', paddingTop:8, marginTop:8 }}>
              <button onClick={()=>setSelected(p)} style={{ textAlign:'left' }}>
                {p.id}
              </button>
            </div>
          )) : <div style={{ color:'var(--muted)' }}>No playbooks yet.</div>}
        </div>
      </aside>
      <main>
        <div style={{ display:'flex', gap:12, alignItems:'center', marginBottom:12 }}>
          <button onClick={()=>{ if(selected){ navigator.clipboard.writeText(selected.yaml).then(()=>{ setMessage('Copied YAML'); showToast('Copied playbook YAML'); },()=>{ setMessage('Copy failed'); showToast('Copy failed'); }); } }}>Copy</button>
          <button onClick={()=>{ if(selected){ const b = new Blob([selected.yaml], { type:'text/yaml' }); const u = URL.createObjectURL(b); const a = document.createElement('a'); a.href=u; a.download=`${selected.id}.yaml`; a.click(); URL.revokeObjectURL(u); setMessage('Downloaded YAML'); showToast('Downloaded playbook YAML'); } }}>Download</button>
          <button onClick={()=>{ if(!selected) return; const yaml = String(selected.yaml||''); const hasId = /\bid\s*:\s*\S+/.test(yaml); const hasActions = /\bactions\s*:\s*[\s\S]+/.test(yaml); const ok = hasId && hasActions; const msg = ok ? 'Valid playbook (basic)' : 'Invalid: missing id or actions'; setMessage(msg); showToast(msg); }}>Validate</button>
          <div ref={liveRef} aria-live="polite" style={{ minHeight:20, color:'var(--muted)' }}>{message}</div>
        </div>
        <div className="ref-plate">
          <h3 style={{ marginTop:0 }}>YAML Preview</h3>
          <pre className="code-block" style={{ overflowX:'auto' }}>
            <code>
{(selected?.yaml || 'Select a playbook to preview.').split('\n').map((line, i) => {
  const trimmed = line.trimStart();
  const isKey = /^[a-zA-Z_][\w-]*\s*:/.test(trimmed);
  const isDash = /^-\s/.test(trimmed);
  const isComment = /^#/.test(trimmed);
  const keyPart = isKey ? trimmed.split(':',1)[0] : '';
  const rest = isKey ? trimmed.slice(keyPart.length) : trimmed;
  const color = isComment ? 'var(--muted)' : isKey ? '#2563eb' : isDash ? '#16a34a' : 'inherit';
  return (
    <span key={i} style={{ color }}>
      {isKey ? line.replace(trimmed, '') + keyPart : line.replace(trimmed, '')}
      {isKey ? <>
        <span style={{ color:'#6b7280' }}>{rest.split(/\s+/)[0]}</span>
        {rest.slice(rest.split(/\s+/)[0].length)}
      </> : rest}
      {"\n"}
    </span>
  );
})}
            </code>
          </pre>
        </div>
      </main>
    </div>
  );
}

