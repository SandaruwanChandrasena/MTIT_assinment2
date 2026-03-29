import { NavLink } from "react-router-dom";

const links = [
  { to: "/", label: "Hotels" },
  { to: "/rooms", label: "Rooms" },
  { to: "/guests", label: "Guests" },
  { to: "/bookings", label: "Bookings" },
  { to: "/payments", label: "Payments" },
];

export default function Navbar() {
  return (
    <nav className="bg-gray-900 text-white px-6 py-4 flex items-center gap-8 shadow-lg">
      <span className="text-xl font-bold tracking-tight">Hotel Booking System</span>
      <div className="flex gap-1">
        {links.map((l) => (
          <NavLink
            key={l.to}
            to={l.to}
            className={({ isActive }) =>
              `px-4 py-2 rounded-lg text-sm font-medium transition ${
                isActive ? "bg-indigo-600 text-white" : "text-gray-300 hover:bg-gray-800"
              }`
            }
          >
            {l.label}
          </NavLink>
        ))}
      </div>
    </nav>
  );
}
