import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import Header from "./components/Header";
import Inbox from "./pages/Inbox";
import EventDetail from "./pages/EventDetail";
import Kb from "./pages/Kb";

export default function App() {
  return (
    <BrowserRouter>
      <Header />
      <main style={{ padding: 16 }}>
        <nav style={{ marginBottom: 12, display: 'flex', gap: 12 }}>
          <Link to="/">Inbox</Link>
          <Link to="/kb">Knowledge</Link>
        </nav>
        <Routes>
          <Route path="/" element={<Inbox />} />
          <Route path="/events/:id" element={<EventDetail />} />
          <Route path="/kb" element={<Kb />} />
        </Routes>
      </main>
    </BrowserRouter>
  );
}
