import { useState, useEffect } from "react";
import { getGuests, createGuest, updateGuest, deleteGuest } from "../api/api";

const emptyForm = { name: "", email: "", phone: "", nationality: "" };

export default function GuestsPage() {
  const [guests, setGuests] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [showForm, setShowForm] = useState(false);
  const [editing, setEditing] = useState(null);
  const [form, setForm] = useState(emptyForm);

  const fetchGuests = async () => {
    setLoading(true);
    try {
      const res = await getGuests();
      setGuests(res.data);
      setError("");
    } catch { setError("Failed to load guests. Is the backend running?"); }
    setLoading(false);
  };

  useEffect(() => { fetchGuests(); }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      if (editing) await updateGuest(editing, form);
      else await createGuest(form);
      setShowForm(false); setEditing(null); setForm(emptyForm); fetchGuests();
    } catch (err) { setError(err.response?.data?.detail || "Failed to save guest"); }
  };

  const handleEdit = (g) => { setForm({ ...g }); setEditing(g.id); setShowForm(true); };
  const handleDelete = async (id) => {
    if (!confirm("Delete this guest?")) return;
    try { await deleteGuest(id); fetchGuests(); } catch { setError("Failed to delete"); }
  };

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Guests</h1>
        <button onClick={() => { setForm(emptyForm); setEditing(null); setShowForm(!showForm); }}
          className="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 transition">
          {showForm ? "Cancel" : "+ Add Guest"}
        </button>
      </div>

      {error && <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-4">{error}</div>}

      {showForm && (
        <form onSubmit={handleSubmit} className="bg-white border border-gray-200 rounded-xl p-6 mb-6 shadow-sm">
          <h2 className="text-lg font-semibold mb-4">{editing ? "Edit Guest" : "Add New Guest"}</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {[
              { key: "name", label: "Full Name", type: "text" },
              { key: "email", label: "Email", type: "email" },
              { key: "phone", label: "Phone", type: "text" },
              { key: "nationality", label: "Nationality", type: "text" },
            ].map((f) => (
              <div key={f.key}>
                <label className="block text-xs font-medium text-gray-600 mb-1">{f.label}</label>
                <input type={f.type} value={form[f.key]}
                  onChange={(e) => setForm({ ...form, [f.key]: e.target.value })}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm" required />
              </div>
            ))}
          </div>
          <button type="submit" className="mt-4 bg-indigo-600 text-white px-6 py-2 rounded-lg hover:bg-indigo-700">
            {editing ? "Update Guest" : "Create Guest"}
          </button>
        </form>
      )}

      {loading ? <p className="text-gray-500">Loading...</p> : guests.length === 0 ? <p className="text-gray-500">No guests found.</p> : (
        <div className="overflow-x-auto">
          <table className="w-full bg-white border border-gray-200 rounded-xl shadow-sm text-sm">
            <thead className="bg-gray-50">
              <tr>
                {["ID", "Name", "Email", "Phone", "Nationality", "Actions"].map((h) => (
                  <th key={h} className="px-4 py-3 text-left font-medium text-gray-600">{h}</th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {guests.map((g) => (
                <tr key={g.id} className="hover:bg-gray-50">
                  <td className="px-4 py-3">{g.id}</td>
                  <td className="px-4 py-3 font-medium text-gray-900">{g.name}</td>
                  <td className="px-4 py-3">{g.email}</td>
                  <td className="px-4 py-3">{g.phone}</td>
                  <td className="px-4 py-3">{g.nationality}</td>
                  <td className="px-4 py-3 flex gap-2">
                    <button onClick={() => handleEdit(g)} className="text-indigo-600 hover:underline text-xs">Edit</button>
                    <button onClick={() => handleDelete(g.id)} className="text-red-600 hover:underline text-xs">Delete</button>
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
