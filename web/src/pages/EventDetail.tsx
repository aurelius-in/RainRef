import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { api } from "../lib/api";

export default function EventDetail() {
  const { id } = useParams();
  const [event, setEvent] = useState<any>(null);
  const [answer, setAnswer] = useState<any>(null);
  useEffect(() => {
    api.get(`/ref/events/${id}`).then((r) => setEvent(r.data));
  }, [id]);
  const draft = async () => {
    const r = await api.post("/support/answer", {
      source: "inbox",
      channel: "support",
      text: event?.text || "",
      user_ref: event?.user_ref,
    });
    setAnswer(r.data);
  };
  const execute = async () => {
    if (!answer?.actions_suggested?.length) return;
    await api.post("/action/execute", answer.actions_suggested[0]);
    alert("Action executed (receipt recorded)");
  };
  return (
    <div>
      <h2>Event</h2>
      <pre>{JSON.stringify(event, null, 2)}</pre>
      <button onClick={draft}>Draft Answer</button>
      {answer && (
        <div>
          <h3>Drafted Answer</h3>
          <pre>{JSON.stringify(answer, null, 2)}</pre>
          {Array.isArray(answer?.citations) && answer.citations.length > 0 && (
            <div>
              <h4>Citations</h4>
              <ul>
                {answer.citations.map((c: string) => {
                  const cid = c.startsWith("kb:") ? c.slice(3) : c;
                  return (
                    <li key={c}>
                      <Link to={`/kb/${cid}`}>{c}</Link>
                    </li>
                  );
                })}
              </ul>
            </div>
          )}
          <button onClick={execute}>Execute Suggested Action</button>
        </div>
      )}
    </div>
  );
}
