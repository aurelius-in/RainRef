import { useEffect, useState } from "react";
import { api } from "../lib/api";
import { showToast } from "../lib/toast";

export default function Answer() {
  const [query, setQuery] = useState("");
  const [draft, setDraft] = useState<any | null>(null);
  const [busy, setBusy] = useState(false);

  const draftAnswer = async () => {
    if (!query.trim()) return;
    setBusy(true);
    try {
      const r = await api.post("/support/answer", { text: query });
      setDraft(r.data);
      showToast("Drafted answer");
    } catch {}
    finally { setBusy(false); }
  };

  const execute = async (action: any) => {
    try {
      const r = await api.post("/action/execute", action);
      const id = r.data?.beacon_receipt_id;
      showToast(id ? `Executed • ${id}` : 'Executed');
    } catch {}
  };

  return (
    <div style={{ display:'grid', gridTemplateColumns:'1fr', gap:16 }}>
      <main style={{ maxWidth: '100%' }}>
        <div style={{ display:'block', marginBottom:12 }}>
          <textarea
            value={query}
            onChange={e=>setQuery(e.target.value)}
            placeholder="Ask or paste the customer message"
            style={{ width:'100%', minHeight: 160, padding: 12, border: '1px solid var(--hair)', borderRadius: 6, background:'var(--panel)', color:'var(--fg)' }}
          />
          <div style={{ display:'flex', justifyContent:'center', marginTop:8 }}>
            <button onClick={draftAnswer} disabled={busy} style={{ padding:'8px 14px' }}>Draft</button>
          </div>
        </div>

        {/* Answer workspace */}
        {!draft ? (
          <div className="ref-stripes" style={{ padding:24 }}>
            <div className="ref-plate" style={{ maxWidth: '100%' }}>
              <p style={{ color:'var(--muted)', margin: 0 }}>Draft answers grounded on your KB. Actions are policy-gated and require approval to run.</p>
            </div>
          </div>
        ) : (
          <article className="ref-plate">
            <div className="code-block" style={{ whiteSpace:'pre-wrap' }}>{draft.answer_md}</div>
            <div style={{ marginTop:12 }}>
              <h4 style={{ marginTop:0 }}>Citations</h4>
              <ul>
                {(draft.citations||[]).map((c:string)=>(<li key={c}><code>{c}</code></li>))}
              </ul>
            </div>
          </article>
        )}

        {/* Suggested actions */}
        <section className="ref-plate">
          <h3 style={{ marginTop:0 }}>Suggested Actions</h3>
          {!draft || !draft.actions_suggested?.length ? (
            <div style={{ color:'var(--muted)' }}>No actions yet.</div>
          ) : (
            <ul style={{ listStyle:'none', padding:0, margin:0 }}>
              {draft.actions_suggested.map((a:any, idx:number)=> (
                <li key={idx} style={{ border:'1px solid var(--hair)', borderRadius:6, padding:8, marginBottom:8 }}>
                  <div style={{ display:'flex', justifyContent:'space-between', alignItems:'center', marginBottom:6 }}>
                    <strong>{a.type}</strong>
                    <span className="badge" title={a.policy_reason || ''}>{a.allowed ? 'Allowed' : 'Blocked'}</span>
                  </div>
                  <pre className="code-block" style={{ fontSize:12 }}>{JSON.stringify(a.params||{}, null, 2)}</pre>
                  <div style={{ display:'flex', gap:8 }}>
                    <button onClick={()=>execute({ type:a.type, params:a.params })} disabled={!a.allowed}>Execute</button>
                  </div>
                </li>
              ))}
            </ul>
          )}
        </section>

        {/* Related KB */}
        <section className="ref-plate">
          <h3 style={{ marginTop:0 }}>Related KB</h3>
          {!draft ? (
            <div style={{ color:'var(--muted)' }}>Shown after answer is proposed.</div>
          ) : (
            <div style={{ color:'var(--muted)' }}>Coming soon.</div>
          )}
        </section>

        {/* Close at bottom */}
        <div style={{ display:'flex', justifyContent:'flex-end' }}>
          <button onClick={()=>window.history.back()} aria-label="Close">Close</button>
        </div>
      </main>
    </div>
  );
}


