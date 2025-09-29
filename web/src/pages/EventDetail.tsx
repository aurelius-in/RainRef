import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { api } from "../lib/api";

export default function EventDetail() {
  const { id } = useParams();
  const [event, setEvent] = useState<any>(null);
  const [answer, setAnswer] = useState<any>(null);
  const [who, setWho] = useState<any>(null);
  const [okMsg, setOkMsg] = useState<string | null>(null);
  const [tab, setTab] = useState<'answer'|'evidence'|'history'>('answer');
  const [evidence, setEvidence] = useState<any[] | null>(null);
  const [history, setHistory] = useState<any[] | null>(null);
  useEffect(() => {
    api.get(`/ref/events/${id}`).then(r => setEvent(r.data));
    api.get('/auth/whoami').then(r => setWho(r.data)).catch(()=>setWho(null));
  }, [id]);
  const draft = async () => {
    const r = await api.post("/support/answer", { source: "inbox", channel: "support", text: event?.text || "", user_ref: event?.user_ref });
    setAnswer(r.data);
  };
  const execute = async () => {
    if (!answer?.actions_suggested?.length) return;
    try {
      const r = await api.post("/action/execute", answer.actions_suggested[0]);
      const rid = r?.data?.beacon_receipt_id || 'receipt';
      try { await navigator.clipboard.writeText(rid); } catch {}
      setOkMsg(`Receipt • ${rid} (copied)`);
    } catch (err: any) {
      const detail = err?.response?.data?.detail || 'action blocked';
      setOkMsg(`Blocked: ${detail}`);
    } finally {
      setTimeout(() => setOkMsg(null), 3000);
    }
  };
  const closeTicket = async () => {
    if (!answer?.ticket_id) return;
    await api.post(`/support/tickets/${answer.ticket_id}/close`);
    setOkMsg("Ticket closed");
    setTimeout(() => setOkMsg(null), 3000);
  };

  // Load Evidence and History on demand
  useEffect(() => {
    const loadEvidence = async () => {
      if (!answer?.citations?.length) { setEvidence([]); return; }
      try {
        const ids: string[] = (answer.citations as string[]).map((c: string) => c.startsWith('kb:') ? c.slice(3) : c);
        const results = await Promise.all(ids.map(cid => api.get(`/kb/cards/${cid}`).then(r => r.data).catch(() => null)));
        setEvidence(results.filter(Boolean));
      } catch {
        setEvidence([]);
      }
    };
    const loadHistory = async () => {
      if (!answer?.ticket_id) { setHistory([]); return; }
      try {
        const r = await api.get(`/support/tickets/${answer.ticket_id}/actions`);
        setHistory(r.data.items || []);
      } catch {
        setHistory([]);
      }
    };
    if (tab === 'evidence') loadEvidence();
    if (tab === 'history') loadHistory();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [tab, JSON.stringify(answer?.citations), answer?.ticket_id]);
  return (
    <div style={{ display:'grid', gridTemplateColumns:'1fr 360px', gap:24 }}>
      <section>
        <header style={{ display:'flex', alignItems:'center', justifyContent:'space-between' }}>
          <h2 style={{ margin:0 }}>Answer</h2>
          <div style={{ display:'flex', gap:8 }}>
            <button onClick={draft} disabled={!['admin','support_lead','support'].includes(who?.role)}>Propose Answer</button>
            {answer?.ticket_id && <button onClick={closeTicket} disabled={!['admin','support_lead','support'].includes(who?.role)}>Close</button>}
          </div>
        </header>
        {!['admin','support_lead','support'].includes(who?.role || '') && (
          <div className="ref-plate" role="status" style={{ margin:'8px 0' }}>Login with a support role to propose answers and execute actions.</div>
        )}
        {okMsg && <div className="ref-plate" role="status">{okMsg}</div>}
        <article style={{ border:'1px solid var(--hair)', background:'var(--panel)', padding:16, minHeight:240 }}>
          <div style={{ display:'flex', gap:12, borderBottom:'1px solid var(--hair)', marginBottom:12 }} role="tablist"
               onKeyDown={(e)=>{
                 const order = ['answer','evidence','history'] as const;
                 const idx = order.indexOf(tab);
                 if (e.key === 'ArrowRight') setTab(order[(idx+1)%order.length]);
                 if (e.key === 'ArrowLeft') setTab(order[(idx+order.length-1)%order.length]);
               }}>
            <button role="tab" aria-selected={tab==='answer'} onClick={()=>setTab('answer')}>Answer</button>
            <button role="tab" aria-selected={tab==='evidence'} onClick={()=>setTab('evidence')}>Evidence</button>
            <button role="tab" aria-selected={tab==='history'} onClick={()=>setTab('history')}>History</button>
          </div>
          {tab==='answer' ? (
            answer ? (
              <div>
                <div style={{ marginBottom:8, color:'var(--muted)' }}>State: Draft</div>
                <div style={{ whiteSpace:'pre-wrap' }}>{answer.answer_md || 'No content yet.'}</div>
                {Array.isArray(answer?.citations) && answer.citations.length > 0 && (
                  <div style={{ marginTop:12 }}>
                    {answer.citations.map((c: string) => {
                      const cid = c.startsWith("kb:") ? c.slice(3) : c;
                      return <Link key={c} to={`/kb/${cid}`} style={{ border:'1px solid var(--hair)', padding:'2px 6px', marginRight:6, display:'inline-block' }}>{c}</Link>;
                    })}
                  </div>
                )}
              </div>
            ) : (
              <div style={{ color:'var(--muted)' }}>Click “Propose Answer” to draft a cited reply.</div>
            )
          ) : tab==='evidence' ? (
            <div>
              {!evidence ? <div style={{ color:'var(--muted)' }}>Loading…</div> : evidence.length === 0 ? (
                <div style={{ color:'var(--muted)' }}>No evidence yet.</div>
              ) : (
                <ul>
                  {evidence.map((k:any) => (
                    <li key={k.id} style={{ marginBottom:8 }}>
                      <strong>{k.title}</strong>
                      <div style={{ color:'var(--muted)' }}>{String(k.body||'').slice(0,140)}…</div>
                    </li>
                  ))}
                </ul>
              )}
            </div>
          ) : (
            <div>
              {!history ? <div style={{ color:'var(--muted)' }}>Loading…</div> : history.length === 0 ? (
                <div style={{ color:'var(--muted)' }}>No history yet.</div>
              ) : (
                <ul>
                  {history.map((h:any) => (
                    <li key={h.id} style={{ marginBottom:6 }}>
                      <code>{h.type}</code> — ticket {h.ticket_id || '—'}
                    </li>
                  ))}
                </ul>
              )}
            </div>
          )}
        </article>
      </section>
      <aside>
        <div className="ref-plate">
          <h3 style={{ marginTop:0 }}>Suggested Actions</h3>
          {answer?.actions_suggested?.length ? (
            <div>
              {answer.actions_suggested.map((a:any, idx:number) => (
                <div key={idx} style={{ borderTop:'1px solid var(--hair)', paddingTop:8, marginTop:8 }}>
                  <div style={{ display:'flex', justifyContent:'space-between' }}>
                    <strong>{a.type}</strong>
                    <span style={{ border:'1px solid var(--hair)', padding:'2px 6px' }}>Policy: Pass</span>
                  </div>
                  <pre style={{ background:'transparent' }}>{JSON.stringify(a.params||{}, null, 2)}</pre>
                  <button onClick={execute} disabled={!['admin','support_lead','support'].includes(who?.role)}>Execute</button>
                </div>
              ))}
            </div>
          ) : (
            <div style={{ color:'var(--muted)' }}>No actions yet.</div>
          )}
        </div>
        <div style={{ marginTop:12 }} className="ref-plate">
          <h4 style={{ marginTop:0 }}>Related KB</h4>
          <div style={{ color:'var(--muted)' }}>Shown after answer is proposed.</div>
        </div>
      </aside>
    </div>
  );
}

