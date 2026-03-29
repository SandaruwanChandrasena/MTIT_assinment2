"""
Seed script — populates all 5 microservices with 10 records each.
Creates data IN ORDER so inter-service validation passes:
  1. Hotels first (rooms need valid hotel_id)
  2. Rooms second (bookings need valid room_id)
  3. Guests third (bookings need valid guest_id)
  4. Bookings fourth (payments need valid booking_id)
  5. Payments last

Usage:
  source venv/bin/activate
  python3 seed_data.py
"""

import requests
import random

BASE = "http://localhost:8000"

# ── 10 Hotels ──────────────────────────────
hotels = [
    {
        "name": "Grand Hyatt Colombo",
        "description": "Luxury hotel with stunning ocean views and premium amenities",
        "address": "1 Galle Face Road",
        "city": "Colombo",
        "country": "Sri Lanka",
        "phone": "+94 11 234 1234",
        "email": "info@grandhyattcolombo.com",
        "stars": 5,
        "price_per_night": 250.00,
        "amenities": "WiFi, Pool, Gym, Spa, Restaurant, Bar",
        "rating": 4.8,
        "image_url": "https://example.com/hotel-1.jpg",
        "is_active": True,
    },
    {
        "name": "Cinnamon Grand Colombo",
        "description": "Elegant city hotel blending tradition with modern comfort",
        "address": "77 Galle Road",
        "city": "Colombo",
        "country": "Sri Lanka",
        "phone": "+94 11 243 7437",
        "email": "info@cinnamongrand.com",
        "stars": 5,
        "price_per_night": 200.00,
        "amenities": "WiFi, Pool, Gym, Restaurant, Business Center",
        "rating": 4.6,
        "image_url": "https://example.com/hotel-2.jpg",
        "is_active": True,
    },
    {
        "name": "Jetwing Blue Negombo",
        "description": "Beachfront paradise with crystal clear waters",
        "address": "Ethukala, Negombo",
        "city": "Negombo",
        "country": "Sri Lanka",
        "phone": "+94 31 227 6000",
        "email": "info@jetwingblue.com",
        "stars": 4,
        "price_per_night": 150.00,
        "amenities": "WiFi, Pool, Beach Access, Restaurant, Bar",
        "rating": 4.5,
        "image_url": "https://example.com/hotel-3.jpg",
        "is_active": True,
    },
    {
        "name": "Shangri-La Colombo",
        "description": "Modern luxury hotel in the heart of the city",
        "address": "1 Beira Lake Road",
        "city": "Colombo",
        "country": "Sri Lanka",
        "phone": "+94 11 788 5000",
        "email": "info@shangrilacolombo.com",
        "stars": 5,
        "price_per_night": 300.00,
        "amenities": "WiFi, Pool, Gym, Spa, Restaurant, Rooftop Bar",
        "rating": 4.9,
        "image_url": "https://example.com/hotel-4.jpg",
        "is_active": True,
    },
    {
        "name": "Kandy City Hotel",
        "description": "Comfortable stay in the cultural capital of Sri Lanka",
        "address": "5 Dalada Veediya",
        "city": "Kandy",
        "country": "Sri Lanka",
        "phone": "+94 81 223 4000",
        "email": "info@kandycityhotel.com",
        "stars": 3,
        "price_per_night": 80.00,
        "amenities": "WiFi, Restaurant, Laundry",
        "rating": 4.1,
        "image_url": "https://example.com/hotel-5.jpg",
        "is_active": True,
    },
    {
        "name": "Galle Fort Hotel",
        "description": "Heritage hotel inside the UNESCO-listed Galle Fort",
        "address": "28 Church Street, Galle Fort",
        "city": "Galle",
        "country": "Sri Lanka",
        "phone": "+94 91 223 0870",
        "email": "info@galleforthotel.com",
        "stars": 4,
        "price_per_night": 180.00,
        "amenities": "WiFi, Pool, Restaurant, Airport Shuttle",
        "rating": 4.7,
        "image_url": "https://example.com/hotel-6.jpg",
        "is_active": True,
    },
    {
        "name": "Ella Eco Lodge",
        "description": "Mountain retreat with breathtaking valley views",
        "address": "12 Passara Road",
        "city": "Ella",
        "country": "Sri Lanka",
        "phone": "+94 57 222 8800",
        "email": "info@ellaecolodge.com",
        "stars": 3,
        "price_per_night": 70.00,
        "amenities": "WiFi, Restaurant, Hiking Trails",
        "rating": 4.3,
        "image_url": "https://example.com/hotel-7.jpg",
        "is_active": True,
    },
    {
        "name": "Hilton Colombo",
        "description": "International standard hotel with world-class facilities",
        "address": "2 Sir Chittampalam A Gardiner Mawatha",
        "city": "Colombo",
        "country": "Sri Lanka",
        "phone": "+94 11 249 2492",
        "email": "info@hiltoncolombo.com",
        "stars": 5,
        "price_per_night": 220.00,
        "amenities": "WiFi, Pool, Gym, Spa, Restaurant, Bar, Valet Parking",
        "rating": 4.7,
        "image_url": "https://example.com/hotel-8.jpg",
        "is_active": True,
    },
    {
        "name": "Sigiriya Village Hotel",
        "description": "Eco-friendly resort surrounded by tropical gardens",
        "address": "Inamaluwa, Sigiriya",
        "city": "Sigiriya",
        "country": "Sri Lanka",
        "phone": "+94 66 228 6803",
        "email": "info@sigiriyavillage.com",
        "stars": 4,
        "price_per_night": 130.00,
        "amenities": "WiFi, Pool, Restaurant, Kids Club",
        "rating": 4.4,
        "image_url": "https://example.com/hotel-9.jpg",
        "is_active": True,
    },
    {
        "name": "Bentota Beach Hotel",
        "description": "Family-friendly resort on the golden Bentota beach",
        "address": "National Holiday Resort, Bentota",
        "city": "Bentota",
        "country": "Sri Lanka",
        "phone": "+94 34 227 5176",
        "email": "info@bentotabeach.com",
        "stars": 4,
        "price_per_night": 160.00,
        "amenities": "WiFi, Pool, Beach Access, Restaurant, Water Sports",
        "rating": 4.5,
        "image_url": "https://example.com/hotel-10.jpg",
        "is_active": True,
    },
]

# ── 10 Rooms (hotel_id 1-10, one per hotel) ──
rooms = [
    {"hotel_id": 1, "room_type": "Suite",    "price_per_night": 350.00, "is_available": True},
    {"hotel_id": 2, "room_type": "Deluxe",   "price_per_night": 250.00, "is_available": True},
    {"hotel_id": 3, "room_type": "Double",   "price_per_night": 180.00, "is_available": True},
    {"hotel_id": 4, "room_type": "Penthouse","price_per_night": 500.00, "is_available": True},
    {"hotel_id": 5, "room_type": "Single",   "price_per_night": 90.00,  "is_available": True},
    {"hotel_id": 6, "room_type": "Deluxe",   "price_per_night": 220.00, "is_available": True},
    {"hotel_id": 7, "room_type": "Double",   "price_per_night": 95.00,  "is_available": True},
    {"hotel_id": 8, "room_type": "Suite",    "price_per_night": 300.00, "is_available": True},
    {"hotel_id": 9, "room_type": "Family",   "price_per_night": 175.00, "is_available": True},
    {"hotel_id":10, "room_type": "Double",   "price_per_night": 200.00, "is_available": True},
]

# ── 10 Guests ──────────────────────────────
guests = [
    {"name": "John Smith",      "email": "john.smith@email.com",      "phone": "+1 212 555 1001", "nationality": "American"},
    {"name": "Priya Sharma",    "email": "priya.sharma@email.com",    "phone": "+91 98 765 4321", "nationality": "Indian"},
    {"name": "Hans Mueller",    "email": "hans.mueller@email.com",    "phone": "+49 30 123 4567", "nationality": "German"},
    {"name": "Yuki Tanaka",     "email": "yuki.tanaka@email.com",     "phone": "+81 3 1234 5678", "nationality": "Japanese"},
    {"name": "Aisha Khan",      "email": "aisha.khan@email.com",      "phone": "+92 21 111 2222", "nationality": "Pakistani"},
    {"name": "Carlos Garcia",   "email": "carlos.garcia@email.com",   "phone": "+34 91 234 5678", "nationality": "Spanish"},
    {"name": "Emma Brown",      "email": "emma.brown@email.com",      "phone": "+44 20 7946 0958","nationality": "British"},
    {"name": "Wei Li",          "email": "wei.li@email.com",          "phone": "+86 10 8765 4321","nationality": "Chinese"},
    {"name": "Sarah Johnson",   "email": "sarah.johnson@email.com",   "phone": "+1 310 555 9876", "nationality": "American"},
    {"name": "Nimal Perera",    "email": "nimal.perera@email.com",    "phone": "+94 77 123 4567", "nationality": "Sri Lankan"},
]

# ── 10 Bookings (guest_id 1-10, room_id 1-10, each room used once) ──
bookings = [
    {"guest_id": 1,  "room_id": 1,  "check_in": "2026-04-10", "check_out": "2026-04-13", "status": "confirmed"},
    {"guest_id": 2,  "room_id": 2,  "check_in": "2026-04-15", "check_out": "2026-04-18", "status": "confirmed"},
    {"guest_id": 3,  "room_id": 3,  "check_in": "2026-05-01", "check_out": "2026-05-05", "status": "confirmed"},
    {"guest_id": 4,  "room_id": 4,  "check_in": "2026-05-10", "check_out": "2026-05-12", "status": "pending"},
    {"guest_id": 5,  "room_id": 5,  "check_in": "2026-05-20", "check_out": "2026-05-22", "status": "confirmed"},
    {"guest_id": 6,  "room_id": 6,  "check_in": "2026-06-01", "check_out": "2026-06-04", "status": "confirmed"},
    {"guest_id": 7,  "room_id": 7,  "check_in": "2026-06-10", "check_out": "2026-06-14", "status": "pending"},
    {"guest_id": 8,  "room_id": 8,  "check_in": "2026-07-05", "check_out": "2026-07-08", "status": "confirmed"},
    {"guest_id": 9,  "room_id": 9,  "check_in": "2026-07-15", "check_out": "2026-07-17", "status": "cancelled"},
    {"guest_id": 10, "room_id": 10, "check_in": "2026-08-01", "check_out": "2026-08-05", "status": "confirmed"},
]

# ── 10 Payments (booking_id 1-10) ──────────
payments = [
    {"booking_id": 1,  "amount": 1050.00, "method": "card",   "status": "paid"},
    {"booking_id": 2,  "amount": 750.00,  "method": "online", "status": "paid"},
    {"booking_id": 3,  "amount": 720.00,  "method": "card",   "status": "paid"},
    {"booking_id": 4,  "amount": 1000.00, "method": "cash",   "status": "pending"},
    {"booking_id": 5,  "amount": 180.00,  "method": "card",   "status": "paid"},
    {"booking_id": 6,  "amount": 660.00,  "method": "online", "status": "paid"},
    {"booking_id": 7,  "amount": 380.00,  "method": "card",   "status": "pending"},
    {"booking_id": 8,  "amount": 900.00,  "method": "online", "status": "paid"},
    {"booking_id": 9,  "amount": 350.00,  "method": "cash",   "status": "failed"},
    {"booking_id": 10, "amount": 800.00,  "method": "card",   "status": "paid"},
]

# ── Seed function ───────────────────────────
def seed(endpoint, items, label):
    print(f"\nSeeding {label} ({len(items)} records)...")
    success = 0
    failed = 0
    for item in items:
        try:
            res = requests.post(f"{BASE}/{endpoint}", json=item)
            if res.status_code in (200, 201):
                success += 1
            else:
                failed += 1
                if failed <= 3:
                    print(f"  x Failed: {res.status_code} - {res.json().get('detail', res.text)[:100]}")
        except requests.ConnectionError:
            print(f"  x Cannot connect! Is the backend running? (python3 run_all.py)")
            return
    print(f"  + {success} created, {failed} failed")

# ── Run in correct order ────────────────────
print("=" * 55)
print("  Seeding Hotel Booking System — 10 records each")
print("  Order: Hotels → Rooms → Guests → Bookings → Payments")
print("=" * 55)

seed("hotels",   hotels,   "Hotels")
seed("rooms",    rooms,    "Rooms")
seed("guests",   guests,   "Guests")
seed("bookings", bookings, "Bookings")
seed("payments", payments, "Payments")

print("\n" + "=" * 55)
print("  Done! 50 total records. Refresh your browser.")
print("=" * 55)