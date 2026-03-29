import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import HotelsPage from "./pages/HotelsPage";
import RoomsPage from "./pages/RoomsPage";
import GuestsPage from "./pages/GuestsPage";
import BookingsPage from "./pages/BookingsPage";
import PaymentsPage from "./pages/PaymentsPage";

export default function App() {
  return (
    <BrowserRouter>
      <div style={{ minHeight: "100vh", background: "#e3f2fd" }}>
        <Navbar />
        <main style={{ maxWidth: 1280, margin: "0 auto", padding: "32px 24px" }}>
          <Routes>
            <Route path="/"         element={<HotelsPage />} />
            <Route path="/rooms"    element={<RoomsPage />} />
            <Route path="/guests"   element={<GuestsPage />} />
            <Route path="/bookings" element={<BookingsPage />} />
            <Route path="/payments" element={<PaymentsPage />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}