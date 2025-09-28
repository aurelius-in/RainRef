import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { api } from "../lib/api";

export default function KbDetail() {
  const { id } = useParams();
  const [card, setCard] = useState<any>(null);
  useEffect(() => {
    if (!id) return;
    api.get(`/kb/cards/${id}`).then((r) => setCard(r.data));
  }, [id]);
  return (
    <div>
      <h2>KB Card</h2>
      <pre>{JSON.stringify(card, null, 2)}</pre>
    </div>
  );
}
