import { useState, useEffect } from "react";
import { getBookings, createBooking, updateBooking, deleteBooking } from "../api/api";
import { colors, btn, styles, inp, lbl, inputStyle, lblStyle, table, card, badge } from "../theme";

const emptyForm = { guest_id: "", room_id: "", check_in: "", check_out: "", status: "pending" };

export default function BookingsPage() {
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading]   = useState(true);
  const [error, setError]       = useState("");
  const [showForm, setShowForm] = useState(false);
  const [editing, setEditing]   = useState(null);
  const [form, setForm]         = useState(emptyForm);

  // Filters
  const [guestIdFilter,   setGuestIdFilter]   = useState("");
  const [roomIdFilter,    setRoomIdFilter]     = useState("");
  const [statusFilter,    setStatusFilter]     = useState("");
  const [checkInFrom,     setCheckInFrom]      = useState("");
  const [checkInTo,       setCheckInTo]        = useState("");
  const [skip, setSkip] = useState(0);
  const limit = 20;

  const fetchBookings = async () => {
    setLoading(true); setError("");
    try {
      const params = { skip, limit };
      if (guestIdFilter)  params.guest_id      = Number(guestIdFilter);
      if (roomIdFilter)   params.room_id        = Number(roomIdFilter);
      if (statusFilter)   params.status         = statusFilter;
      if (checkInFrom)    params.check_in_from  = checkInFrom;
      if (checkInTo)      params.check_in_to    = checkInTo;
      const res = await getBookings(params);
      setBookings(res.data);
    } catch { setError("Failed to load bookings. Is the backend running?"); }
    setLoading(false);
  };

  useEffect(() => { fetchBookings(); }, [skip]);

  const handleSubmit = async (e) => {
    e.preventDefault(); setError("");
    const data = { ...form, guest_id: Number(form.guest_id), room_id: Number(form.room_id) };
    try {
      editing ? await updateBooking(editing, data) : await createBooking(data);
      setShowForm(false); setEditing(null); setForm(emptyForm); fetchBookings();
    } catch (err) { setError(err.response?.data?.detail || "Failed to save booking"); }
  };

  const handleEdit   = (b) => { setForm({ ...b }); setEditing(b.id); setShowForm(true); };
  const handleDelete = async (id) => {
    if (!confirm("Delete this booking?")) return;
    try { await deleteBooking(id); fetchBookings(); } catch { setError("Failed to delete"); }
  };

  const handleSearch = () => { setSkip(0); fetchBookings(); };
  const handleClear  = () => {
    setGuestIdFilter(""); setRoomIdFilter(""); setStatusFilter("");
    setCheckInFrom(""); setCheckInTo(""); setSkip(0);
    setTimeout(fetchBookings, 0);
  };

  return (
    <div className="max-w-7xl mx-auto px-6 py-8">

      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold" style={{ color: colors.textPrimary }}>Bookings</h1>
          <p className="text-sm mt-0.5" style={{ color: colors.textSecondary }}>Manage reservations</p>
        </div>
        <button onClick={() => { setForm(emptyForm); setEditing(null); setShowForm(!showForm); }}
          className={btn.primary} style={showForm ? styles.btnCancel : styles.btnPrimary}>
          {showForm ? "✕ Cancel" : "+ Add Booking"}
        </button>
      </div>

      {/* Error */}
      {error && (
        <div className="flex items-center gap-2 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-5 text-sm">
          ⚠️ {error}
        </div>
      )}

      {/* Search & Filters */}
      <div className="flex flex-wrap gap-3 mb-6 p-4 bg-white border rounded-xl" style={card}>
        <input type="number" placeholder="Guest ID..." value={guestIdFilter}
          onChange={(e) => setGuestIdFilter(e.target.value)}
          className={`${inp} w-32`} style={inputStyle} />
        <input type="number" placeholder="Room ID..." value={roomIdFilter}
          onChange={(e) => setRoomIdFilter(e.target.value)}
          className={`${inp} w-32`} style={inputStyle} />
        <select value={statusFilter} onChange={(e) => setStatusFilter(e.target.value)}
          className={`${inp} w-40`} style={inputStyle}>
          <option value="">All Statuses</option>
          <option value="confirmed">Confirmed</option>
          <option value="pending">Pending</option>
          <option value="cancelled">Cancelled</option>
        </select>
        <div className="flex items-center gap-2">
          <label className="text-xs font-medium" style={{ color: colors.textSecondary }}>From</label>
          <input type="date" value={checkInFrom}
            onChange={(e) => setCheckInFrom(e.target.value)}
            className={`${inp} w-40`} style={inputStyle} />
        </div>
        <div className="flex items-center gap-2">
          <label className="text-xs font-medium" style={{ color: colors.textSecondary }}>To</label>
          <input type="date" value={checkInTo}
            onChange={(e) => setCheckInTo(e.target.value)}
            className={`${inp} w-40`} style={inputStyle} />
        </div>
        <button onClick={handleSearch} className={btn.secondary} style={styles.btnSecondary}>Search</button>
        <button onClick={handleClear}  className={btn.secondary} style={styles.btnGray}>Clear</button>
      </div>

      {/* Form */}
      {showForm && (
        <div className="bg-white border rounded-xl p-6 mb-6 shadow-sm" style={card}>
          <h2 className="text-base font-semibold mb-5" style={{ color: colors.textPrimary }}>
            {editing ? "✏️  Edit Booking" : "➕  Add New Booking"}
          </h2>
          <form onSubmit={handleSubmit}>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {[
                { key: "guest_id",  label: "Guest ID",       type: "number" },
                { key: "room_id",   label: "Room ID",        type: "number" },
                { key: "check_in",  label: "Check-in Date",  type: "date"   },
                { key: "check_out", label: "Check-out Date", type: "date"   },
              ].map((f) => (
                <div key={f.key}>
                  <label className={lbl} style={lblStyle}>{f.label}</label>
                  <input type={f.type} value={form[f.key]}
                    onChange={(e) => setForm({ ...form, [f.key]: e.target.value })}
                    className={inp} style={inputStyle} required />
                </div>
              ))}
              <div>
                <label className={lbl} style={lblStyle}>Status</label>
                <select value={form.status} onChange={(e) => setForm({ ...form, status: e.target.value })}
                  className={inp} style={inputStyle}>
                  <option value="pending">Pending</option>
                  <option value="confirmed">Confirmed</option>
                  <option value="cancelled">Cancelled</option>
                </select>
              </div>
            </div>
            <div className="flex gap-3 mt-6">
              <button type="submit" className={btn.primary} style={styles.btnPrimary}>
                {editing ? "Update Booking" : "Create Booking"}
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
        <div className="text-center py-16 text-sm" style={{ color: colors.textMuted }}>Loading bookings...</div>
      ) : bookings.length === 0 ? (
        <div className="text-center py-16 text-sm" style={{ color: colors.textMuted }}>No bookings found.</div>
      ) : (
        <div className="bg-white border rounded-xl overflow-hidden shadow-sm" style={table.wrapper}>
          <table className="w-full text-sm">
            <thead>
              <tr style={table.head}>
                {["ID","Guest ID","Room ID","Check-in","Check-out","Nights","Status","Actions"].map(h => (
                  <th key={h} className="px-4 py-3 text-left text-xs font-semibold tracking-wide uppercase"
                    style={table.th}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {bookings.map((b, i) => {
                const nights = Math.max(1, Math.ceil((new Date(b.check_out) - new Date(b.check_in)) / 86400000));
                return (
                  <tr key={b.id} className={table.rowHover} style={table.divider(i, bookings.length)}>
                    <td className="px-4 py-3 text-xs" style={{ color: colors.textMuted }}>{b.id}</td>
                    <td className="px-4 py-3" style={{ color: colors.textSecondary }}>{b.guest_id}</td>
                    <td className="px-4 py-3" style={{ color: colors.textSecondary }}>{b.room_id}</td>
                    <td className="px-4 py-3" style={{ color: colors.textPrimary }}>{b.check_in}</td>
                    <td className="px-4 py-3" style={{ color: colors.textPrimary }}>{b.check_out}</td>
                    <td className="px-4 py-3" style={{ color: colors.textSecondary }}>{nights}n</td>
                    <td className="px-4 py-3">
                      <span className="px-2 py-0.5 rounded-full text-xs font-medium capitalize"
                        style={badge[b.status] || badge.pending}>{b.status}</span>
                    </td>
                    <td className="px-4 py-3">
                      <div className="flex gap-1.5">
                        <button onClick={() => handleEdit(b)} className={btn.edit} style={styles.btnEdit}>Edit</button>
                        <button onClick={() => handleDelete(b.id)} className={btn.danger} style={styles.btnDelete}>Delete</button>
                      </div>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}

      {/* Pagination */}
      {!loading && bookings.length > 0 && (
        <div className="flex items-center justify-center gap-3 mt-5">
          <button onClick={() => setSkip(Math.max(0, skip - limit))} disabled={skip === 0}
            className={btn.secondary} style={styles.btnGray}>← Previous</button>
          <span className="text-sm" style={{ color: colors.textSecondary }}>
            Showing {skip + 1}–{skip + bookings.length}
          </span>
          <button onClick={() => setSkip(skip + limit)} disabled={bookings.length < limit}
            className={btn.secondary} style={styles.btnGray}>Next →</button>
        </div>
      )}
    </div>
  );
}