export default function Header() {
  return (
    <header style={{ padding: 16, borderBottom: '1px solid #eee', display: 'flex', gap: 12, alignItems: 'center' }}>
      <img src="/rr-black-trans.png" alt="RainRef" height={32} />
      <div>
        <h1 style={{ margin: 0, fontSize: 20, fontWeight: 700 }}>RainRef</h1>
        <p style={{ margin: 0, fontSize: 12, opacity: 0.8 }}>The Ref for answers, safe actions, and clear signals.</p>
      </div>
    </header>
  );
}
