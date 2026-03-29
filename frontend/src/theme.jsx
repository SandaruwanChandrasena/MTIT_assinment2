// ─────────────────────────────────────────────────────────────
// THEME.JS — Centralized Design System
// Hotel Booking System | IT4020 — SLIIT
//
// HOW TO CHANGE THE THEME:
//   Just edit the color values in the "Color Palette" section below.
//   All components import from this file, so every page updates
//   automatically when you change a value here.
//
// USAGE IN COMPONENTS:
//   import { colors, btn, inp, lbl, badge } from "../theme";
// ─────────────────────────────────────────────────────────────


// ─────────────────────────────────────────────────────────────
// COLOR PALETTE
// Change these values to switch the entire app theme
// ─────────────────────────────────────────────────────────────
export const colors = {
  // Primary blue shades
  primary:        "#2563eb",   // main buttons, active states
  primaryHover:   "#1d4ed8",   // hover on primary
  primaryLight:   "#eff6ff",   // light bg for table headers, filter bars
  primaryBorder:  "#bfdbfe",   // borders on cards and tables
  primaryText:    "#1d4ed8",   // text on light blue backgrounds
  primaryDeep:    "#1e3a5f",   // badge backgrounds, dark accents

  // Navbar
  navBg:          "#0f172a",   // navbar background (dark navy)
  navBorder:      "#1e293b",   // navbar bottom border
  navActive:      "#60a5fa",   // active link text + underline
  navInactive:    "#94a3b8",   // inactive link text
  navBadgeBg:     "#1e3a5f",   // SLIIT badge background
  navBadgeText:   "#93c5fd",   // SLIIT badge text

  // Status colors
  successBg:      "#dcfce7",
  successText:    "#166534",
  warningBg:      "#fef9c3",
  warningText:    "#854d0e",
  dangerBg:       "#fee2e2",
  dangerText:     "#991b1b",

  // Edit / Delete button pills
  editBg:         "#eff6ff",
  editText:       "#2563eb",
  deleteBg:       "#fff1f2",
  deleteText:     "#be123c",

  // General UI
  pageBg:         "#f8fafc",
  cardBg:         "#ffffff",
  rowHover:       "#f8fafc",
  rowDivider:     "#f1f5f9",
  inputBorder:    "#e2e8f0",
  inputFocusRing: "#bfdbfe",

  // Text
  textPrimary:    "#111827",
  textSecondary:  "#6b7280",
  textMuted:      "#9ca3af",
};


// ─────────────────────────────────────────────────────────────
// BUTTON CLASS NAMES
// ─────────────────────────────────────────────────────────────
export const btn = {
  primary:   "inline-flex items-center gap-1.5 px-4 py-2 rounded-lg text-sm font-medium text-white transition-all hover:opacity-90 active:scale-95",
  secondary: "inline-flex items-center gap-1.5 px-4 py-2 rounded-lg text-sm font-medium transition-all hover:opacity-90 active:scale-95",
  edit:      "text-xs font-medium px-2.5 py-1 rounded-md transition-all hover:opacity-80",
  danger:    "text-xs font-medium px-2.5 py-1 rounded-md transition-all hover:opacity-80",
};

// Inline styles for buttons
export const styles = {
  btnPrimary:   { background: colors.primary },
  btnCancel:    { background: "#6b7280" },
  btnSecondary: { background: colors.primaryLight, color: colors.primaryText, border: `1px solid ${colors.primaryBorder}` },
  btnGray:      { background: "#f3f4f6", color: "#374151" },
  btnEdit:      { background: colors.editBg,   color: colors.editText   },
  btnDelete:    { background: colors.deleteBg, color: colors.deleteText },
};


// ─────────────────────────────────────────────────────────────
// FORM STYLES
// ─────────────────────────────────────────────────────────────
export const inp = "w-full border rounded-lg px-3 py-2 text-sm outline-none transition-all focus:ring-2 focus:ring-blue-100 focus:border-blue-400";
export const lbl = "block text-xs font-semibold mb-1.5 tracking-wide uppercase";
export const inputStyle = { borderColor: colors.inputBorder };
export const lblStyle   = { color: colors.primaryHover };


// ─────────────────────────────────────────────────────────────
// TABLE STYLES
// ─────────────────────────────────────────────────────────────
export const table = {
  wrapper:  { borderColor: colors.primaryBorder },
  head:     { background: colors.primaryLight, borderBottom: `1px solid ${colors.primaryBorder}` },
  th:       { color: colors.primaryText },
  rowHover: "hover:bg-slate-50 transition-colors",
  divider:  (i, len) => ({ borderBottom: i < len - 1 ? `1px solid ${colors.rowDivider}` : "none" }),
};


// ─────────────────────────────────────────────────────────────
// CARD / PANEL STYLES
// ─────────────────────────────────────────────────────────────
export const card = {
  border:     `1px solid ${colors.primaryBorder}`,
  background: colors.cardBg,
};


// ─────────────────────────────────────────────────────────────
// BADGE / STATUS STYLES
// ─────────────────────────────────────────────────────────────
export const badge = {
  confirmed: { background: colors.successBg,   color: colors.successText },
  pending:   { background: colors.warningBg,   color: colors.warningText },
  cancelled: { background: colors.dangerBg,    color: colors.dangerText  },
  paid:      { background: colors.successBg,   color: colors.successText },
  failed:    { background: colors.dangerBg,    color: colors.dangerText  },
  active:    { background: colors.successBg,   color: colors.successText },
  inactive:  { background: colors.dangerBg,    color: colors.dangerText  },
  available: { background: colors.successBg,   color: colors.successText },
  booked:    { background: colors.dangerBg,    color: colors.dangerText  },
  info:      { background: colors.primaryLight, color: colors.primaryText },
  card:      { background: "#eff6ff", color: "#1d4ed8" },
  cash:      { background: "#f9fafb", color: "#374151" },
  online:    { background: "#f5f3ff", color: "#5b21b6" },

  roomType: (t) => {
    const map = {
      Suite:        { background: "#fdf4ff", color: "#7e22ce" },
      Penthouse:    { background: "#fdf4ff", color: "#6d28d9" },
      Presidential: { background: "#fdf4ff", color: "#581c87" },
      Deluxe:       { background: "#eff6ff", color: "#1d4ed8" },
      Executive:    { background: "#ecfdf5", color: "#047857" },
      Double:       { background: "#f0f9ff", color: "#075985" },
      Twin:         { background: "#f0f9ff", color: "#0369a1" },
      Family:       { background: "#fff7ed", color: "#9a3412" },
      Studio:       { background: "#fefce8", color: "#854d0e" },
      Single:       { background: "#f9fafb", color: "#374151" },
    };
    return map[t] || { background: "#f3f4f6", color: "#374151" };
  },
};


// ─────────────────────────────────────────────────────────────
// AVATAR HELPER (Guests page)
// ─────────────────────────────────────────────────────────────
export const avatar = {
  color: (name) => {
    const palette = [
      colors.primary, "#0891b2", "#7c3aed", "#db2777",
      "#d97706", "#dc2626", "#059669", "#0d9488",
    ];
    let hash = 0;
    for (let c of name) hash = c.charCodeAt(0) + ((hash << 5) - hash);
    return palette[Math.abs(hash) % palette.length];
  },
  initials: (name) => name.split(" ").map(w => w[0]).join("").toUpperCase().slice(0, 2),
};