export default function Header() {
  return (
    <header style={{ padding: 16, borderBottom: '1px solid #e5e7eb', display: 'flex', gap: 12, alignItems: 'center', background: '#0a2540', color: 'white' }}>
      <img src="/rr-white-trans.png" alt="RainRef" height={28} />
      <div>
        <h1 style={{ margin: 0, fontSize: 20, fontWeight: 700 }}>RainRef</h1>
        <p style={{ margin: 0, fontSize: 12, opacity: 0.9 }}>The Ref for answers, safe actions, and clear signals.</p>
      </div>
    </header>
  );
}
