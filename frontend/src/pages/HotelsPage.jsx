import { useState, useEffect } from "react";
import { getHotels, createHotel, updateHotel, deleteHotel } from "../api/api";

const emptyForm = {
  name: "", description: "", address: "", city: "", country: "",
  phone: "", email: "", stars: 3, price_per_night: 0,
  amenities: "", rating: 0, image_url: "", is_active: true,
};

export default function HotelsPage() {
  const [hotels, setHotels] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [showForm, setShowForm] = useState(false);
  const [editing, setEditing] = useState(null);
  const [form, setForm] = useState(emptyForm);

  // Filters
  const [search, setSearch] = useState("");
  const [cityFilter, setCityFilter] = useState("");
  const [starsFilter, setStarsFilter] = useState("");
  const [skip, setSkip] = useState(0);
  const limit = 20;

  const fetchHotels = async () => {
    setLoading(true);
    setError("");
    try {
      const params = { skip, limit };
      if (search) params.search = search;
      if (cityFilter) params.city = cityFilter;
      if (starsFilter) params.stars = starsFilter;
      const res = await getHotels(params);
      setHotels(res.data);
    } catch (err) {
      setError("Failed to load hotels. Is the backend running?");
    }
    setLoading(false);
  };

  useEffect(() => { fetchHotels(); }, [skip, starsFilter]);

  const handleSearch = (e) => {
    e.preventDefault();
    setSkip(0);
    fetchHotels();
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      const data = {
        ...form,
        stars: Number(form.stars),
        price_per_night: Number(form.price_per_night),
        rating: Number(form.rating),
        image_url: form.image_url || null,
      };
      if (editing) {
        await updateHotel(editing, data);
      } else {
        await createHotel(data);
      }
      setShowForm(false);
      setEditing(null);
      setForm(emptyForm);
      fetchHotels();
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to save hotel");
    }
  };

  const handleEdit = (hotel) => {
    setForm({ ...hotel, image_url: hotel.image_url || "" });
    setEditing(hotel.id);
    setShowForm(true);
  };

  const handleDelete = async (id) => {
    if (!confirm("Delete this hotel?")) return;
    try {
      await deleteHotel(id);
      fetchHotels();
    } catch (err) {
      setError("Failed to delete hotel");
    }
  };

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Hotels</h1>
        <button
          onClick={() => { setForm(emptyForm); setEditing(null); setShowForm(!showForm); }}
          className="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 transition"
        >
          {showForm ? "Cancel" : "+ Add Hotel"}
        </button>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-4">
          {typeof error === "object" ? JSON.stringify(error) : error}
        </div>
      )}

      {/* Search & Filters */}
      <form onSubmit={handleSearch} className="flex flex-wrap gap-3 mb-6">
        <input
          type="text" placeholder="Search by name..." value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="border border-gray-300 rounded-lg px-3 py-2 text-sm flex-1 min-w-[200px]"
        />
        <input
          type="text" placeholder="Filter by city..." value={cityFilter}
          onChange={(e) => setCityFilter(e.target.value)}
          className="border border-gray-300 rounded-lg px-3 py-2 text-sm"
        />
        <select
          value={starsFilter} onChange={(e) => setStarsFilter(e.target.value)}
          className="border border-gray-300 rounded-lg px-3 py-2 text-sm"
        >
          <option value="">All Stars</option>
          {[1, 2, 3, 4, 5].map((s) => (
            <option key={s} value={s}>{s} Star{s > 1 && "s"}</option>
          ))}
        </select>
        <button type="submit" className="bg-gray-800 text-white px-4 py-2 rounded-lg text-sm hover:bg-gray-700">
          Search
        </button>
      </form>

      {/* Add/Edit Form */}
      {showForm && (
        <form onSubmit={handleSubmit} className="bg-white border border-gray-200 rounded-xl p-6 mb-6 shadow-sm">
          <h2 className="text-lg font-semibold mb-4">{editing ? "Edit Hotel" : "Add New Hotel"}</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {[
              { key: "name", label: "Hotel Name", type: "text" },
              { key: "address", label: "Address", type: "text" },
              { key: "city", label: "City", type: "text" },
              { key: "country", label: "Country", type: "text" },
              { key: "phone", label: "Phone", type: "text" },
              { key: "email", label: "Email", type: "email" },
              { key: "stars", label: "Stars (1-5)", type: "number", min: 1, max: 5 },
              { key: "price_per_night", label: "Price/Night ($)", type: "number", min: 0, step: "0.01" },
              { key: "rating", label: "Rating (0-5)", type: "number", min: 0, max: 5, step: "0.1" },
              { key: "image_url", label: "Image URL (optional)", type: "text" },
            ].map((f) => (
              <div key={f.key}>
                <label className="block text-xs font-medium text-gray-600 mb-1">{f.label}</label>
                <input
                  type={f.type} value={form[f.key]}
                  min={f.min} max={f.max} step={f.step}
                  onChange={(e) => setForm({ ...form, [f.key]: e.target.value })}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm"
                  required={f.key !== "image_url" && f.key !== "rating"}
                />
              </div>
            ))}
            <div>
              <label className="block text-xs font-medium text-gray-600 mb-1">Amenities</label>
              <input
                type="text" value={form.amenities}
                onChange={(e) => setForm({ ...form, amenities: e.target.value })}
                placeholder="WiFi, Pool, Gym..."
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm" required
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-600 mb-1">Description</label>
              <input
                type="text" value={form.description}
                onChange={(e) => setForm({ ...form, description: e.target.value })}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm" required
              />
            </div>
            <div className="flex items-center gap-2 pt-5">
              <input
                type="checkbox" checked={form.is_active}
                onChange={(e) => setForm({ ...form, is_active: e.target.checked })}
                className="h-4 w-4"
              />
              <label className="text-sm text-gray-600">Active (accepting bookings)</label>
            </div>
          </div>
          <button type="submit" className="mt-4 bg-indigo-600 text-white px-6 py-2 rounded-lg hover:bg-indigo-700">
            {editing ? "Update Hotel" : "Create Hotel"}
          </button>
        </form>
      )}

      {/* Hotels Table */}
      {loading ? (
        <p className="text-gray-500">Loading...</p>
      ) : hotels.length === 0 ? (
        <p className="text-gray-500">No hotels found.</p>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full bg-white border border-gray-200 rounded-xl shadow-sm text-sm">
            <thead className="bg-gray-50">
              <tr>
                {["ID", "Name", "City", "Country", "Stars", "Price/Night", "Rating", "Active", "Actions"].map((h) => (
                  <th key={h} className="px-4 py-3 text-left font-medium text-gray-600">{h}</th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {hotels.map((h) => (
                <tr key={h.id} className="hover:bg-gray-50">
                  <td className="px-4 py-3">{h.id}</td>
                  <td className="px-4 py-3 font-medium text-gray-900">{h.name}</td>
                  <td className="px-4 py-3">{h.city}</td>
                  <td className="px-4 py-3">{h.country}</td>
                  <td className="px-4 py-3">{"★".repeat(h.stars)}</td>
                  <td className="px-4 py-3">${h.price_per_night}</td>
                  <td className="px-4 py-3">{h.rating}/5</td>
                  <td className="px-4 py-3">
                    <span className={`px-2 py-1 rounded-full text-xs ${h.is_active ? "bg-green-100 text-green-700" : "bg-red-100 text-red-700"}`}>
                      {h.is_active ? "Active" : "Inactive"}
                    </span>
                  </td>
                  <td className="px-4 py-3 flex gap-2">
                    <button onClick={() => handleEdit(h)} className="text-indigo-600 hover:underline text-xs">Edit</button>
                    <button onClick={() => handleDelete(h.id)} className="text-red-600 hover:underline text-xs">Delete</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Pagination */}
      <div className="flex gap-3 mt-4 justify-center">
        <button
          onClick={() => setSkip(Math.max(0, skip - limit))}
          disabled={skip === 0}
          className="px-4 py-2 rounded-lg bg-gray-200 text-sm disabled:opacity-40 hover:bg-gray-300"
        >
          Previous
        </button>
        <span className="px-4 py-2 text-sm text-gray-600">
          Showing {skip + 1} - {skip + hotels.length}
        </span>
        <button
          onClick={() => setSkip(skip + limit)}
          disabled={hotels.length < limit}
          className="px-4 py-2 rounded-lg bg-gray-200 text-sm disabled:opacity-40 hover:bg-gray-300"
        >
          Next
        </button>
      </div>
    </div>
  );
}
