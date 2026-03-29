import { NavLink } from "react-router-dom";
import { colors } from "../theme";

const links = [
  { to: "/",         label: "Hotels",   icon: "🏨" },
  { to: "/rooms",    label: "Rooms",    icon: "🛏️" },
  { to: "/guests",   label: "Guests",   icon: "👤" },
  { to: "/bookings", label: "Bookings", icon: "📋" },
  { to: "/payments", label: "Payments", icon: "💳" },
];

export default function Navbar() {
  return (
    <nav style={{ background: colors.navBg, borderBottom: `1px solid ${colors.navBorder}` }}
      className="px-8 py-0 flex items-center gap-10 shadow-lg sticky top-0 z-50">

      {/* Brand */}
      <div className="flex items-center gap-2 py-4 mr-4">
        <div className="w-8 h-8 rounded-lg flex items-center justify-center"
          style={{ background: `linear-gradient(135deg, ${colors.primary}, #3b82f6)` }}>
          <span className="text-white text-sm font-bold">H</span>
        </div>
        <span className="font-semibold text-white text-sm tracking-tight">
          Hotel Booking{" "}
          <span style={{ color: colors.navActive }}>System</span>
        </span>
      </div>

      {/* Nav Links */}
      <div className="flex items-stretch gap-1 flex-1">
        {links.map((l) => (
          <NavLink
            key={l.to}
            to={l.to}
            end={l.to === "/"}
            style={({ isActive }) => ({
              borderBottomColor: isActive ? colors.navActive : "transparent",
              color: isActive ? colors.navActive : colors.navInactive,
            })}
            className="flex items-center gap-1.5 px-4 py-4 text-sm font-medium transition-all border-b-2 hover:text-white hover:border-slate-600"
          >
            <span className="text-base leading-none">{l.icon}</span>
            {l.label}
          </NavLink>
        ))}
      </div>

      {/* Badge */}
      <div className="py-4">
        <span className="text-xs px-2.5 py-1 rounded-full font-medium"
          style={{ background: colors.navBadgeBg, color: colors.navBadgeText }}>
          IT4020 — SLIIT
        </span>
      </div>
    </nav>
  );
}