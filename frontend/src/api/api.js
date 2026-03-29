import axios from "axios";

// All requests go through the API Gateway on port 8000
const API = axios.create({ baseURL: "http://localhost:8000" });

// ── Hotels ──────────────────────────────────
export const getHotels  = (params) => API.get("/hotels", { params });
export const getHotel   = (id)     => API.get(`/hotels/${id}`);
export const createHotel = (data)  => API.post("/hotels", data);
export const updateHotel = (id, data) => API.put(`/hotels/${id}`, data);
export const patchHotel  = (id, data) => API.patch(`/hotels/${id}`, data);
export const deleteHotel = (id)    => API.delete(`/hotels/${id}`);

// ── Rooms ───────────────────────────────────
// Supported params: hotel_id, room_type, is_available, min_price, max_price, skip, limit
export const getRooms   = (params) => API.get("/rooms", { params });
export const getRoom    = (id)     => API.get(`/rooms/${id}`);
export const createRoom  = (data)  => API.post("/rooms", data);
export const updateRoom  = (id, data) => API.put(`/rooms/${id}`, data);
export const deleteRoom  = (id)    => API.delete(`/rooms/${id}`);

// ── Guests ──────────────────────────────────
// Supported params: search, nationality, skip, limit
export const getGuests  = (params) => API.get("/guests", { params });
export const getGuest   = (id)     => API.get(`/guests/${id}`);
export const createGuest = (data)  => API.post("/guests", data);
export const updateGuest = (id, data) => API.put(`/guests/${id}`, data);
export const deleteGuest = (id)    => API.delete(`/guests/${id}`);

// ── Bookings ────────────────────────────────
// Supported params: guest_id, room_id, status, check_in_from, check_in_to, skip, limit
export const getBookings  = (params) => API.get("/bookings", { params });
export const getBooking   = (id)     => API.get(`/bookings/${id}`);
export const createBooking = (data)  => API.post("/bookings", data);
export const updateBooking = (id, data) => API.put(`/bookings/${id}`, data);
export const deleteBooking = (id)    => API.delete(`/bookings/${id}`);

// ── Payments ────────────────────────────────
// Supported params: booking_id, status, method, min_amount, max_amount, skip, limit
export const getPayments  = (params) => API.get("/payments", { params });
export const getPayment   = (id)     => API.get(`/payments/${id}`);
export const createPayment = (data)  => API.post("/payments", data);
export const updatePayment = (id, data) => API.put(`/payments/${id}`, data);
export const deletePayment = (id)    => API.delete(`/payments/${id}`);