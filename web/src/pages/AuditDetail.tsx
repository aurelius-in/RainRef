import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { api } from "../lib/api";

export default function AuditDetail() {
  const { id } = useParams();
  const [rec, setRec] = useState<any>(null);
  useEffect(() => {
    if (!id) return;
    api.get(`/audit/${id}`).then(r => setRec(r.data)).catch(()=>setRec({ receipt_id: id, verified: false }));
  }, [id]);
  return (
    <div className="ref-plate">
      <h3 style={{ marginTop:0 }}>Receipt</h3>
      <div style={{ display:'flex', gap:8, alignItems:'center' }}>
        <strong>Receipt • {id}</strong>
        <button onClick={async()=>{ try { await navigator.clipboard.writeText(String(id)); } catch {} }}>Copy</button>
      </div>
      <pre style={{ whiteSpace:'pre-wrap' }}>{JSON.stringify(rec, null, 2)}</pre>
    </div>
  );
}

