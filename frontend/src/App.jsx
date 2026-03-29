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
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <main className="max-w-7xl mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<HotelsPage />} />
            <Route path="/rooms" element={<RoomsPage />} />
            <Route path="/guests" element={<GuestsPage />} />
            <Route path="/bookings" element={<BookingsPage />} />
            <Route path="/payments" element={<PaymentsPage />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}
