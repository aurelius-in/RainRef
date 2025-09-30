export default function Spinner() {
  return (
    <div style={{ display:'inline-flex', alignItems:'center', gap:8, opacity: 0.7 }} aria-live="polite" aria-busy="true">
      <svg width="16" height="16" viewBox="0 0 24 24" role="img" aria-label="Loading">
        <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="2" fill="none" opacity="0.25" />
        <path d="M22 12a10 10 0 0 1-10 10" stroke="currentColor" strokeWidth="2" fill="none" />
      </svg>
      <span>Loading...</span>
    </div>
  );
}
