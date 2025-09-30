import { useEffect, useState } from "react";
import { api } from "../lib/api";
import { showToast } from "../lib/toast";

export default function Audit() {
  const [items, setItems] = useState<any[] | null>(null);
  useEffect(() => {
    api.get("/audit").then(r => setItems(r.data.items || [])).catch(() => setItems([]));
  }, []);
  return (
    <div>
      <h2>Receipts</h2>
      {items === null ? <div>Loading…</div> : (
        <table style={{ width:'100%', borderCollapse:'collapse' }}>
          <thead className="table-head-center">
            <tr style={{ color:'var(--muted)' }}>
              <th>Time</th>
              <th>Action</th>
              <th>Target</th>
              <th>Policy</th>
              <th>Result</th>
              <th>Receipt</th>
            </tr>
          </thead>
          <tbody id="audit-tbody">
            {items.map((a:any) => (
              <tr key={a.id} style={{ borderBottom:'1px solid var(--hair)' }}>
                <td style={{ padding:'6px 8px' }}>{a.created_at || '—'}</td>
                <td style={{ padding:'6px 8px' }}>{a.type || '—'}</td>
                <td style={{ padding:'6px 8px' }}>{a.target || '—'}</td>
                <td style={{ padding:'6px 8px' }}><span style={{ border:'1px solid var(--hair)', padding:'2px 6px' }}>{a.policy || 'Pass'}</span></td>
                <td style={{ padding:'6px 8px' }}>{a.result || 'ok'}</td>
                <td style={{ padding:'6px 8px', display:'flex', gap:8, alignItems:'center' }}>
                  <a href={`/audit/${a.id}`}>Receipt • {a.id?.slice(-6) || '??????'}</a>
                  <button aria-label="Copy receipt id" onClick={async()=>{ try { await navigator.clipboard.writeText(String(a.id||'')); showToast('Copied receipt id'); } catch { showToast('Copy failed'); } }}>Copy</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
      <div style={{ display:'flex', justifyContent:'flex-end', marginTop:8, gap:8 }}>
        <label style={{ display:'flex', alignItems:'center', gap:6 }}>
          <input type="checkbox" aria-label="Compact mode" onChange={(e)=>{
            const root = document.getElementById('audit-tbody');
            if (!root) return;
            (root as HTMLElement).style.fontSize = e.currentTarget.checked ? '13px' : '';
          }} />
          <span style={{ color:'var(--muted)' }}>Compact</span>
        </label>
      </div>
    </div>
  );
}
