import { useState, useEffect } from "react";
import { getGuests, createGuest, updateGuest, deleteGuest } from "../api/api";
import {
  colors,
  btn,
  styles,
  inp,
  lbl,
  inputStyle,
  lblStyle,
  table,
  card,
  badge,
  avatar,
} from "../theme";

const emptyForm = { name: "", email: "", phone: "", nationality: "" };

export default function GuestsPage() {
  const [guests, setGuests] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [showForm, setShowForm] = useState(false);
  const [editing, setEditing] = useState(null);
  const [form, setForm] = useState(emptyForm);

  // Filters
  const [search, setSearch] = useState("");
  const [nationality, setNationality] = useState("");
  const [skip, setSkip] = useState(0);
  const limit = 20;

  const fetchGuests = async () => {
    setLoading(true);
    setError("");
    try {
      const params = { skip, limit };
      if (search) params.search = search;
      if (nationality) params.nationality = nationality;
      const res = await getGuests(params);
      setGuests(res.data);
    } catch {
      setError("Failed to load guests. Is the backend running?");
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchGuests();
  }, [skip]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      editing ? await updateGuest(editing, form) : await createGuest(form);
      setShowForm(false);
      setEditing(null);
      setForm(emptyForm);
      fetchGuests();
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to save guest");
    }
  };

  const handleEdit = (g) => {
    setForm({ ...g });
    setEditing(g.id);
    setShowForm(true);
  };
  const handleDelete = async (id) => {
    if (!confirm("Delete this guest?")) return;
    try {
      await deleteGuest(id);
      fetchGuests();
    } catch {
      setError("Failed to delete");
    }
  };

  const handleSearch = () => {
    setSkip(0);
    fetchGuests();
  };

  return (
    <div className="max-w-7xl mx-auto px-6 py-8">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1
            className="text-2xl font-bold"
            style={{ color: colors.textPrimary }}
          >
            Guests
          </h1>
          <p className="text-sm mt-0.5" style={{ color: colors.textSecondary }}>
            Manage guest profiles
          </p>
        </div>
        <button
          onClick={() => {
            setForm(emptyForm);
            setEditing(null);
            setShowForm(!showForm);
          }}
          className={btn.primary}
          style={showForm ? styles.btnCancel : styles.btnPrimary}
        >
          {showForm ? "✕ Cancel" : "+ Add Guest"}
        </button>
      </div>

      {/* Error */}
      {error && (
        <div className="flex items-center gap-2 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-5 text-sm">
          ⚠️ {error}
        </div>
      )}

      {/* Search & Filters */}
      <div
        className="flex flex-wrap gap-3 mb-6 p-4 bg-white border rounded-xl"
        style={card}
      >
        <input
          type="text"
          placeholder="🔍  Search by name or email..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSearch()}
          className={`${inp} flex-1 min-w-50`}
          style={inputStyle}
        />
        <input
          type="text"
          placeholder="Filter by nationality..."
          value={nationality}
          onChange={(e) => setNationality(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSearch()}
          className={`${inp} w-48`}
          style={inputStyle}
        />
        <button
          onClick={handleSearch}
          className={btn.secondary}
          style={styles.btnSecondary}
        >
          Search
        </button>
        <button
          onClick={() => {
            setSearch("");
            setNationality("");
            setSkip(0);
            setTimeout(fetchGuests, 0);
          }}
          className={btn.secondary}
          style={styles.btnGray}
        >
          Clear
        </button>
      </div>

      {/* Form */}
      {showForm && (
        <div
          className="bg-white border rounded-xl p-6 mb-6 shadow-sm"
          style={card}
        >
          <h2
            className="text-base font-semibold mb-5"
            style={{ color: colors.textPrimary }}
          >
            {editing ? "✏️  Edit Guest" : "➕  Add New Guest"}
          </h2>
          <form onSubmit={handleSubmit}>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {[
                { key: "name", label: "Full Name", type: "text" },
                { key: "email", label: "Email", type: "email" },
                { key: "phone", label: "Phone", type: "text" },
                { key: "nationality", label: "Nationality", type: "text" },
              ].map((f) => (
                <div key={f.key}>
                  <label className={lbl} style={lblStyle}>
                    {f.label}
                  </label>
                  <input
                    type={f.type}
                    value={form[f.key]}
                    onChange={(e) =>
                      setForm({ ...form, [f.key]: e.target.value })
                    }
                    className={inp}
                    style={inputStyle}
                    required
                  />
                </div>
              ))}
            </div>
            <div className="flex gap-3 mt-6">
              <button
                type="submit"
                className={btn.primary}
                style={styles.btnPrimary}
              >
                {editing ? "Update Guest" : "Create Guest"}
              </button>
              <button
                type="button"
                className={btn.secondary}
                style={styles.btnGray}
                onClick={() => {
                  setShowForm(false);
                  setEditing(null);
                }}
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Table */}
      {loading ? (
        <div
          className="text-center py-16 text-sm"
          style={{ color: colors.textMuted }}
        >
          Loading guests...
        </div>
      ) : guests.length === 0 ? (
        <div
          className="text-center py-16 text-sm"
          style={{ color: colors.textMuted }}
        >
          No guests found.
        </div>
      ) : (
        <div
          className="bg-white border rounded-xl overflow-hidden shadow-sm"
          style={table.wrapper}
        >
          <table className="w-full text-sm">
            <thead>
              <tr style={table.head}>
                {[
                  "ID",
                  "Guest",
                  "Email",
                  "Phone",
                  "Nationality",
                  "Actions",
                ].map((h) => (
                  <th
                    key={h}
                    className="px-4 py-3 text-left text-xs font-semibold tracking-wide uppercase"
                    style={table.th}
                  >
                    {h}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {guests.map((g, i) => (
                <tr
                  key={g.id}
                  className={table.rowHover}
                  style={table.divider(i, guests.length)}
                >
                  <td
                    className="px-4 py-3 text-xs"
                    style={{ color: colors.textMuted }}
                  >
                    {g.id}
                  </td>
                  <td className="px-4 py-3">
                    <div className="flex items-center gap-2.5">
                      <div
                        className="w-8 h-8 rounded-full flex items-center justify-center text-white text-xs font-bold shrink-0"
                        style={{ background: avatar.color(g.name) }}
                      >
                        {avatar.initials(g.name)}
                      </div>
                      <span
                        className="font-medium"
                        style={{ color: colors.textPrimary }}
                      >
                        {g.name}
                      </span>
                    </div>
                  </td>
                  <td
                    className="px-4 py-3"
                    style={{ color: colors.textSecondary }}
                  >
                    {g.email}
                  </td>
                  <td
                    className="px-4 py-3"
                    style={{ color: colors.textSecondary }}
                  >
                    {g.phone}
                  </td>
                  <td className="px-4 py-3">
                    <span
                      className="px-2 py-0.5 rounded-full text-xs font-medium"
                      style={badge.info}
                    >
                      {g.nationality}
                    </span>
                  </td>
                  <td className="px-4 py-3">
                    <div className="flex gap-1.5">
                      <button
                        onClick={() => handleEdit(g)}
                        className={btn.edit}
                        style={styles.btnEdit}
                      >
                        Edit
                      </button>
                      <button
                        onClick={() => handleDelete(g.id)}
                        className={btn.danger}
                        style={styles.btnDelete}
                      >
                        Delete
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Pagination */}
      {!loading && guests.length > 0 && (
        <div className="flex items-center justify-center gap-3 mt-5">
          <button
            onClick={() => setSkip(Math.max(0, skip - limit))}
            disabled={skip === 0}
            className={btn.secondary}
            style={styles.btnGray}
          >
            ← Previous
          </button>
          <span className="text-sm" style={{ color: colors.textSecondary }}>
            Showing {skip + 1}–{skip + guests.length}
          </span>
          <button
            onClick={() => setSkip(skip + limit)}
            disabled={guests.length < limit}
            className={btn.secondary}
            style={styles.btnGray}
          >
            Next →
          </button>
        </div>
      )}
    </div>
  );
}
