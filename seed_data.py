"""
Seed script — populates all 5 microservices with 50 records each.
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

# ── Hotel data pools ────────────────────────
hotel_brands = [
    "Grand Hyatt", "Hilton", "Shangri-La", "Marriott", "Cinnamon Grand",
    "Jetwing", "Taj", "Radisson", "Sheraton", "InterContinental",
    "Four Seasons", "Ritz-Carlton", "Mandarin Oriental", "Fairmont", "Westin",
    "Novotel", "Crowne Plaza", "Holiday Inn", "Best Western", "Ramada",
    "Park Hyatt", "W Hotel", "St. Regis", "Sofitel", "Movenpick",
]
cities = [
    ("Colombo", "Sri Lanka"), ("Kandy", "Sri Lanka"), ("Galle", "Sri Lanka"),
    ("Hambantota", "Sri Lanka"), ("Negombo", "Sri Lanka"), ("Trincomalee", "Sri Lanka"),
    ("Ella", "Sri Lanka"), ("Nuwara Eliya", "Sri Lanka"), ("Jaffna", "Sri Lanka"),
    ("Sigiriya", "Sri Lanka"), ("Bentota", "Sri Lanka"), ("Anuradhapura", "Sri Lanka"),
    ("Mumbai", "India"), ("Bangkok", "Thailand"), ("Singapore", "Singapore"),
    ("Dubai", "UAE"), ("London", "UK"), ("Paris", "France"),
    ("Tokyo", "Japan"), ("Sydney", "Australia"),
]
streets = ["Main St", "Beach Rd", "Temple Ave", "Lake Dr", "Hill Rd", "Park Lane", "Ocean Blvd", "Garden Way",
           "Station Rd", "Market St", "River Walk", "Palm Ave", "Sunset Blvd", "Kings Rd", "Queens Ave"]
amenity_pool = ["WiFi", "Pool", "Gym", "Spa", "Restaurant", "Bar", "Room Service",
                "Beach Access", "Golf Course", "Tennis Court", "Kids Club", "Valet Parking",
                "Business Center", "Laundry", "Airport Shuttle", "Rooftop Bar", "Fine Dining"]
descriptions = [
    "Luxury hotel with stunning views and premium amenities",
    "Modern boutique hotel in the heart of the city",
    "Family-friendly resort with world-class facilities",
    "Budget-friendly stay with all essential amenities",
    "Elegant colonial-style property with rich history",
    "Beachfront paradise with crystal clear waters",
    "Mountain retreat with breathtaking valley views",
    "Urban oasis with rooftop dining and city panorama",
    "Heritage hotel blending tradition with modern comfort",
    "Eco-friendly resort surrounded by tropical gardens",
]
room_types = ["Single", "Double", "Twin", "Suite", "Deluxe", "Penthouse", "Family", "Studio", "Executive", "Presidential"]
first_names = ["John", "Aisha", "Hans", "Yuki", "Priya", "Mohammed", "Sarah", "Carlos", "Emma", "Wei",
               "Fatima", "James", "Sofia", "Raj", "Olivia", "Ahmed", "Maria", "Kenji", "Zara", "David",
               "Nadia", "Thomas", "Amara", "Liam", "Mei", "Omar", "Isabella", "Ravi", "Chloe", "Sanjay",
               "Elena", "Marcus", "Aiko", "Tariq", "Anna", "Vikram", "Lucia", "Chen", "Hannah", "Ali",
               "Nina", "Pavel", "Layla", "Daniel", "Sakura", "Ibrahim", "Clara", "Arjun", "Mia", "Dmitri"]
last_names = ["Smith", "Fernando", "Mueller", "Tanaka", "Sharma", "Khan", "Johnson", "Garcia", "Brown", "Li",
              "Wilson", "Kumar", "Perera", "Nakamura", "Patel", "Anderson", "Silva", "Kim", "Martinez", "Taylor",
              "Gupta", "Williams", "Lopez", "Suzuki", "Ali", "Thomas", "Hernandez", "Sato", "Das", "Moore",
              "Singh", "White", "Chen", "Santos", "Jones", "Rao", "Clark", "Park", "Shah", "Lewis",
              "Mendez", "Wang", "Adams", "Yamamoto", "Hussein", "Baker", "Costa", "Reddy", "Young", "Ivanov"]
nationalities = ["Sri Lankan", "American", "British", "German", "Japanese", "Indian", "Australian",
                 "French", "Thai", "Chinese", "Canadian", "Italian", "Brazilian", "South Korean",
                 "Emirati", "Russian", "Spanish", "Swedish", "Malaysian", "New Zealander"]

# ── Generate 50 Hotels ──────────────────────
hotels = []
used_names = set()
for i in range(50):
    city, country = cities[i % len(cities)]
    brand = hotel_brands[i % len(hotel_brands)]
    name = f"{brand} {city}"
    while name in used_names:
        name = f"{brand} {city} {random.randint(2, 99)}"
    used_names.add(name)
    hotels.append({
        "name": name,
        "description": descriptions[i % len(descriptions)],
        "address": f"{random.randint(1, 999)} {random.choice(streets)}",
        "city": city,
        "country": country,
        "phone": f"+{random.randint(1, 99)} {random.randint(10, 99)} {random.randint(100, 999)} {random.randint(1000, 9999)}",
        "email": f"info@{brand.lower().replace(' ', '')}{i+1}.com",
        "stars": random.randint(1, 5),
        "price_per_night": round(random.uniform(30, 500), 2),
        "amenities": ", ".join(random.sample(amenity_pool, random.randint(3, 8))),
        "rating": round(random.uniform(1.0, 5.0), 1),
        "image_url": f"https://example.com/hotel-{i+1}.jpg" if random.random() > 0.3 else None,
        "is_active": True if i < 45 else False,
    })

# ── Generate 50 Rooms (hotel_id 1-50, all valid) ─────
rooms = []
for i in range(50):
    rooms.append({
        "hotel_id": (i % 50) + 1,  # cycles through hotels 1-50
        "room_type": room_types[i % len(room_types)],
        "price_per_night": round(random.uniform(40, 800), 2),
        "is_available": True,  # all start available so bookings work
    })

# ── Generate 50 Guests ─────────────────────
guests = []
for i in range(50):
    guests.append({
        "name": f"{first_names[i]} {last_names[i]}",
        "email": f"{first_names[i].lower()}.{last_names[i].lower()}@email.com",
        "phone": f"+{random.randint(1, 99)} {random.randint(10, 99)} {random.randint(100, 999)} {random.randint(1000, 9999)}",
        "nationality": nationalities[i % len(nationalities)],
    })

# ── Generate 50 Bookings (valid guest_id 1-50, room_id 1-50) ─────
# Each room is booked at most once so availability checks pass
bookings = []
available_rooms = list(range(1, 51))  # rooms 1-50
random.shuffle(available_rooms)
for i in range(50):
    month = random.randint(4, 12)
    day_in = random.randint(1, 20)
    day_out = day_in + random.randint(1, 7)
    if day_out > 28:
        day_out = 28
    status = random.choice(["confirmed", "confirmed", "confirmed", "pending", "pending", "cancelled"])
    bookings.append({
        "guest_id": (i % 50) + 1,
        "room_id": available_rooms[i],  # each room used once
        "check_in": f"2026-{month:02d}-{day_in:02d}",
        "check_out": f"2026-{month:02d}-{day_out:02d}",
        "status": status,
    })

# ── Generate 50 Payments (valid booking_id 1-50) ─────
payments = []
methods = ["card", "cash", "online"]
pay_statuses = ["paid", "paid", "paid", "pending", "failed"]
for i in range(50):
    payments.append({
        "booking_id": (i % 50) + 1,
        "amount": round(random.uniform(50, 5000), 2),
        "method": random.choice(methods),
        "status": random.choice(pay_statuses),
    })

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
                if failed <= 3:  # only show first 3 errors
                    print(f"  x Failed: {res.status_code} - {res.json().get('detail', res.text)[:100]}")
        except requests.ConnectionError:
            print(f"  x Cannot connect! Is the backend running? (python3 run_all.py)")
            return
    print(f"  + {success} created, {failed} failed")

# ── Run in correct order ────────────────────
print("=" * 55)
print("  Seeding Hotel Booking System — 50 records each")
print("  Order: Hotels → Rooms → Guests → Bookings → Payments")
print("=" * 55)

seed("hotels", hotels, "Hotels")
seed("rooms", rooms, "Rooms")
seed("guests", guests, "Guests")
seed("bookings", bookings, "Bookings")
seed("payments", payments, "Payments")

print("\n" + "=" * 55)
print("  Done! 250 total records. Refresh your browser.")
print("=" * 55)
