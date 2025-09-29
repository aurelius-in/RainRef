import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { api } from "../lib/api";
import { showToast } from "../lib/toast";

export default function AuditDetail() {
  const { id } = useParams();
  const [rec, setRec] = useState<any>(null);
  useEffect(() => {
    if (!id) return;
    api.get(`/audit/${id}`).then(r => setRec(r.data)).catch(()=>setRec({ receipt_id: id, verified: false }));
  }, [id]);
  const copy = async () => { try { await navigator.clipboard.writeText(String(id)); showToast('Copied receipt id'); } catch { showToast('Copy failed'); } };
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
            {rec.verification_details && (<>
              <div style={{ color:'var(--muted)' }}>Issuer</div>
              <div>{rec.verification_details.issuer || '—'}</div>
              <div style={{ color:'var(--muted)' }}>Reason</div>
              <div>{rec.verification_details.reason || '—'}</div>
              <div style={{ color:'var(--muted)' }}>Signature Match</div>
              <div>{String(rec.verification_details.signature_match ?? '—')}</div>
              <div style={{ color:'var(--muted)' }}>Timestamp</div>
              <div>{rec.verification_details.timestamp ? new Date(rec.verification_details.timestamp*1000).toLocaleString() : '—'}</div>
            </>)}
          </div>
          <h4 style={{ marginTop: 16 }}>Raw</h4>
          <pre className="code-block" style={{ whiteSpace:'pre-wrap' }}>{JSON.stringify(rec, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

