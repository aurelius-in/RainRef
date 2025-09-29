import { useEffect, useState } from "react";
import { api } from "../lib/api";

export default function Playbooks() {
  const [items, setItems] = useState<any[] | null>(null);
  const [selected, setSelected] = useState<any | null>(null);
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
        <div className="ref-plate">
          <h3 style={{ marginTop:0 }}>YAML Preview</h3>
          <pre className="code-block">{selected?.yaml || 'Select a playbook to preview.'}</pre>
        </div>
      </main>
    </div>
  );
}

