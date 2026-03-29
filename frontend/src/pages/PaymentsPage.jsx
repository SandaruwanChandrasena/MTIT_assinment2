import { useState, useEffect } from "react";
import { getPayments, createPayment, updatePayment, deletePayment } from "../api/api";
import { colors, btn, styles, inp, lbl, inputStyle, lblStyle, table, card, badge } from "../theme";

const emptyForm = { booking_id: "", amount: "", method: "card", status: "pending" };

export default function PaymentsPage() {
  const [payments, setPayments] = useState([]);
  const [loading, setLoading]   = useState(true);
  const [error, setError]       = useState("");
  const [showForm, setShowForm] = useState(false);
  const [editing, setEditing]   = useState(null);
  const [form, setForm]         = useState(emptyForm);

  // Filters
  const [bookingIdFilter, setBookingIdFilter] = useState("");
  const [statusFilter,    setStatusFilter]    = useState("");
  const [methodFilter,    setMethodFilter]    = useState("");
  const [minAmount,       setMinAmount]       = useState("");
  const [maxAmount,       setMaxAmount]       = useState("");
  const [skip, setSkip] = useState(0);
  const limit = 20;

  const fetchPayments = async () => {
    setLoading(true); setError("");
    try {
      const params = { skip, limit };
      if (bookingIdFilter) params.booking_id = Number(bookingIdFilter);
      if (statusFilter)    params.status     = statusFilter;
      if (methodFilter)    params.method     = methodFilter;
      if (minAmount)       params.min_amount = Number(minAmount);
      if (maxAmount)       params.max_amount = Number(maxAmount);
      const res = await getPayments(params);
      setPayments(res.data);
    } catch { setError("Failed to load payments. Is the backend running?"); }
    setLoading(false);
  };

  useEffect(() => { fetchPayments(); }, [skip]);

  const handleSubmit = async (e) => {
    e.preventDefault(); setError("");
    const data = { ...form, booking_id: Number(form.booking_id), amount: Number(form.amount) };
    try {
      editing ? await updatePayment(editing, data) : await createPayment(data);
      setShowForm(false); setEditing(null); setForm(emptyForm); fetchPayments();
    } catch (err) { setError(err.response?.data?.detail || "Failed to save payment"); }
  };

  const handleEdit   = (p) => { setForm({ ...p }); setEditing(p.id); setShowForm(true); };
  const handleDelete = async (id) => {
    if (!confirm("Delete this payment?")) return;
    try { await deletePayment(id); fetchPayments(); } catch { setError("Failed to delete"); }
  };

  const handleSearch = () => { setSkip(0); fetchPayments(); };
  const handleClear  = () => {
    setBookingIdFilter(""); setStatusFilter(""); setMethodFilter("");
    setMinAmount(""); setMaxAmount(""); setSkip(0);
    setTimeout(fetchPayments, 0);
  };

  const totalRevenue = payments.filter(p => p.status === "paid").reduce((s, p) => s + p.amount, 0);
  const pending      = payments.filter(p => p.status === "pending").length;
  const failed       = payments.filter(p => p.status === "failed").length;

  const summaryCards = [
    { label: "Total Revenue", value: `$${totalRevenue.toLocaleString("en-US", { minimumFractionDigits: 2 })}`, style: { background: colors.primaryLight, borderColor: colors.primaryBorder, color: colors.primaryText } },
    { label: "Pending",       value: pending, style: { background: "#fefce8", borderColor: "#fde68a", color: "#854d0e" } },
    { label: "Failed",        value: failed,  style: { background: "#fff1f2", borderColor: "#fecdd3", color: "#be123c" } },
  ];

  return (
    <div className="max-w-7xl mx-auto px-6 py-8">

      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold" style={{ color: colors.textPrimary }}>Payments</h1>
          <p className="text-sm mt-0.5" style={{ color: colors.textSecondary }}>Track payment transactions</p>
        </div>
        <button onClick={() => { setForm(emptyForm); setEditing(null); setShowForm(!showForm); }}
          className={btn.primary} style={showForm ? styles.btnCancel : styles.btnPrimary}>
          {showForm ? "✕ Cancel" : "+ Add Payment"}
        </button>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-3 gap-4 mb-6">
        {summaryCards.map((s) => (
          <div key={s.label} className="rounded-xl p-4 border" style={s.style}>
            <p className="text-xs font-semibold uppercase tracking-wide mb-1">{s.label}</p>
            <p className="text-2xl font-bold">{s.value}</p>
          </div>
        ))}
      </div>

      {/* Error */}
      {error && (
        <div className="flex items-center gap-2 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-5 text-sm">
          ⚠️ {error}
        </div>
      )}

      {/* Search & Filters */}
      <div className="flex flex-wrap gap-3 mb-6 p-4 bg-white border rounded-xl" style={card}>
        <input type="number" placeholder="Booking ID..." value={bookingIdFilter}
          onChange={(e) => setBookingIdFilter(e.target.value)}
          className={`${inp} w-36`} style={inputStyle} />
        <select value={statusFilter} onChange={(e) => setStatusFilter(e.target.value)}
          className={`${inp} w-36`} style={inputStyle}>
          <option value="">All Statuses</option>
          <option value="paid">Paid</option>
          <option value="pending">Pending</option>
          <option value="failed">Failed</option>
        </select>
        <select value={methodFilter} onChange={(e) => setMethodFilter(e.target.value)}
          className={`${inp} w-36`} style={inputStyle}>
          <option value="">All Methods</option>
          <option value="card">💳 Card</option>
          <option value="cash">💵 Cash</option>
          <option value="online">🌐 Online</option>
        </select>
        <input type="number" placeholder="Min amount..." value={minAmount}
          onChange={(e) => setMinAmount(e.target.value)}
          className={`${inp} w-32`} style={inputStyle} />
        <input type="number" placeholder="Max amount..." value={maxAmount}
          onChange={(e) => setMaxAmount(e.target.value)}
          className={`${inp} w-32`} style={inputStyle} />
        <button onClick={handleSearch} className={btn.secondary} style={styles.btnSecondary}>Search</button>
        <button onClick={handleClear}  className={btn.secondary} style={styles.btnGray}>Clear</button>
      </div>

      {/* Form */}
      {showForm && (
        <div className="bg-white border rounded-xl p-6 mb-6 shadow-sm" style={card}>
          <h2 className="text-base font-semibold mb-5" style={{ color: colors.textPrimary }}>
            {editing ? "✏️  Edit Payment" : "➕  Add New Payment"}
          </h2>
          <form onSubmit={handleSubmit}>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className={lbl} style={lblStyle}>Booking ID</label>
                <input type="number" value={form.booking_id}
                  onChange={(e) => setForm({ ...form, booking_id: e.target.value })}
                  className={inp} style={inputStyle} required />
              </div>
              <div>
                <label className={lbl} style={lblStyle}>Amount ($)</label>
                <input type="number" step="0.01" min="0" value={form.amount}
                  onChange={(e) => setForm({ ...form, amount: e.target.value })}
                  className={inp} style={inputStyle} required />
              </div>
              <div>
                <label className={lbl} style={lblStyle}>Payment Method</label>
                <select value={form.method} onChange={(e) => setForm({ ...form, method: e.target.value })}
                  className={inp} style={inputStyle}>
                  <option value="card">💳 Card</option>
                  <option value="cash">💵 Cash</option>
                  <option value="online">🌐 Online</option>
                </select>
              </div>
              <div>
                <label className={lbl} style={lblStyle}>Status</label>
                <select value={form.status} onChange={(e) => setForm({ ...form, status: e.target.value })}
                  className={inp} style={inputStyle}>
                  <option value="pending">Pending</option>
                  <option value="paid">Paid</option>
                  <option value="failed">Failed</option>
                </select>
              </div>
            </div>
            <div className="flex gap-3 mt-6">
              <button type="submit" className={btn.primary} style={styles.btnPrimary}>
                {editing ? "Update Payment" : "Create Payment"}
              </button>
              <button type="button" className={btn.secondary} style={styles.btnGray}
                onClick={() => { setShowForm(false); setEditing(null); }}>
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Table */}
      {loading ? (
        <div className="text-center py-16 text-sm" style={{ color: colors.textMuted }}>Loading payments...</div>
      ) : payments.length === 0 ? (
        <div className="text-center py-16 text-sm" style={{ color: colors.textMuted }}>No payments found.</div>
      ) : (
        <div className="bg-white border rounded-xl overflow-hidden shadow-sm" style={table.wrapper}>
          <table className="w-full text-sm">
            <thead>
              <tr style={table.head}>
                {["ID","Booking ID","Amount","Method","Status","Actions"].map(h => (
                  <th key={h} className="px-4 py-3 text-left text-xs font-semibold tracking-wide uppercase"
                    style={table.th}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {payments.map((p, i) => (
                <tr key={p.id} className={table.rowHover} style={table.divider(i, payments.length)}>
                  <td className="px-4 py-3 text-xs" style={{ color: colors.textMuted }}>{p.id}</td>
                  <td className="px-4 py-3" style={{ color: colors.textSecondary }}>{p.booking_id}</td>
                  <td className="px-4 py-3 font-semibold" style={{ color: colors.textPrimary }}>${p.amount.toLocaleString()}</td>
                  <td className="px-4 py-3">
                    <span className="px-2 py-0.5 rounded-full text-xs font-medium capitalize"
                      style={badge[p.method] || badge.cash}>
                      {{ card: "💳", cash: "💵", online: "🌐" }[p.method]} {p.method}
                    </span>
                  </td>
                  <td className="px-4 py-3">
                    <span className="px-2 py-0.5 rounded-full text-xs font-medium capitalize"
                      style={badge[p.status] || badge.pending}>{p.status}</span>
                  </td>
                  <td className="px-4 py-3">
                    <div className="flex gap-1.5">
                      <button onClick={() => handleEdit(p)} className={btn.edit} style={styles.btnEdit}>Edit</button>
                      <button onClick={() => handleDelete(p.id)} className={btn.danger} style={styles.btnDelete}>Delete</button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Pagination */}
      {!loading && payments.length > 0 && (
        <div className="flex items-center justify-center gap-3 mt-5">
          <button onClick={() => setSkip(Math.max(0, skip - limit))} disabled={skip === 0}
            className={btn.secondary} style={styles.btnGray}>← Previous</button>
          <span className="text-sm" style={{ color: colors.textSecondary }}>
            Showing {skip + 1}–{skip + payments.length}
          </span>
          <button onClick={() => setSkip(skip + limit)} disabled={payments.length < limit}
            className={btn.secondary} style={styles.btnGray}>Next →</button>
        </div>
      )}
    </div>
  );
}