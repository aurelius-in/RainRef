import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { api } from "../lib/api";

export default function EventDetail() {
  const { id } = useParams();
  const [event, setEvent] = useState<any>(null);
  const [answer, setAnswer] = useState<any>(null);
  const [okMsg, setOkMsg] = useState<string | null>(null);
  useEffect(() => {
    api.get(`/ref/events/${id}`).then(r => setEvent(r.data));
  }, [id]);
  const draft = async () => {
    const r = await api.post("/support/answer", { source: "inbox", channel: "support", text: event?.text || "", user_ref: event?.user_ref });
    setAnswer(r.data);
  };
  const execute = async () => {
    if (!answer?.actions_suggested?.length) return;
    await api.post("/action/execute", answer.actions_suggested[0]);
    setOkMsg("Action executed â€” receipt recorded");
    setTimeout(() => setOkMsg(null), 3000);
  };
  const closeTicket = async () => {
    if (!answer?.ticket_id) return;
    await api.post(`/support/tickets/${answer.ticket_id}/close`);
    setOkMsg("Ticket closed");
    setTimeout(() => setOkMsg(null), 3000);
  };
  return (
    <div>
      <h2>Event</h2>
      {okMsg && <div style={{ background: '#ecfdf5', color: '#065f46', padding: 8, borderRadius: 4 }}>{okMsg}</div>}
      <pre>{JSON.stringify(event, null, 2)}</pre>
      <button onClick={draft}>Draft Answer</button>
      {answer && (
        <div>
          <h3>Drafted Answer</h3>
          {answer?.ticket_id && <div>Ticket: {answer.ticket_id}</div>}
          <pre>{JSON.stringify(answer, null, 2)}</pre>
          {Array.isArray(answer?.citations) && answer.citations.length > 0 && (
            <div>
              <h4>Citations</h4>
              <ul>
                {answer.citations.map((c: string) => {
                  const cid = c.startsWith("kb:") ? c.slice(3) : c;
                  return <li key={c}><Link to={`/kb/${cid}`}>{c}</Link></li>;
                })}
              </ul>
            </div>
          )}
          <button onClick={execute}>Execute Suggested Action</button>
          {answer?.ticket_id && <button onClick={closeTicket}>Close Ticket</button>}
        </div>
      )}
    </div>
  );
}
