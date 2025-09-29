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
  const copy = async () => { try { await navigator.clipboard.writeText(String(id)); } catch {} };
  return (
    <div className="ref-plate">
      <h3 style={{ marginTop:0 }}>Receipt</h3>
      <div style={{ display:'flex', gap:8, alignItems:'center' }}>
        <strong>Receipt • {id}</strong>
        <button onClick={copy}>Copy</button>
      </div>
      {rec && (
        <div style={{ marginTop: 12 }}>
          <div style={{ display:'grid', gridTemplateColumns:'160px 1fr', rowGap:6 }}>
            <div style={{ color:'var(--muted)' }}>Verified</div>
            <div>{String(rec.verified)}</div>
            {rec.created_at && (<>
              <div style={{ color:'var(--muted)' }}>Created At</div>
              <div>{new Date(rec.created_at).toLocaleString()}</div>
            </>)}
            {rec.details && (<>
              <div style={{ color:'var(--muted)' }}>Issuer</div>
              <div>{rec.details.issuer || '—'}</div>
              <div style={{ color:'var(--muted)' }}>Signature</div>
              <div className="code-block" style={{ whiteSpace:'nowrap', overflow:'hidden', textOverflow:'ellipsis' }}>{rec.details.signature || '—'}</div>
              <div style={{ color:'var(--muted)' }}>Timestamp</div>
              <div>{rec.details.ts || '—'}</div>
            </>)}
          </div>
          <h4 style={{ marginTop: 16 }}>Raw</h4>
          <pre className="code-block" style={{ whiteSpace:'pre-wrap' }}>{JSON.stringify(rec, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

