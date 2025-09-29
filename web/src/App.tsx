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
        <Header />
        <div className="app-shell">
          <aside className="left-rail ref-stripes" aria-label="Primary navigation">
            <nav style={{ display:'flex', flexDirection:'column', gap:12, padding: 8 }}>
              <Link to="/">Inbox</Link>
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
  const hasDrawer = /\/events\//.test(location.pathname) || /\/audit\//.test(location.pathname);

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
      style={{ padding: 12, overflowY:'auto' }}
    >
      {hasDrawer && (
        <div style={{ display:'flex', justifyContent:'flex-end', marginBottom:8 }}>
          <button onClick={()=>navigate(-1)} aria-label="Close">Close</button>
        </div>
      )}
      {children}
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
