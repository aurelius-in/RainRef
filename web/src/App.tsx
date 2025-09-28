import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import Header from "./components/Header";
import ErrorBoundary from "./components/ErrorBoundary";
import Inbox from "./pages/Inbox";
import EventDetail from "./pages/EventDetail";
import Kb from "./pages/Kb";
import KbDetail from "./pages/KbDetail";
import Health from "./pages/Health";
import Signals from "./pages/Signals";
import Audit from "./pages/Audit";
import Actions from "./pages/Actions";
import Settings from "./pages/Settings";
import Tickets from "./pages/Tickets";
import NotFound from "./pages/NotFound";

export default function App() {
  return (
    <BrowserRouter>
      <ErrorBoundary>
        <Header />
        <main style={{ padding: 16 }}>
          <nav style={{ marginBottom: 12, display: 'flex', gap: 12, flexWrap: 'wrap' }}>
            <Link to="/">Inbox</Link>
            <Link to="/kb">Knowledge</Link>
            <Link to="/tickets">Tickets</Link>
            <Link to="/actions">Actions</Link>
            <Link to="/signals">Signals</Link>
            <Link to="/audit">Audit</Link>
            <Link to="/health">Health</Link>
            <Link to="/settings">Settings</Link>
          </nav>
          <Routes>
            <Route path="/" element={<Inbox />} />
            <Route path="/events/:id" element={<EventDetail />} />
            <Route path="/kb" element={<Kb />} />
            <Route path="/kb/:id" element={<KbDetail />} />
            <Route path="/tickets" element={<Tickets />} />
            <Route path="/actions" element={<Actions />} />
            <Route path="/signals" element={<Signals />} />
            <Route path="/audit" element={<Audit />} />
            <Route path="/health" element={<Health />} />
            <Route path="/settings" element={<Settings />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </main>
      </ErrorBoundary>
    </BrowserRouter>
  );
}
