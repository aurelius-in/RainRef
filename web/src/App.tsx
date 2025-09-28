import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import Header from "./components/Header";
import Inbox from "./pages/Inbox";
import EventDetail from "./pages/EventDetail";

export default function App() {
  return (
    <BrowserRouter>
      <Header />
      <main style={{ padding: 16 }}>
        <nav style={{ marginBottom: 12 }}>
          <Link to="/">Inbox</Link>
        </nav>
        <Routes>
          <Route path="/" element={<Inbox />} />
          <Route path="/events/:id" element={<EventDetail />} />
        </Routes>
      </main>
    </BrowserRouter>
  );
}
