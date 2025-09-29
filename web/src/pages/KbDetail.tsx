import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { api } from "../lib/api";

export default function KbDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [card, setCard] = useState<any>(null);
  const [who, setWho] = useState<any>(null);
  useEffect(() => {
    if (!id) return;
    api.get(`/kb/cards/${id}`).then((r) => setCard(r.data));
    api.get('/auth/whoami').then(r => setWho(r.data)).catch(()=>setWho(null));
  }, [id]);
  return (
    <div>
      <h2>KB Card</h2>
      <div style={{ display:'flex', gap:8, marginBottom:8 }}>
        {who?.role === 'admin' && (
          <button onClick={async () => { if(!id) return; await api.delete(`/kb/cards/${id}`); navigate('/kb'); }}>Delete</button>
        )}
        <button onClick={()=>navigate(`/kb/${id}/edit`)} disabled={who?.role !== 'admin'}>Edit</button>
      </div>
      <pre className="code-block">{JSON.stringify(card, null, 2)}</pre>
    </div>
  );
}

