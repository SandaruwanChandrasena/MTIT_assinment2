import { useState, useEffect } from "react";
import { getRooms, createRoom, updateRoom, deleteRoom } from "../api/api";
import { colors, btn, styles, inp, lbl, inputStyle, lblStyle, table, card, badge } from "../theme";

const emptyForm = { hotel_id: "", room_type: "", price_per_night: "", is_available: true };

export default function RoomsPage() {
  const [rooms, setRooms]       = useState([]);
  const [loading, setLoading]   = useState(true);
  const [error, setError]       = useState("");
  const [showForm, setShowForm] = useState(false);
  const [editing, setEditing]   = useState(null);
  const [form, setForm]         = useState(emptyForm);

  // Filters
  const [hotelIdFilter,    setHotelIdFilter]    = useState("");
  const [roomTypeFilter,   setRoomTypeFilter]   = useState("");
  const [availableFilter,  setAvailableFilter]  = useState("");
  const [minPrice,         setMinPrice]         = useState("");
  const [maxPrice,         setMaxPrice]         = useState("");
  const [skip, setSkip] = useState(0);
  const limit = 20;

  const fetchRooms = async () => {
    setLoading(true); setError("");
    try {
      const params = { skip, limit };
      if (hotelIdFilter)   params.hotel_id     = Number(hotelIdFilter);
      if (roomTypeFilter)  params.room_type     = roomTypeFilter;
      if (availableFilter !== "") params.is_available = availableFilter === "true";
      if (minPrice)        params.min_price     = Number(minPrice);
      if (maxPrice)        params.max_price     = Number(maxPrice);
      const res = await getRooms(params);
      setRooms(res.data);
    } catch { setError("Failed to load rooms. Is the backend running?"); }
    setLoading(false);
  };

  useEffect(() => { fetchRooms(); }, [skip]);

  const handleSubmit = async (e) => {
    e.preventDefault(); setError("");
    const data = { ...form, hotel_id: Number(form.hotel_id), price_per_night: Number(form.price_per_night) };
    try {
      editing ? await updateRoom(editing, data) : await createRoom(data);
      setShowForm(false); setEditing(null); setForm(emptyForm); fetchRooms();
    } catch (err) { setError(err.response?.data?.detail || "Failed to save room"); }
  };

  const handleEdit   = (r) => { setForm({ ...r }); setEditing(r.id); setShowForm(true); };
  const handleDelete = async (id) => {
    if (!confirm("Delete this room?")) return;
    try { await deleteRoom(id); fetchRooms(); } catch { setError("Failed to delete"); }
  };

  const handleSearch = () => { setSkip(0); fetchRooms(); };

  return (
    <div className="max-w-7xl mx-auto px-6 py-8">

      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold" style={{ color: colors.textPrimary }}>Rooms</h1>
          <p className="text-sm mt-0.5" style={{ color: colors.textSecondary }}>Manage room inventory</p>
        </div>
        <button onClick={() => { setForm(emptyForm); setEditing(null); setShowForm(!showForm); }}
          className={btn.primary} style={showForm ? styles.btnCancel : styles.btnPrimary}>
          {showForm ? "✕ Cancel" : "+ Add Room"}
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
        <input type="number" placeholder="Hotel ID..." value={hotelIdFilter}
          onChange={(e) => setHotelIdFilter(e.target.value)}
          className={`${inp} w-32`} style={inputStyle} />
        <select value={roomTypeFilter} onChange={(e) => setRoomTypeFilter(e.target.value)}
          className={`${inp} w-40`} style={inputStyle}>
          <option value="">All Types</option>
          {["Single","Double","Twin","Suite","Deluxe","Penthouse","Family","Studio","Executive","Presidential"].map(t => (
            <option key={t} value={t}>{t}</option>
          ))}
        </select>
        <select value={availableFilter} onChange={(e) => setAvailableFilter(e.target.value)}
          className={`${inp} w-40`} style={inputStyle}>
          <option value="">All Availability</option>
          <option value="true">Available</option>
          <option value="false">Booked</option>
        </select>
        <input type="number" placeholder="Min price..." value={minPrice}
          onChange={(e) => setMinPrice(e.target.value)}
          className={`${inp} w-32`} style={inputStyle} />
        <input type="number" placeholder="Max price..." value={maxPrice}
          onChange={(e) => setMaxPrice(e.target.value)}
          className={`${inp} w-32`} style={inputStyle} />
        <button onClick={handleSearch} className={btn.secondary} style={styles.btnSecondary}>
          Search
        </button>
        <button onClick={() => { setHotelIdFilter(""); setRoomTypeFilter(""); setAvailableFilter(""); setMinPrice(""); setMaxPrice(""); setSkip(0); setTimeout(fetchRooms, 0); }}
          className={btn.secondary} style={styles.btnGray}>
          Clear
        </button>
      </div>

      {/* Form */}
      {showForm && (
        <div className="bg-white border rounded-xl p-6 mb-6 shadow-sm" style={card}>
          <h2 className="text-base font-semibold mb-5" style={{ color: colors.textPrimary }}>
            {editing ? "✏️  Edit Room" : "➕  Add New Room"}
          </h2>
          <form onSubmit={handleSubmit}>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className={lbl} style={lblStyle}>Hotel ID</label>
                <input type="number" value={form.hotel_id}
                  onChange={(e) => setForm({ ...form, hotel_id: e.target.value })}
                  className={inp} style={inputStyle} required />
              </div>
              <div>
                <label className={lbl} style={lblStyle}>Room Type</label>
                <select value={form.room_type}
                  onChange={(e) => setForm({ ...form, room_type: e.target.value })}
                  className={inp} style={inputStyle} required>
                  <option value="">Select type</option>
                  {["Single","Double","Twin","Suite","Deluxe","Penthouse","Family","Studio","Executive","Presidential"].map(t => (
                    <option key={t} value={t}>{t}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className={lbl} style={lblStyle}>Price / Night ($)</label>
                <input type="number" step="0.01" min="0" value={form.price_per_night}
                  onChange={(e) => setForm({ ...form, price_per_night: e.target.value })}
                  className={inp} style={inputStyle} required />
              </div>
              <div className="flex items-center gap-2 pt-6">
                <input type="checkbox" id="available" checked={form.is_available}
                  onChange={(e) => setForm({ ...form, is_available: e.target.checked })}
                  className="h-4 w-4 rounded accent-blue-600" />
                <label htmlFor="available" className="text-sm" style={{ color: colors.textSecondary }}>
                  Available for booking
                </label>
              </div>
            </div>
            <div className="flex gap-3 mt-6">
              <button type="submit" className={btn.primary} style={styles.btnPrimary}>
                {editing ? "Update Room" : "Create Room"}
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
        <div className="text-center py-16 text-sm" style={{ color: colors.textMuted }}>Loading rooms...</div>
      ) : rooms.length === 0 ? (
        <div className="text-center py-16 text-sm" style={{ color: colors.textMuted }}>No rooms found.</div>
      ) : (
        <div className="bg-white border rounded-xl overflow-hidden shadow-sm" style={table.wrapper}>
          <table className="w-full text-sm">
            <thead>
              <tr style={table.head}>
                {["ID","Hotel ID","Room Type","Price / Night","Availability","Actions"].map(h => (
                  <th key={h} className="px-4 py-3 text-left text-xs font-semibold tracking-wide uppercase"
                    style={table.th}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {rooms.map((r, i) => (
                <tr key={r.id} className={table.rowHover} style={table.divider(i, rooms.length)}>
                  <td className="px-4 py-3 text-xs" style={{ color: colors.textMuted }}>{r.id}</td>
                  <td className="px-4 py-3" style={{ color: colors.textSecondary }}>{r.hotel_id}</td>
                  <td className="px-4 py-3">
                    <span className="px-2.5 py-0.5 rounded-full text-xs font-medium"
                      style={badge.roomType(r.room_type)}>{r.room_type}</span>
                  </td>
                  <td className="px-4 py-3 font-medium" style={{ color: colors.textPrimary }}>${r.price_per_night}</td>
                  <td className="px-4 py-3">
                    <span className="px-2 py-0.5 rounded-full text-xs font-medium"
                      style={r.is_available ? badge.available : badge.booked}>
                      {r.is_available ? "Available" : "Booked"}
                    </span>
                  </td>
                  <td className="px-4 py-3">
                    <div className="flex gap-1.5">
                      <button onClick={() => handleEdit(r)} className={btn.edit} style={styles.btnEdit}>Edit</button>
                      <button onClick={() => handleDelete(r.id)} className={btn.danger} style={styles.btnDelete}>Delete</button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Pagination */}
      {!loading && rooms.length > 0 && (
        <div className="flex items-center justify-center gap-3 mt-5">
          <button onClick={() => setSkip(Math.max(0, skip - limit))} disabled={skip === 0}
            className={btn.secondary} style={styles.btnGray}>← Previous</button>
          <span className="text-sm" style={{ color: colors.textSecondary }}>
            Showing {skip + 1}–{skip + rooms.length}
          </span>
          <button onClick={() => setSkip(skip + limit)} disabled={rooms.length < limit}
            className={btn.secondary} style={styles.btnGray}>Next →</button>
        </div>
      )}
    </div>
  );
}