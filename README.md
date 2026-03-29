# 🏨 Hotel Booking System — Microservices Architecture

A microservices-based Hotel Booking System built with **Python FastAPI**, **SQLite**, and **React + Tailwind CSS**, developed as part of the IT4020 Modern Topics in IT module at SLIIT.

---

## 📋 Project Info

| Field | Details |
|---|---|
| Module | IT4020 - Modern Topics in IT |
| Assignment | Assignment 2 |
| Year | Year 4 Semester 1/2 — 2026 |
| Institution | Sri Lanka Institute of Information Technology (SLIIT) |
| Architecture | Microservices + API Gateway |
| Submission Deadline | 31.03.2026 |

---

## 👥 Group Members & Contributions

| Member | Service | Port | Branch |
|---|---|---|---|
| Member 1 | Hotel Service | 8001 | Hotel-Service |
| Member 2 | Room Service | 8002 | Room-Service |
| Member 3 | Guest Service | 8003 | Guest-Service |
| Member 4 | Booking Service | 8004 | Booking-Service |
| Member 5 | Payment Service | 8005 | Payment-Service |
| All | API Gateway | 8000 | main |
| All | React Frontend | 5173 | main |

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.11+ | Backend programming language |
| FastAPI | Web framework for REST APIs |
| Uvicorn | ASGI server to run FastAPI |
| SQLAlchemy | ORM for database operations |
| SQLite | Lightweight database (one per service) |
| httpx | HTTP client for inter-service communication |
| Pydantic | Data validation and request/response schemas |
| React | Frontend UI framework |
| Tailwind CSS | Utility-first CSS styling |
| Axios | HTTP client for frontend API calls |
| Vite | Frontend build tool and dev server |

---

## 📁 Project Structure

```
MTIT_assinment2/
├── run_all.py                  # Start all backend services at once
├── seed_data.py                # Populate all services with 10 records each (50 total)
├── README.md
├── .gitignore
│
├── api-gateway/                # API Gateway (port 8000)
│   ├── main.py                 # Dynamic catch-all routing to microservices
│   └── requirements.txt
│
├── hotel-service/              # Hotel Service (port 8001)
│   ├── main.py                 # App entry + health check endpoint
│   ├── routes.py               # HTTP layer — CRUD + search/filter/pagination
│   ├── service.py              # Business logic layer
│   ├── models.py               # SQLAlchemy database model
│   ├── schemas.py              # Pydantic request/response schemas
│   ├── database.py             # SQLite connection setup
│   └── requirements.txt
│
├── room-service/               # Room Service (port 8002)
│   ├── main.py
│   ├── routes.py               # CRUD + filter/pagination, calls Hotel Service
│   ├── service.py              # Business logic layer
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   └── requirements.txt
│
├── guest-service/              # Guest Service (port 8003)
│   ├── main.py
│   ├── routes.py               # CRUD + search/filter/pagination
│   ├── service.py              # Business logic layer
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   └── requirements.txt
│
├── booking-service/            # Booking Service (port 8004)
│   ├── main.py
│   ├── routes.py               # CRUD + filter/pagination, calls Guest & Room services
│   ├── service.py              # Business logic + inter-service communication
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   └── requirements.txt
│
├── payment-service/            # Payment Service (port 8005)
│   ├── main.py
│   ├── routes.py               # CRUD + filter/pagination, calls Booking Service
│   ├── service.py              # Business logic + inter-service communication
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   └── requirements.txt
│
└── frontend/                   # React Frontend (port 5173)
    ├── package.json
    ├── vite.config.js
    ├── src/
    │   ├── main.jsx
    │   ├── App.jsx             # Router + page navigation
    │   ├── theme.js            # Centralized design system (colors, styles, badges)
    │   ├── api/
    │   │   └── api.js          # All API calls routed via API Gateway
    │   ├── components/
    │   │   └── Navbar.jsx      # Dark navy navbar with active tab indicator
    │   └── pages/
    │       ├── HotelsPage.jsx  # CRUD + search by name + filter by city/stars + pagination
    │       ├── RoomsPage.jsx   # CRUD + filter by hotel/type/availability/price + pagination
    │       ├── GuestsPage.jsx  # CRUD + search by name/email + filter by nationality + pagination
    │       ├── BookingsPage.jsx # CRUD + filter by guest/room/status/date range + pagination
    │       └── PaymentsPage.jsx # CRUD + filter by booking/status/method/amount + pagination
    └── ...
```

---

## 🏗️ Architecture Overview

```
                    React Frontend (port 5173)
                             │
                             ▼
                    API Gateway (port 8000)
                    [Single Entry Point — no multiple ports]
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
          ▼                  ▼                  ▼
    Hotel Service      Room Service       Guest Service
    (port 8001)        (port 8002)        (port 8003)
    hotels.db          rooms.db           guests.db
          ▲                  ▲                  ▲
          │                  │                  │
          └──────── Booking Service ────────────┘
                    (port 8004)
                    bookings.db
                             ▲
                             │
                    Payment Service
                    (port 8005)
                    payments.db
```

### 🔗 Inter-Service Communication

| Service | Calls | Purpose |
|---|---|---|
| Room Service | Hotel Service | Verify hotel exists before creating a room |
| Booking Service | Guest Service | Verify guest exists before creating a booking |
| Booking Service | Room Service | Verify room exists and is available |
| Booking Service | Room Service | Mark room as **unavailable** after booking created |
| Booking Service | Room Service | Mark room as **available** after booking deleted |
| Payment Service | Booking Service | Verify booking exists before creating a payment |

---

## ⚙️ Setup Guide

### Step 1 — Clone the Repository

```bash
git clone https://github.com/SandaruwanChandrasena/MTIT_assinment2.git
cd MTIT_assinment2
```

### Step 2 — Create & Activate Virtual Environment

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3 — Install Backend Dependencies

```bash
pip install fastapi uvicorn sqlalchemy httpx requests
```

### Step 4 — Install Frontend Dependencies

```bash
cd frontend
npm install
cd ..
```

---

## 🚀 Running the Application

### Terminal 1 — Start All Backend Services

```bash
# Mac/Linux
source venv/bin/activate
python3 run_all.py

# Windows
venv\Scripts\activate
python run_all.py
```

This starts all 5 microservices and the API Gateway simultaneously on their respective ports.

### Terminal 2 — Seed Demo Data (one-time only)

```bash
# Mac/Linux
source venv/bin/activate
python3 seed_data.py

# Windows
venv\Scripts\activate
python seed_data.py
```

Creates **50 records total** (10 per service) with real Sri Lankan hotel data, seeded in dependency order so all inter-service validations pass: Hotels → Rooms → Guests → Bookings → Payments.

> To re-seed fresh data, delete the `.db` files first:
> ```bash
> # Windows
> del hotel-service\hotels.db room-service\rooms.db guest-service\guests.db booking-service\bookings.db payment-service\payments.db
> # Mac/Linux
> rm hotel-service/hotels.db room-service/rooms.db guest-service/guests.db booking-service/bookings.db payment-service/payments.db
> ```

### Terminal 3 — Start Frontend

```bash
cd frontend
npm run dev
```

Open **http://localhost:5173** in your browser.

---

## 🌐 API Endpoints

### Via API Gateway (port 8000) — Recommended

| Service | URL |
|---|---|
| Hotels | http://localhost:8000/hotels |
| Rooms | http://localhost:8000/rooms |
| Guests | http://localhost:8000/guests |
| Bookings | http://localhost:8000/bookings |
| Payments | http://localhost:8000/payments |

### Hotel Service — Search, Filter & Pagination

| Operation | Method | Endpoint | Notes |
|---|---|---|---|
| Get all | GET | `/hotels` | Supports all filters below |
| Search by name | GET | `/hotels?search=Hilton` | Case-insensitive partial match |
| Filter by city | GET | `/hotels?city=Colombo` | Case-insensitive |
| Filter by country | GET | `/hotels?country=Sri Lanka` | Case-insensitive |
| Filter by stars | GET | `/hotels?stars=5` | Exact match (1–5) |
| Min rating | GET | `/hotels?min_rating=4` | Greater than or equal |
| Active only | GET | `/hotels?is_active=true` | |
| Pagination | GET | `/hotels?skip=0&limit=20` | Default: skip=0, limit=20 |
| Get one | GET | `/hotels/{id}` | |
| Create | POST | `/hotels` | |
| Full update | PUT | `/hotels/{id}` | |
| Partial update | PATCH | `/hotels/{id}` | Only send changed fields |
| Delete | DELETE | `/hotels/{id}` | |
| Health check | GET | `/health` | Service + DB status |

### Room Service — Filter & Pagination

| Filter | Example |
|---|---|
| By hotel | `/rooms?hotel_id=1` |
| By type | `/rooms?room_type=Suite` |
| By availability | `/rooms?is_available=true` |
| By price range | `/rooms?min_price=100&max_price=300` |
| Pagination | `/rooms?skip=0&limit=20` |

### Guest Service — Search & Filter

| Filter | Example |
|---|---|
| Search name/email | `/guests?search=John` |
| By nationality | `/guests?nationality=Sri Lankan` |
| Pagination | `/guests?skip=0&limit=20` |

### Booking Service — Filter & Pagination

| Filter | Example |
|---|---|
| By guest | `/bookings?guest_id=1` |
| By room | `/bookings?room_id=2` |
| By status | `/bookings?status=confirmed` |
| Date range | `/bookings?check_in_from=2026-04-01&check_in_to=2026-06-30` |
| Pagination | `/bookings?skip=0&limit=20` |

### Payment Service — Filter & Pagination

| Filter | Example |
|---|---|
| By booking | `/payments?booking_id=1` |
| By status | `/payments?status=paid` |
| By method | `/payments?method=card` |
| By amount range | `/payments?min_amount=100&max_amount=500` |
| Pagination | `/payments?skip=0&limit=20` |

---

## 📄 Swagger UI (Interactive API Docs)

Each FastAPI service auto-generates interactive API documentation:

| Service | Direct Swagger URL | Via Gateway |
|---|---|---|
| Hotel Service | http://localhost:8001/docs | http://localhost:8000/hotels |
| Room Service | http://localhost:8002/docs | http://localhost:8000/rooms |
| Guest Service | http://localhost:8003/docs | http://localhost:8000/guests |
| Booking Service | http://localhost:8004/docs | http://localhost:8000/bookings |
| Payment Service | http://localhost:8005/docs | http://localhost:8000/payments |
| API Gateway | http://localhost:8000/docs | — |

---

## 🗄️ Database

Each service has its own **isolated SQLite database** (Database-per-Service pattern). Services never share databases — they communicate only via HTTP.

| Service | Database File |
|---|---|
| Hotel Service | `hotel-service/hotels.db` |
| Room Service | `room-service/rooms.db` |
| Guest Service | `guest-service/guests.db` |
| Booking Service | `booking-service/bookings.db` |
| Payment Service | `payment-service/payments.db` |

> Database `.db` files are created automatically on first run and are excluded from Git via `.gitignore`.

---

## 🎨 Frontend Theme System

The frontend uses a centralized design system in `src/theme.js`. All colors, button styles, badges, table styles, and form styles are defined in one place and imported by every component.

**To change the entire app theme**, only edit `src/theme.js`:

```js
// src/theme.js
export const colors = {
  primary:       "#2563eb",   // change this to switch the main color
  primaryLight:  "#eff6ff",   // light background tint
  primaryBorder: "#bfdbfe",   // border color
  navBg:         "#0f172a",   // navbar background
  // ...
};
```

All 5 pages, the navbar, buttons, table headers, badges, and form labels update automatically.

---

## ✅ Microservices Patterns Implemented

| Pattern | Description |
|---|---|
| **API Gateway Pattern** | Single entry point (port 8000) routing all requests — client never calls services directly |
| **Database per Service** | Each service owns its own isolated SQLite database |
| **Service Layer Pattern** | All services separate HTTP concerns (routes.py) from business logic (service.py) |
| **Inter-Service Communication** | Services validate data across boundaries via HTTP using `httpx` |
| **Health Check Endpoint** | `/health` on Hotel Service returns service + DB status |
| **Input Validation** | Pydantic schemas with field-level constraints on all services |
| **Search, Filter & Pagination** | All 5 services support query parameters for filtering and pagination |
| **Availability Management** | Room availability automatically updated when bookings are created or deleted |
| **Centralized Theme System** | Frontend uses a single `theme.js` file for all design tokens |

---

## ⛔ Stopping Services

Press `CTRL+C` in each terminal window to stop all services.

---

## 📝 Notes

- All backend services must be running before using the frontend or running `seed_data.py`
- The frontend communicates **exclusively through the API Gateway** (port 8000) — never directly to microservices
- CORS is configured on the API Gateway to allow requests from the React frontend (port 5173)
- SQLite `.db` files and `venv/` are excluded from Git via `.gitignore`
- The `service.py` layer exists in all 5 microservices for consistent architecture
- Inter-service calls (booking validation, room availability updates) are handled inside `service.py`, not `routes.py`