import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../lib/api";

export default function Inbox() {
  const [items, setItems] = useState<any[]>([]);
  useEffect(() => {
    api.get("/ref/events").then((r) => setItems(r.data.items || []));
  }, []);
  return (
    <div>
      <h2>Ref Events</h2>
      <ul>
        {items.map((e) => (
          <li key={e.id}>
            <Link to={`/events/${e.id}`}>
              {e.channel}: {e.text}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
