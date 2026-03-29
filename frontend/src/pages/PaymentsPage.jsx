import { useState, useEffect } from "react";
import { getPayments, createPayment, updatePayment, deletePayment } from "../api/api";

const emptyForm = { booking_id: "", amount: "", method: "card", status: "pending" };

export default function PaymentsPage() {
  const [payments, setPayments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [showForm, setShowForm] = useState(false);
  const [editing, setEditing] = useState(null);
  const [form, setForm] = useState(emptyForm);

  const fetchPayments = async () => {
    setLoading(true);
    try {
      const res = await getPayments();
      setPayments(res.data);
      setError("");
    } catch { setError("Failed to load payments. Is the backend running?"); }
    setLoading(false);
  };

  useEffect(() => { fetchPayments(); }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    const data = { ...form, booking_id: Number(form.booking_id), amount: Number(form.amount) };
    try {
      if (editing) await updatePayment(editing, data);
      else await createPayment(data);
      setShowForm(false); setEditing(null); setForm(emptyForm); fetchPayments();
    } catch (err) { setError(err.response?.data?.detail || "Failed to save payment"); }
  };

  const handleEdit = (p) => { setForm({ ...p }); setEditing(p.id); setShowForm(true); };
  const handleDelete = async (id) => {
    if (!confirm("Delete this payment?")) return;
    try { await deletePayment(id); fetchPayments(); } catch { setError("Failed to delete"); }
  };

  const statusColor = (s) => {
    if (s === "paid") return "bg-green-100 text-green-700";
    if (s === "failed") return "bg-red-100 text-red-700";
    return "bg-yellow-100 text-yellow-700";
  };

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Payments</h1>
        <button onClick={() => { setForm(emptyForm); setEditing(null); setShowForm(!showForm); }}
          className="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 transition">
          {showForm ? "Cancel" : "+ Add Payment"}
        </button>
      </div>

      {error && <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-4">{error}</div>}

      {showForm && (
        <form onSubmit={handleSubmit} className="bg-white border border-gray-200 rounded-xl p-6 mb-6 shadow-sm">
          <h2 className="text-lg font-semibold mb-4">{editing ? "Edit Payment" : "Add New Payment"}</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-medium text-gray-600 mb-1">Booking ID</label>
              <input type="number" value={form.booking_id}
                onChange={(e) => setForm({ ...form, booking_id: e.target.value })}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm" required />
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-600 mb-1">Amount ($)</label>
              <input type="number" step="0.01" min="0" value={form.amount}
                onChange={(e) => setForm({ ...form, amount: e.target.value })}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm" required />
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-600 mb-1">Method</label>
              <select value={form.method} onChange={(e) => setForm({ ...form, method: e.target.value })}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm">
                <option value="card">Card</option>
                <option value="cash">Cash</option>
                <option value="online">Online</option>
              </select>
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-600 mb-1">Status</label>
              <select value={form.status} onChange={(e) => setForm({ ...form, status: e.target.value })}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm">
                <option value="pending">Pending</option>
                <option value="paid">Paid</option>
                <option value="failed">Failed</option>
              </select>
            </div>
          </div>
          <button type="submit" className="mt-4 bg-indigo-600 text-white px-6 py-2 rounded-lg hover:bg-indigo-700">
            {editing ? "Update Payment" : "Create Payment"}
          </button>
        </form>
      )}

      {loading ? <p className="text-gray-500">Loading...</p> : payments.length === 0 ? <p className="text-gray-500">No payments found.</p> : (
        <div className="overflow-x-auto">
          <table className="w-full bg-white border border-gray-200 rounded-xl shadow-sm text-sm">
            <thead className="bg-gray-50">
              <tr>
                {["ID", "Booking ID", "Amount", "Method", "Status", "Actions"].map((h) => (
                  <th key={h} className="px-4 py-3 text-left font-medium text-gray-600">{h}</th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {payments.map((p) => (
                <tr key={p.id} className="hover:bg-gray-50">
                  <td className="px-4 py-3">{p.id}</td>
                  <td className="px-4 py-3">{p.booking_id}</td>
                  <td className="px-4 py-3 font-medium">${p.amount}</td>
                  <td className="px-4 py-3 capitalize">{p.method}</td>
                  <td className="px-4 py-3">
                    <span className={`px-2 py-1 rounded-full text-xs ${statusColor(p.status)}`}>{p.status}</span>
                  </td>
                  <td className="px-4 py-3 flex gap-2">
                    <button onClick={() => handleEdit(p)} className="text-indigo-600 hover:underline text-xs">Edit</button>
                    <button onClick={() => handleDelete(p.id)} className="text-red-600 hover:underline text-xs">Delete</button>
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
