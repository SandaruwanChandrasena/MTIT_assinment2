import { useState, useEffect } from "react";
import { getBookings, createBooking, updateBooking, deleteBooking } from "../api/api";

const emptyForm = { guest_id: "", room_id: "", check_in: "", check_out: "", status: "pending" };

export default function BookingsPage() {
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [showForm, setShowForm] = useState(false);
  const [editing, setEditing] = useState(null);
  const [form, setForm] = useState(emptyForm);

  const fetchBookings = async () => {
    setLoading(true);
    try {
      const res = await getBookings();
      setBookings(res.data);
      setError("");
    } catch { setError("Failed to load bookings. Is the backend running?"); }
    setLoading(false);
  };

  useEffect(() => { fetchBookings(); }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    const data = { ...form, guest_id: Number(form.guest_id), room_id: Number(form.room_id) };
    try {
      if (editing) await updateBooking(editing, data);
      else await createBooking(data);
      setShowForm(false); setEditing(null); setForm(emptyForm); fetchBookings();
    } catch (err) { setError(err.response?.data?.detail || "Failed to save booking"); }
  };

  const handleEdit = (b) => { setForm({ ...b }); setEditing(b.id); setShowForm(true); };
  const handleDelete = async (id) => {
    if (!confirm("Delete this booking?")) return;
    try { await deleteBooking(id); fetchBookings(); } catch { setError("Failed to delete"); }
  };

  const statusColor = (s) => {
    if (s === "confirmed") return "bg-green-100 text-green-700";
    if (s === "cancelled") return "bg-red-100 text-red-700";
    return "bg-yellow-100 text-yellow-700";
  };

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Bookings</h1>
        <button onClick={() => { setForm(emptyForm); setEditing(null); setShowForm(!showForm); }}
          className="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 transition">
          {showForm ? "Cancel" : "+ Add Booking"}
        </button>
      </div>

      {error && <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-4">{error}</div>}

      {showForm && (
        <form onSubmit={handleSubmit} className="bg-white border border-gray-200 rounded-xl p-6 mb-6 shadow-sm">
          <h2 className="text-lg font-semibold mb-4">{editing ? "Edit Booking" : "Add New Booking"}</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div>
              <label className="block text-xs font-medium text-gray-600 mb-1">Guest ID</label>
              <input type="number" value={form.guest_id}
                onChange={(e) => setForm({ ...form, guest_id: e.target.value })}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm" required />
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-600 mb-1">Room ID</label>
              <input type="number" value={form.room_id}
                onChange={(e) => setForm({ ...form, room_id: e.target.value })}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm" required />
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-600 mb-1">Check-in Date</label>
              <input type="date" value={form.check_in}
                onChange={(e) => setForm({ ...form, check_in: e.target.value })}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm" required />
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-600 mb-1">Check-out Date</label>
              <input type="date" value={form.check_out}
                onChange={(e) => setForm({ ...form, check_out: e.target.value })}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm" required />
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-600 mb-1">Status</label>
              <select value={form.status} onChange={(e) => setForm({ ...form, status: e.target.value })}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm">
                <option value="pending">Pending</option>
                <option value="confirmed">Confirmed</option>
                <option value="cancelled">Cancelled</option>
              </select>
            </div>
          </div>
          <button type="submit" className="mt-4 bg-indigo-600 text-white px-6 py-2 rounded-lg hover:bg-indigo-700">
            {editing ? "Update Booking" : "Create Booking"}
          </button>
        </form>
      )}

      {loading ? <p className="text-gray-500">Loading...</p> : bookings.length === 0 ? <p className="text-gray-500">No bookings found.</p> : (
        <div className="overflow-x-auto">
          <table className="w-full bg-white border border-gray-200 rounded-xl shadow-sm text-sm">
            <thead className="bg-gray-50">
              <tr>
                {["ID", "Guest ID", "Room ID", "Check-in", "Check-out", "Status", "Actions"].map((h) => (
                  <th key={h} className="px-4 py-3 text-left font-medium text-gray-600">{h}</th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {bookings.map((b) => (
                <tr key={b.id} className="hover:bg-gray-50">
                  <td className="px-4 py-3">{b.id}</td>
                  <td className="px-4 py-3">{b.guest_id}</td>
                  <td className="px-4 py-3">{b.room_id}</td>
                  <td className="px-4 py-3">{b.check_in}</td>
                  <td className="px-4 py-3">{b.check_out}</td>
                  <td className="px-4 py-3">
                    <span className={`px-2 py-1 rounded-full text-xs ${statusColor(b.status)}`}>{b.status}</span>
                  </td>
                  <td className="px-4 py-3 flex gap-2">
                    <button onClick={() => handleEdit(b)} className="text-indigo-600 hover:underline text-xs">Edit</button>
                    <button onClick={() => handleDelete(b.id)} className="text-red-600 hover:underline text-xs">Delete</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
