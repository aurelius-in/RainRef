import { BrowserRouter, Routes, Route, Link, useLocation, useNavigate } from "react-router-dom";
import { useEffect, useRef } from "react";
import Header from "./components/Header";
import ErrorBoundary from "./components/ErrorBoundary";
import Inbox from "./pages/Inbox";
import EventDetail from "./pages/EventDetail";
import Kb from "./pages/Kb";
import KbDetail from "./pages/KbDetail";
import KbEdit from "./pages/KbEdit";
import Health from "./pages/Health";
import Signals from "./pages/Signals";
import Audit from "./pages/Audit";
import Actions from "./pages/Actions";
import Answer from "./pages/Answer";
import Tickets from "./pages/Tickets";
import Settings from "./pages/Settings";
import Metrics from "./pages/Metrics";
import About from "./pages/About";
import NotFound from "./pages/NotFound";
import Playbooks from "./pages/Playbooks";
import AuditDetail from "./pages/AuditDetail";

export default function App() {
  return (
    <BrowserRouter>
      <ErrorBoundary>
        <Splash />
        <Header />
        <div className="app-shell">
          <aside className="left-rail ref-stripes" aria-label="Primary navigation">
            <nav style={{ display:'flex', flexDirection:'column', gap:12, padding: 0 }}>
              <Link to="/">Events</Link>
              <Link to="/events/current">Answer</Link>
              <Link to="/signals">Signals</Link>
              <Link to="/kb">KB</Link>
              <Link to="/audit">Receipts</Link>
              <Link to="/playbooks">Playbooks</Link>
              <Link to="/settings">Settings</Link>
            </nav>
          </aside>
          <main className="main">
            <Routes>
              <Route path="/" element={<Inbox />} />
              <Route path="/kb" element={<Kb />} />
              <Route path="/kb/new" element={<KbEdit />} />
              <Route path="/kb/:id" element={<KbDetail />} />
              <Route path="/kb/:id/edit" element={<KbEdit />} />
              <Route path="/tickets" element={<Tickets />} />
              <Route path="/actions" element={<Actions />} />
              <Route path="/signals" element={<Signals />} />
              <Route path="/audit" element={<Audit />} />
              <Route path="/playbooks" element={<Playbooks />} />
              <Route path="/events/current" element={<Answer />} />
              <Route path="/health" element={<Health />} />
              <Route path="/metrics" element={<Metrics />} />
              <Route path="/settings" element={<Settings />} />
              <Route path="/about" element={<About />} />
              <Route path="*" element={<NotFound />} />
            </Routes>
          </main>
          <Drawer>
            <Routes>
              <Route path="/events/:id" element={<EventDetail />} />
              <Route path="/audit/:id" element={<AuditDetail />} />
            </Routes>
          </Drawer>
        </div>
      </ErrorBoundary>
    </BrowserRouter>
  );
}

function Drawer({ children }: { children: React.ReactNode }) {
  const ref = useRef<HTMLDivElement>(null);
  const navigate = useNavigate();
  const location = useLocation();
  const hasDrawer = (/^\/events\/(?!current)([^\/]+)$/.test(location.pathname)) || (/^\/audit\/(.+)$/.test(location.pathname));

  useEffect(() => {
    if (!hasDrawer) return;
    const root = ref.current;
    if (!root) return;
    const focusables = getFocusables(root);
    (focusables[0] as HTMLElement | undefined)?.focus?.();
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        e.preventDefault();
        navigate(-1);
      } else if (e.key === 'Tab') {
        const els = getFocusables(root);
        if (!els.length) return;
        const active = document.activeElement as HTMLElement | null;
        const idx = Math.max(0, els.indexOf(active as any));
        if (e.shiftKey) {
          const prev = els[(idx + els.length - 1) % els.length] as HTMLElement;
          prev.focus();
        } else {
          const next = els[(idx + 1) % els.length] as HTMLElement;
          next.focus();
        }
        e.preventDefault();
      }
    };
    root.addEventListener('keydown', onKey);
    return () => root.removeEventListener('keydown', onKey);
  }, [hasDrawer, navigate]);

  return (
    <aside
      ref={ref}
      className="drawer"
      aria-label="Detail drawer"
      role="dialog"
      aria-modal="true"
      tabIndex={-1}
      style={{ padding: 12, overflowY:'auto', display:'flex', flexDirection:'column' }}
    >
      {children}
      {hasDrawer && (
        <div style={{ display:'flex', justifyContent:'flex-end', marginTop:12 }}>
          <button onClick={()=>navigate(-1)} aria-label="Close">Close</button>
        </div>
      )}
    </aside>
  );
}

function getFocusables(root: HTMLElement) {
  const selectors = [
    'a[href]','button','input','select','textarea','[tabindex]:not([tabindex="-1"])'
  ];
  const nodes = Array.from(root.querySelectorAll<HTMLElement>(selectors.join(',')));
  return nodes.filter(el => !el.hasAttribute('disabled') && el.tabIndex !== -1);
}

function Splash() {
  const splashRef = useRef<HTMLDivElement | null>(null);
  const scheduledRef = useRef<boolean>(false);
  useEffect(() => {
    const cover = document.getElementById('rr-splash-cover');
    const logo = document.getElementById('rr-splash-logo') as HTMLImageElement | null;
    const schedule = () => {
      if (scheduledRef.current) return; // prevent double schedule
      scheduledRef.current = true;
      const t1 = window.setTimeout(() => { cover?.classList.add('fill'); }, 5000);
      const t2 = window.setTimeout(() => { splashRef.current?.classList.add('fade'); }, 5900);
      // cleanup
      return () => { window.clearTimeout(t1); window.clearTimeout(t2); };
    };
    let cleanup: (() => void) | undefined;
    if (logo) {
      if (logo.complete) {
        cleanup = schedule() || undefined;
      } else {
        const onLoad = () => { cleanup = schedule() || undefined; };
        logo.addEventListener('load', onLoad, { once: true });
        // Fallback in case load doesn't fire (cached or error)
        const t = window.setTimeout(() => { cleanup = schedule() || undefined; }, 300);
        cleanup = () => { window.clearTimeout(t); };
      }
    } else {
      cleanup = schedule() || undefined;
    }
    return () => { cleanup && cleanup(); };
  }, []);
  return (
    <div ref={splashRef} className="splash-overlay">
      <img id="rr-splash-logo" src="/rr-white-trans.png" alt="RainRef" className="splash-logo" />
      <div id="rr-splash-cover" className="splash-cover" />
    </div>
  );
}
