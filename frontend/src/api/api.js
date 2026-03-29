import axios from "axios";

// All requests go through the API Gateway on port 8000
const API = axios.create({ baseURL: "http://localhost:8000" });

// ── Hotels ──────────────────────────────────
export const getHotels = (params) => API.get("/hotels", { params });
export const getHotel = (id) => API.get(`/hotels/${id}`);
export const createHotel = (data) => API.post("/hotels", data);
export const updateHotel = (id, data) => API.put(`/hotels/${id}`, data);
export const patchHotel = (id, data) => API.patch(`/hotels/${id}`, data);
export const deleteHotel = (id) => API.delete(`/hotels/${id}`);

// ── Rooms ───────────────────────────────────
export const getRooms = () => API.get("/rooms");
export const getRoom = (id) => API.get(`/rooms/${id}`);
export const createRoom = (data) => API.post("/rooms", data);
export const updateRoom = (id, data) => API.put(`/rooms/${id}`, data);
export const deleteRoom = (id) => API.delete(`/rooms/${id}`);

// ── Guests ──────────────────────────────────
export const getGuests = () => API.get("/guests");
export const getGuest = (id) => API.get(`/guests/${id}`);
export const createGuest = (data) => API.post("/guests", data);
export const updateGuest = (id, data) => API.put(`/guests/${id}`, data);
export const deleteGuest = (id) => API.delete(`/guests/${id}`);

// ── Bookings ────────────────────────────────
export const getBookings = () => API.get("/bookings");
export const getBooking = (id) => API.get(`/bookings/${id}`);
export const createBooking = (data) => API.post("/bookings", data);
export const updateBooking = (id, data) => API.put(`/bookings/${id}`, data);
export const deleteBooking = (id) => API.delete(`/bookings/${id}`);

// ── Payments ────────────────────────────────
export const getPayments = () => API.get("/payments");
export const getPayment = (id) => API.get(`/payments/${id}`);
export const createPayment = (data) => API.post("/payments", data);
export const updatePayment = (id, data) => API.put(`/payments/${id}`, data);
export const deletePayment = (id) => API.delete(`/payments/${id}`);
