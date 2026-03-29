import { useState, useEffect } from "react";
import { getHotels, createHotel, updateHotel, deleteHotel } from "../api/api";
import { colors, btn, styles, inp, lbl, inputStyle, lblStyle, table, card, badge } from "../theme";

const emptyForm = {
  name: "", description: "", address: "", city: "", country: "",
  phone: "", email: "", stars: 3, price_per_night: 0,
  amenities: "", rating: 0, image_url: "", is_active: true,
};

const fields = [
  { key: "name",            label: "Hotel Name",        type: "text"   },
  { key: "address",         label: "Address",           type: "text"   },
  { key: "city",            label: "City",              type: "text"   },
  { key: "country",         label: "Country",           type: "text"   },
  { key: "phone",           label: "Phone",             type: "text"   },
  { key: "email",           label: "Email",             type: "email"  },
  { key: "stars",           label: "Stars (1–5)",       type: "number", min: 1, max: 5 },
  { key: "price_per_night", label: "Price / Night ($)", type: "number", min: 0, step: "0.01" },
  { key: "rating",          label: "Rating (0–5)",      type: "number", min: 0, max: 5, step: "0.1" },
  { key: "image_url",       label: "Image URL",         type: "text",  optional: true },
];

export default function HotelsPage() {
  const [hotels, setHotels]       = useState([]);
  const [loading, setLoading]     = useState(true);
  const [error, setError]         = useState("");
  const [showForm, setShowForm]   = useState(false);
  const [editing, setEditing]     = useState(null);
  const [form, setForm]           = useState(emptyForm);
  const [search, setSearch]       = useState("");
  const [cityFilter, setCityFilter] = useState("");
  const [starsFilter, setStarsFilter] = useState("");
  const [skip, setSkip]           = useState(0);
  const limit = 20;

  const fetchHotels = async () => {
    setLoading(true); setError("");
    try {
      const params = { skip, limit };
      if (search)      params.search = search;
      if (cityFilter)  params.city   = cityFilter;
      if (starsFilter) params.stars  = starsFilter;
      const res = await getHotels(params);
      setHotels(res.data);
    } catch { setError("Failed to load hotels. Is the backend running?"); }
    setLoading(false);
  };

  useEffect(() => { fetchHotels(); }, [skip, starsFilter]);

  const handleSubmit = async (e) => {
    e.preventDefault(); setError("");
    try {
      const data = {
        ...form,
        stars:           Number(form.stars),
        price_per_night: Number(form.price_per_night),
        rating:          Number(form.rating),
        image_url:       form.image_url || null,
      };
      editing ? await updateHotel(editing, data) : await createHotel(data);
      setShowForm(false); setEditing(null); setForm(emptyForm); fetchHotels();
    } catch (err) { setError(err.response?.data?.detail || "Failed to save hotel"); }
  };

  const handleEdit   = (h) => { setForm({ ...h, image_url: h.image_url || "" }); setEditing(h.id); setShowForm(true); };
  const handleDelete = async (id) => {
    if (!confirm("Delete this hotel?")) return;
    try { await deleteHotel(id); fetchHotels(); } catch { setError("Failed to delete hotel"); }
  };

  return (
    <div className="max-w-7xl mx-auto px-6 py-8">

      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold" style={{ color: colors.textPrimary }}>Hotels</h1>
          <p className="text-sm mt-0.5" style={{ color: colors.textSecondary }}>Manage hotel listings</p>
        </div>
        <button onClick={() => { setForm(emptyForm); setEditing(null); setShowForm(!showForm); }}
          className={btn.primary}
          style={showForm ? styles.btnCancel : styles.btnPrimary}>
          {showForm ? "✕ Cancel" : "+ Add Hotel"}
        </button>
      </div>

      {/* Error */}
      {error && (
        <div className="flex items-center gap-2 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-5 text-sm">
          ⚠️ {typeof error === "object" ? JSON.stringify(error) : error}
        </div>
      )}

      {/* Search & Filters */}
      <div className="flex flex-wrap gap-3 mb-6 p-4 bg-white border rounded-xl" style={card}>
        <input type="text" placeholder="🔍  Search by name..." value={search}
          onChange={(e) => setSearch(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && fetchHotels()}
          className={`${inp} flex-1 min-w-45`} style={inputStyle} />
        <input type="text" placeholder="Filter by city..." value={cityFilter}
          onChange={(e) => setCityFilter(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && fetchHotels()}
          className={`${inp} w-44`} style={inputStyle} />
        <select value={starsFilter} onChange={(e) => setStarsFilter(e.target.value)}
          className={`${inp} w-36`} style={inputStyle}>
          <option value="">All Stars</option>
          {[1,2,3,4,5].map(s => <option key={s} value={s}>{s} Star{s > 1 && "s"}</option>)}
        </select>
        <button onClick={() => { setSkip(0); fetchHotels(); }}
          className={btn.secondary} style={styles.btnSecondary}>
          Search
        </button>
      </div>

      {/* Add / Edit Form */}
      {showForm && (
        <div className="bg-white border rounded-xl p-6 mb-6 shadow-sm" style={card}>
          <h2 className="text-base font-semibold mb-5" style={{ color: colors.textPrimary }}>
            {editing ? "✏️  Edit Hotel" : "➕  Add New Hotel"}
          </h2>
          <form onSubmit={handleSubmit}>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {fields.map((f) => (
                <div key={f.key}>
                  <label className={lbl} style={lblStyle}>{f.label}</label>
                  <input type={f.type} value={form[f.key]}
                    min={f.min} max={f.max} step={f.step}
                    onChange={(e) => setForm({ ...form, [f.key]: e.target.value })}
                    className={inp} style={inputStyle}
                    required={!f.optional} />
                </div>
              ))}
              <div>
                <label className={lbl} style={lblStyle}>Amenities</label>
                <input type="text" value={form.amenities} placeholder="WiFi, Pool, Gym..."
                  onChange={(e) => setForm({ ...form, amenities: e.target.value })}
                  className={inp} style={inputStyle} required />
              </div>
              <div>
                <label className={lbl} style={lblStyle}>Description</label>
                <input type="text" value={form.description}
                  onChange={(e) => setForm({ ...form, description: e.target.value })}
                  className={inp} style={inputStyle} required />
              </div>
              <div className="flex items-center gap-2 pt-6">
                <input type="checkbox" id="is_active" checked={form.is_active}
                  onChange={(e) => setForm({ ...form, is_active: e.target.checked })}
                  className="h-4 w-4 rounded accent-blue-600" />
                <label htmlFor="is_active" className="text-sm" style={{ color: colors.textSecondary }}>
                  Active (accepting bookings)
                </label>
              </div>
            </div>
            <div className="flex gap-3 mt-6">
              <button type="submit" className={btn.primary} style={styles.btnPrimary}>
                {editing ? "Update Hotel" : "Create Hotel"}
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
        <div className="text-center py-16 text-sm" style={{ color: colors.textMuted }}>Loading hotels...</div>
      ) : hotels.length === 0 ? (
        <div className="text-center py-16 text-sm" style={{ color: colors.textMuted }}>No hotels found.</div>
      ) : (
        <div className="bg-white border rounded-xl overflow-hidden shadow-sm" style={table.wrapper}>
          <table className="w-full text-sm">
            <thead>
              <tr style={table.head}>
                {["ID","Name","City","Country","Stars","Price/Night","Rating","Status","Actions"].map(h => (
                  <th key={h} className="px-4 py-3 text-left text-xs font-semibold tracking-wide uppercase"
                    style={table.th}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {hotels.map((h, i) => (
                <tr key={h.id} className={table.rowHover} style={table.divider(i, hotels.length)}>
                  <td className="px-4 py-3 text-xs" style={{ color: colors.textMuted }}>{h.id}</td>
                  <td className="px-4 py-3 font-medium" style={{ color: colors.textPrimary }}>{h.name}</td>
                  <td className="px-4 py-3" style={{ color: colors.textSecondary }}>{h.city}</td>
                  <td className="px-4 py-3" style={{ color: colors.textSecondary }}>{h.country}</td>
                  <td className="px-4 py-3" style={{ color: "#f59e0b" }}>{"★".repeat(h.stars)}</td>
                  <td className="px-4 py-3 font-medium" style={{ color: colors.textPrimary }}>${h.price_per_night}</td>
                  <td className="px-4 py-3" style={{ color: colors.textSecondary }}>{h.rating}/5</td>
                  <td className="px-4 py-3">
                    <span className="px-2 py-0.5 rounded-full text-xs font-medium"
                      style={h.is_active ? badge.active : badge.inactive}>
                      {h.is_active ? "Active" : "Inactive"}
                    </span>
                  </td>
                  <td className="px-4 py-3">
                    <div className="flex gap-1.5">
                      <button onClick={() => handleEdit(h)} className={btn.edit} style={styles.btnEdit}>Edit</button>
                      <button onClick={() => handleDelete(h.id)} className={btn.danger} style={styles.btnDelete}>Delete</button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Pagination */}
      {!loading && hotels.length > 0 && (
        <div className="flex items-center justify-center gap-3 mt-5">
          <button onClick={() => setSkip(Math.max(0, skip - limit))} disabled={skip === 0}
            className={btn.secondary} style={styles.btnGray}>← Previous</button>
          <span className="text-sm" style={{ color: colors.textSecondary }}>
            Showing {skip + 1}–{skip + hotels.length}
          </span>
          <button onClick={() => setSkip(skip + limit)} disabled={hotels.length < limit}
            className={btn.secondary} style={styles.btnGray}>Next →</button>
        </div>
      )}
    </div>
  );
}