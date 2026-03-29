import { useState, useEffect } from "react";
import { getRooms, createRoom, updateRoom, deleteRoom } from "../api/api";

const emptyForm = { hotel_id: "", room_type: "", price_per_night: "", is_available: true };

export default function RoomsPage() {
  const [rooms, setRooms] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [showForm, setShowForm] = useState(false);
  const [editing, setEditing] = useState(null);
  const [form, setForm] = useState(emptyForm);

  const fetchRooms = async () => {
    setLoading(true);
    try {
      const res = await getRooms();
      setRooms(res.data);
      setError("");
    } catch { setError("Failed to load rooms. Is the backend running?"); }
    setLoading(false);
  };

  useEffect(() => { fetchRooms(); }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    const data = { ...form, hotel_id: Number(form.hotel_id), price_per_night: Number(form.price_per_night) };
    try {
      if (editing) await updateRoom(editing, data);
      else await createRoom(data);
      setShowForm(false); setEditing(null); setForm(emptyForm); fetchRooms();
    } catch (err) { setError(err.response?.data?.detail || "Failed to save room"); }
  };

  const handleEdit = (r) => { setForm({ ...r }); setEditing(r.id); setShowForm(true); };
  const handleDelete = async (id) => {
    if (!confirm("Delete this room?")) return;
    try { await deleteRoom(id); fetchRooms(); } catch { setError("Failed to delete"); }
  };

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Rooms</h1>
        <button onClick={() => { setForm(emptyForm); setEditing(null); setShowForm(!showForm); }}
          className="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 transition">
          {showForm ? "Cancel" : "+ Add Room"}
        </button>
      </div>

      {error && <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-4">{error}</div>}

      {showForm && (
        <form onSubmit={handleSubmit} className="bg-white border border-gray-200 rounded-xl p-6 mb-6 shadow-sm">
          <h2 className="text-lg font-semibold mb-4">{editing ? "Edit Room" : "Add New Room"}</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-medium text-gray-600 mb-1">Hotel ID</label>
              <input type="number" value={form.hotel_id} onChange={(e) => setForm({ ...form, hotel_id: e.target.value })}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm" required />
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-600 mb-1">Room Type</label>
              <select value={form.room_type} onChange={(e) => setForm({ ...form, room_type: e.target.value })}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm" required>
                <option value="">Select type</option>
                {["Single", "Double", "Suite", "Deluxe", "Penthouse"].map((t) => (
                  <option key={t} value={t}>{t}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-600 mb-1">Price/Night ($)</label>
              <input type="number" step="0.01" min="0" value={form.price_per_night}
                onChange={(e) => setForm({ ...form, price_per_night: e.target.value })}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm" required />
            </div>
            <div className="flex items-center gap-2 pt-5">
              <input type="checkbox" checked={form.is_available}
                onChange={(e) => setForm({ ...form, is_available: e.target.checked })} className="h-4 w-4" />
              <label className="text-sm text-gray-600">Available</label>
            </div>
          </div>
          <button type="submit" className="mt-4 bg-indigo-600 text-white px-6 py-2 rounded-lg hover:bg-indigo-700">
            {editing ? "Update Room" : "Create Room"}
          </button>
        </form>
      )}

      {loading ? <p className="text-gray-500">Loading...</p> : rooms.length === 0 ? <p className="text-gray-500">No rooms found.</p> : (
        <div className="overflow-x-auto">
          <table className="w-full bg-white border border-gray-200 rounded-xl shadow-sm text-sm">
            <thead className="bg-gray-50">
              <tr>
                {["ID", "Hotel ID", "Type", "Price/Night", "Available", "Actions"].map((h) => (
                  <th key={h} className="px-4 py-3 text-left font-medium text-gray-600">{h}</th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {rooms.map((r) => (
                <tr key={r.id} className="hover:bg-gray-50">
                  <td className="px-4 py-3">{r.id}</td>
                  <td className="px-4 py-3">{r.hotel_id}</td>
                  <td className="px-4 py-3 font-medium text-gray-900">{r.room_type}</td>
                  <td className="px-4 py-3">${r.price_per_night}</td>
                  <td className="px-4 py-3">
                    <span className={`px-2 py-1 rounded-full text-xs ${r.is_available ? "bg-green-100 text-green-700" : "bg-red-100 text-red-700"}`}>
                      {r.is_available ? "Yes" : "No"}
                    </span>
                  </td>
                  <td className="px-4 py-3 flex gap-2">
                    <button onClick={() => handleEdit(r)} className="text-indigo-600 hover:underline text-xs">Edit</button>
                    <button onClick={() => handleDelete(r.id)} className="text-red-600 hover:underline text-xs">Delete</button>
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
